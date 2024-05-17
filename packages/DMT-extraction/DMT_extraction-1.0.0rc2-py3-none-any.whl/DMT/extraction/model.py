""" Model of model building.

Inherits from circuit to directly include the equivalent circuit here.
"""

# DMT
# Copyright (C) from 2022  SemiMod
# Copyright (C) until 2021  Markus Müller, Mario Krattenmacher and Pascal Kuthe
# <https://gitlab.com/dmt-development/dmt-extraction>
#
# This file is part of DMT-extraction.
#
# DMT-extraction is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# DMT-extraction is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along with DMT-extraction.
# If not, see <https://www.gnu.org/licenses/>.
import re
from collections import OrderedDict
from inspect import signature, getsource  # , _empty
from functools import wraps
import numpy as np
from DMT.core.mc_parameter import McParameterCollection
from DMT.exceptions import NanInfError


def check_nan_inf(func):
    """This wrapper for mathematical functions checks if that functions returns Nan or Inf values.
    If such a value is returned, an error is raised and the function arguments are also given, which is
    useful to debug model equations.
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        func_return = func(*args, **kwargs)
        if np.isnan(func_return).any() or np.isinf(func_return).any():
            message = "Method {} returned NaN or Inf".format(func.__name__)
            bound_args = signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()
            message = message + r"\n" + str(dict(bound_args.arguments))
            raise NanInfError(message)

        else:
            return func_return

    return func_wrapper


def vectorize(func):
    """This decorator can be used to vectorize model functions. Somehow it slows everything down heavily,
    it is currently not clear why!
    https://www.pythonlikeyoumeanit.com/Module3_IntroducingNumpy/VectorizedOperations.html
    """

    @wraps(func)
    def vectorize_wrapper(*args, **kwargs):
        n_args = len(args)
        n_kwargs = len(kwargs)
        if n_args > 32:
            raise IOError("DMT -> vectorize: Can only vectorize up to 32 args.")

        elif (n_args + n_kwargs) > 32:
            delta = 32 - n_args  # exclude last delta kwargs
            func_vectorized = np.vectorize(func, excluded=list(kwargs.keys())[delta - 1 :])

        else:
            func_vectorized = np.vectorize(func)

        return func_vectorized(*args, **kwargs)

    return vectorize_wrapper


def memoize(obj):
    r"""Decorator that implements memoization for McParameter objects in \*args."""
    cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        # find mcards
        mcard = None
        args_cache = None
        for i_arg, arg in enumerate(args):
            if isinstance(arg, McParameterCollection):
                mcard = arg
                args_cache = tuple(
                    [arg_a for i_arg_a, arg_a in enumerate(args) if i_arg_a != i_arg]
                )
                break

        if mcard is None:
            key = str(args) + str(kwargs)
        else:
            key = (
                str(args_cache) + str(kwargs) + mcard.print_parameters()
            )  # hashing would be better

        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


class Model(object):
    """
    Base class for compact models that can be evaluated analytically in Python.

    Parameters
    ----------
    model_name : str
        Name of the model
    version : float
        Specifies the version of the model
    nodes : [str]
        Nodes of the model
    independent_vars : [str]
        Variables of the models which sould be considered independent, like voltages, currents and temperatures... 'kwargs' is added per default
    model_resistance_info : dict
        Dictionary describing the dependencies for the model method 'model_resistance'. For each key a tuple is expected if it is given. The possible keys are:

        * 'independent_vars': Independent variables of this model method.
        * 'depends': The model method depends on these other model methods.
        * 'depends_optional': The model method CAN depend on these additional model methods to model the full voltage and current range.

    Attributes
    ----------
    model_name : str
        Name of the model
    version : float
        Specifies the version of the model
    nodes : [str]
        Nodes of the model
    independent_vars : [str]
        Variables of the models which should be considered independent, like voltages, currents and temperatures...
    netlist : [:class:`~DMT.core.CircuitElement`]
        Netlist of the equivalent circuit of this model.
    """

    def __init__(self, model_name, version, nodes, independent_vars):
        self.model_name = model_name
        self.version = version
        self.nodes = nodes
        self.independent_vars = ["kwargs", "_kwargs"] + independent_vars
        self.netlist = []

        self.model_resistance_info = {"independent_vars": ("v",)}

    def get_param_list(self, meq_function, all_parameters=False, dict_info=None):
        """Returns a list with the McParameter names for meq_function in correct order.

        Parameters
        ----------
        meq_function : function
            Function of the model equation which shall be used.
        all_parameters : {False, True}, optional
            If True, the independent_vars are ignored and the full parameter list is returned.

        Returns
        --------
        params : list
            List of parameters for this function
        """
        sig = signature(meq_function)
        func_params = list(sig.parameters)

        if dict_info is None:
            try:
                # always grab the dict info from the object the method is attached to
                dict_info = getattr(meq_function.__self__, meq_function.__name__ + "_info")
            except AttributeError as err:
                print(err)  # can be removed as soon as all bugs are fixed
                dict_info = {}

        ### These 3 keys can be in each dict!
        if "depends" not in dict_info:
            dict_info["depends"] = ()
        if "depends_optional" not in dict_info:
            dict_info["depends_optional"] = ()
        if "independent_vars" not in dict_info:
            dict_info["independent_vars"] = ()

        if "indep_vars" in dict_info:
            raise NotImplementedError(
                "It is now called 'independent_vars' to be more specific. Please correct it!"
            )
        if not isinstance(dict_info["depends"], tuple):
            raise NotImplementedError("MUST be tuple! Error in " + meq_function.__name__ + "_info")
        if not isinstance(dict_info["depends_optional"], tuple):
            raise NotImplementedError("MUST be tuple! Error in " + meq_function.__name__ + "_info")
        if not isinstance(dict_info["independent_vars"], tuple):
            raise NotImplementedError("MUST be tuple! Error in " + meq_function.__name__ + "_info")

        ## more bug safety!
        try:
            source_depends = re.findall(r"self\.(.*?)\(", getsource(meq_function))
            for depends in source_depends:
                if (
                    depends not in dict_info["depends"]
                    and depends not in dict_info["depends_optional"]
                ):
                    if (
                        "xstep." + depends not in dict_info["depends"]
                        and depends.replace("model.", "") not in dict_info["depends"]
                    ):
                        print(
                            "The model method "
                            + meq_function.__name__
                            + " may depend on (not mentioned in info_dict): "
                            + depends
                        )
        except OSError:
            pass

        setattr(self, meq_function.__name__ + "_info", dict_info)  # write it back for next time...

        for dependence in dict_info["depends"]:
            try:
                if dependence.startswith("xstep."):
                    func_params += self.get_param_list(
                        getattr(meq_function.__self__, dependence[6:]),
                        all_parameters=all_parameters,
                    )
                else:
                    func_params += self.get_param_list(
                        getattr(self, dependence), all_parameters=all_parameters
                    )
            except AttributeError:
                func_params.append(dependence)

        opti_params = []
        for method_dependent in dict_info["depends_optional"]:
            if method_dependent.startswith("xstep."):
                opti_params += self.get_param_list(
                    getattr(meq_function.__self__, method_dependent[6:]),
                    all_parameters=all_parameters,
                )
            else:
                opti_params += self.get_param_list(
                    getattr(self, method_dependent), all_parameters=all_parameters
                )

        # unique it!
        func_params = list(OrderedDict.fromkeys(func_params))

        if all_parameters:
            func_params = list(OrderedDict.fromkeys(func_params + opti_params))
            return func_params

        # delete the parameters which are independent and without the opti_params
        params = []
        for param in func_params:
            if not param in self.independent_vars:
                if not param in dict_info["independent_vars"]:
                    params.append(param)

        return params
