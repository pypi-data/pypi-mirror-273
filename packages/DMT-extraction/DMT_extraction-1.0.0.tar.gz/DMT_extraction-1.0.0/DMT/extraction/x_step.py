""" Extraction step super class and some decorators for the extraction and its GUI

Author: Mario Krattenmacher | Mario.Krattenmacher@semimod.de
Author: Markus Müller | Markus.Mueller3@tu-dresden.de
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
# pylint: disable=too-many-lines
import abc
import copy
import time
import logging
from functools import wraps
from collections import OrderedDict
import warnings
import _pickle as cpickle
import numpy as np
import scipy.optimize as sciopt
import scipy.interpolate as sciint
from typing import Dict
import re

from qtpy.QtCore import QObject, Signal  # here it is changed to PySide6 (why?)

from DMT.core import (
    SimCon,
    Plot,
    McParameter,
    McParameterCollection,
    MCard,
    specifiers,
    SpecifierStr,
    DataFrame,
    naming,
    DutLib,
)

from DMT.extraction import find_nearest_index
from DMT.extraction import IYNormDefault
from DMT.extraction import Bounds, XBounds, YBounds, XYBounds
from DMT.exceptions import (
    Stopped,
    Canceled,
    ValueTooLargeError,
    DataReferenceEmpty,
    NanInfError,
    ValueAtBoundsError,
    ParaExistsError,
)
from DMT.external.verilogae import get_param_list


def plot(plot_to_gui=True, reinit=True):
    """Marks a function as a supplier for plotting in the GUI."""

    def decorate_plot(func_plot):
        @wraps(func_plot)
        def wraps_plot(*args, mcard=None, calc_all=True):
            if calc_all:
                if mcard is None:
                    args[0].data_model = args[0].calc_all(
                        None, args[0].mcard, jac=False, reinit=reinit
                    )  # maybe somehow more beautiful
                else:
                    args[0].data_model = args[0].calc_all(
                        None, mcard, jac=False, reinit=reinit
                    )  # maybe somehow more beautiful

            return func_plot(*args)

        wraps_plot._plot_to_gui = plot_to_gui
        return wraps_plot

    return decorate_plot


def print_to_documentation(print_to_documentation=True):
    """Plot for the documentation. This way not all shown plots are passed to the documentation."""

    def decorate_print(func_plot):
        @wraps(func_plot)
        def wraps_plot(*args, **kwargs):
            return func_plot(*args, **kwargs)

        wraps_plot.print_to_documentation = print_to_documentation
        return wraps_plot

    return decorate_print


class XStep(QObject):
    """Template class for all parameter extraction classes that inherit from this class.
    XStep subclasses need to implement all methods with the decorator @abc.abstractclass.
    This class implements logic to fit data, from either a "Model" or "Circuit SImulation" to reference
    data. For fitting, a "modelcard" is used, that is a named list of parameters with attributes.

    Parameters
    ----------
    name                    : string
        This string specifies the name of the XStep object. The name should be unique when XStep objects are added to an Xtraction object,
        a container-like object for XSteps.
    mcard                   : :class:`~DMT.core.mcard.MCard` or :class:`~DMT.core.mc_parameter.McParameterCollection`
        The mcard holds all relevant model parameters for the model evaluation. Unknown parameters are added to the mcard, and
        initialized as 0.
    lib                     : :class:`~DMT.core.dut_lib.DutLib`
        This DutLib object contains DutView objects with data that are relevant for this XStep.
    op_definition           : {DMT.specifier : float, tuple or list} or iterable of {DMT.specifier : float, tuple or list}
        This dictionary defines how to filter the relevant data for this XStep from the DutView objets in the DutLib by setting either a:
            * single value (float): Use only the data, where the column with a name equal to the specifier equals the single value
            * 2-element tuple: Use only the data, where the column with name equal to the specifier is bigger than the first element of the tuple and smaller than the second element of the tuple-
            * 3-element tuple: same as 2-element tuple, but take only columns in the data that have more than tuple[2] unique elements.
            * 4-element tuple: same as 3-element tuple, but take only tuple[3] equally spaced values from the column.
            * list: Use only the data, where the column with name equal to the specifier equals one of the values in the list
        More than one dictionary can be passed.
    model                   : :class:`~DMT.extraction.model.Model`, optional
        Model object with all model equations used for this extraction step.
    deembed_method          : method, optional
        If given, the data found in the DutViews by this XStep is pre-processed with the method deembed_method.
        This argument can be used to de-embed the internal or intrinsic transistor data "on the fly".
    key                     : string or [string], optional
        This key is used to find the reference data in relevant_duts.data.
        See :meth:`DMT.extraction.x_step.XStep.collect_data` for the usage.
    use_exact_key           : {True,False},False
        If this argument is set to True, only those keys in DutView data are considered, that correspond exactly to "key".
        Else, only those keys are considered that contain "key" in them.
    to_optimize             : [string]
        This list contains the names of all parameters that shall be optimized by this XStep.
    to_optimize_per_line    : [string]
        This list contains the names of all parameters that shall be optimized for each line, separately. The parameters in this
        list MUST be a subset of "to_optimize".
    op_selector             : {None, Specifier}, optional
        If given, an operating point selector plot will be created that can be displayed in the DMT Gui.
    op_selector_para        : {None, Specifier}, optional
        If given, the operating point selector will use this parameter for viewing the optimization for different operating points. Else self.to_optimize_per_line[0] will be used.
    initial_guess           : {True, False}, optional
        If True, the set_initial_guess method is called.
        Turn this off, if the parameters are already good with good boundaries in the given modelcard.
    relevant_duts            : [DutView], None
        List of DutViews, that are relevant for the current step. If none is give, only the DutLib.dut_ref DutView is considered to be relevant.
    DutCircuitClass         : :class:`~DMT.core.dut_view.DutCircuit`, optional
        The DutCircuitClass is used for simulation of DutView objects.
    circuit_sim_dir, circuit_database_dir : str, optional
        Paths where the circuit simulations and also the simulated and read duts are saved.
    get_circuit_arguments   : None
        TODO
    technology              : :class:`~DMT.core.technology`, optional
        Technology for the created DutCircuit objects. A technology specifies additional methods for example to scale modelcards.
    write_table_model       : bool, optional
        Flag to turn on copying the reference dataframes into the simulation folder, for example as table model.
    n_step_max              : int, optional
        Maximum number of optimization algorithm steps. Default = 100
    fit_method              : {'lm','trf'}
        The fit method that shall be used. 'lm' -> Levenberg Marquardt and 'trf' Trust-Region-Reflective (?)
    f_tol                   : float, optional
        The target function tolerance. Default = np.finfo(float).eps so machine tolerance.
    bounds_class            : :class:`~DMT.extraction.ixbounds.Bounds`
        Class to choose which bound type is used for this step, either x, y or both.
    t_max                   : float, optional
        The maximum time in seconds that simulations may run. Is passed on to the object of :class:`~DMT.core.DMT`. Default = 60
    n_core                  : int, optional
        The number of cores the object of :class:`~DMT.core.DMT` is allowed to use in parallel. Default = 4
    normalize               : {True, False}, optional
        If True, the model parameters that need to be extracted, are normalized to the range [0,1], if possible.
    sort_by                 : SpecifierStr, optional
        By default (None), data is sorted by x/y depending on the bounds. Change this if for example the plot is versus I_C but the measurement is over V_BE.
    legend_off              : {False, True}, optional
        Turns off the legend in the main plot.
    document_step           : {True, False}, optional
        If False, this step is not added to the documentation.
    specifier_paras         : None
        This dict with keys corresponding to arguments and values corresponding to default values for the arguments is given
        to __init__. Can be used to define which arguments must be supplied to the __init__ function.
    """

    # Signals for GUI integration
    process = Signal()
    finished = Signal()
    mcardChanged = Signal()

    def __init__(
        self,
        name,
        mcard: MCard,
        lib: DutLib,
        op_definition: dict,
        model=None,
        deembed_method=None,
        key=None,
        use_exact_key=False,
        use_regex_key=False,
        to_optimize=None,
        to_optimize_per_line=None,
        op_selector=None,
        op_selector_para=None,
        initial_guess=True,
        relevant_duts=None,
        DutCircuitClass=None,
        circuit_sim_dir=None,
        circuit_database_dir=None,
        get_circuit_arguments=None,
        technology=None,
        write_table_model=False,
        n_step_max=100,
        fit_method="trf",
        f_tol=np.finfo(float).eps,
        bounds_class=XBounds,
        t_max=60,
        n_core=4,
        normalize=True,
        sort_by=None,
        legend_off=False,
        document_step=True,
        specifier_paras=None,
        **kwargs,
    ):
        """
        Notes
        -----
        ..todo: catch input errors
        ..note: Do not actively calculate or process something in this method as
        it is overwritten often in the Subclasses of this base class.
        """
        # Qt functionality that needs to stay here
        QObject.__init__(self)
        # self.widget                 = None

        # human readable name of this XStep, simplifies logging and GUI stuff later
        self.name = name.replace(" ", "_")
        self.document_step = document_step

        self.specifier_paras = {}
        if specifier_paras is None:
            specifier_paras = {}

        for name, default in specifier_paras.items():
            if default is None and name not in kwargs:
                raise ValueError("Required argument '{}' is missing!".format(name))
            elif isinstance(default, list):
                if name in kwargs:
                    self.specifier_paras[name] = [spec for spec in kwargs[name]]
                    del kwargs[name]
                else:
                    self.specifier_paras[name] = default

            else:
                self.specifier_paras[name] = kwargs.pop(name, default)

        for key_remain in kwargs:
            warnings.warn(
                f"{type(self)}:{self.name} was created with the remaining kwarg {key_remain}={kwargs[key_remain]}",
                category=RuntimeWarning,
            )

        # extraction dut information
        self.DutCircuitClass = DutCircuitClass
        self.technology = technology
        self.circuit_sim_dir = circuit_sim_dir
        self.circuit_database_dir = circuit_database_dir
        self.get_circuit_arguments = get_circuit_arguments
        self.write_table_model = write_table_model
        self.duts = []
        self.mcard = copy.deepcopy(mcard)  # important!

        self.model = model

        # optimization parameters
        self.available_fit_methods = ["lm", "trf"]
        self.n_step_max = n_step_max
        self.fit_method = fit_method
        self.f_tol = f_tol
        self.jac = None
        self.normalize = normalize
        self.list_normalize_log = []

        # y normalization
        self.iynorm = IYNormDefault  # interface to y normalization module
        self.y_normalizer = None

        self.sort_by = sort_by

        # make sure that all steps have an model_function_info_dict
        if not hasattr(self, "model_function_info"):
            self.model_function_info = None

        # possible parameters, can be read directly from parameter list
        # if self.model is None: # is self.model is None -> step with dut_ext, just give all parameters
        if self.DutCircuitClass is None:
            try:
                possible_parameters = self.model.get_param_list(
                    self.model_function, dict_info=self.model_function_info
                )  # sorting this list for groups from mcard ?!?
            except AttributeError:
                possible_parameters = get_param_list(
                    self.model_function, info=self.model_function_info
                )
        else:
            possible_parameters = self.mcard.name

        if to_optimize is None:  # if not given all should be optimized
            to_optimize = possible_parameters

        if to_optimize_per_line is None:  # if not given all parameters are optimized globally
            to_optimize_per_line = []

        # op selection tool
        self.op_selector = False
        self.op_selection_fig = None
        self.op_selector_x = None
        self.op_selector_y = None

        self.op_selector_along = op_selector
        if op_selector_para is None:
            self.op_selector_para = []
        else:
            self.op_selector_para = op_selector_para
        if op_selector is not None and to_optimize_per_line is []:
            raise IOError(
                "DMT -> XStep: You can not specify to_optimize_per_line if op_selector is not None. When op_selector is not None, all parameters are automatically per_line."
            )
        # set operating point selector properties
        if op_selector is not None:
            if op_selector not in op_definition.keys():
                self.op_selector = True
            else:
                op_selection = op_definition[op_selector]
                try:
                    if len(op_selection) > 1:
                        self.op_selector = True
                except (AttributeError, TypeError):
                    pass

        # except of course tnom! Also catch a possible wrong user input here!
        to_optimize = [para for para in to_optimize if para != "tnom"]

        # unique it!
        to_optimize = list(OrderedDict.fromkeys(to_optimize))
        self.to_optimize_per_line = list(OrderedDict.fromkeys(to_optimize_per_line))
        if self.op_selector:
            self.to_optimize_per_line = to_optimize
            to_optimize_per_line = to_optimize

        # make sure that to_optimize_per_line parameters are in to optimize, so that user is aware of what is beeing optimized
        for para in to_optimize_per_line:
            if not para in to_optimize:
                raise IOError(
                    "DMT -> XStep: The parameters in to_optimize_per_line need to be a subset of to_optimize."
                )
        if len(to_optimize_per_line) > 0 and self.model is None:
            raise IOError(
                "DMT -> XStep: Optimization of parameters per line is currently only implemented with model functions."
            )

        # remove elements from to_optimize that shall be optimized per line
        to_optimize = [para for para in to_optimize if para not in to_optimize_per_line]

        # sort possible parameters so that the parameters from to_optimize are at the start
        possible_parameters = list(OrderedDict.fromkeys(to_optimize + possible_parameters))

        # make sure all possible paras are in mcard. If not, add them.
        for para in possible_parameters:
            if (
                para == op_selector_para
            ):  # [] of string to get a Composition and not a single parameter
                self.paras_derived = self.mcard.get(
                    [op_selector_para]
                )  # these are parameters that depend indirectly from the optimization results

            if (
                para in to_optimize_per_line and para != op_selector_para
            ):  # Op Selector Para Stays in Modelcard
                try:
                    self.mcard.remove(para)
                except KeyError:
                    pass
            else:  # other parameters are added to modelcard, if not already present
                try:
                    para = self.mcard.get(para)
                except KeyError:
                    self.mcard.add(
                        McParameter(para, value=0, group="AAAA")
                    )  # group so that these parameters are at the start!
                    # the value is set to a better value in self.set_initial_guess(), later.

        # remove the paras_per_line from paras_possible since control of them in the GUI makes no sense currently
        for para in self.to_optimize_per_line:
            if para != op_selector_para:
                try:
                    possible_parameters.remove(para)
                except ValueError as err:
                    raise IOError(
                        "DMT " + self.name + ": Parameter " + para + " not in possible parameters."
                    ) from err

        # sort the possible parameters for group and name
        mc_possible_parameters = self.mcard.get(possible_parameters)
        try:
            possible_parameters = [
                para.name
                for para in sorted(
                    mc_possible_parameters.paras, key=lambda para: (para.group, para.name)
                )
            ]
        except TypeError:  # group not always there
            pass
        possible_parameters = list(
            OrderedDict.fromkeys(to_optimize + possible_parameters)
        )  # move to optimize to start again

        # from here on, these attributes are instances of McParameterCollection.
        self.paras_possible = self.mcard.get(possible_parameters)  # list of all possible paras

        # sort parameters in self.paras_possible to display them in GUI

        self.paras_to_optimize = self.mcard.get(to_optimize)  # list of the parameters to optimize
        self.paras_to_optimize_per_line = []
        if not self.op_selector:
            self.paras_derived = McParameterCollection()
        self.paras_to_push = copy.deepcopy(
            self.paras_to_optimize + self.paras_derived
        )  # per default, paras_to_push equals paras_to_optimize.

        self._initial_guess = initial_guess

        # reference data information
        self.data_reference = []
        self.data_model = []
        self.lib = lib
        self.key = key
        self.use_exact_key = use_exact_key
        self.use_regex_key = use_regex_key
        self.p_o_a = None
        self.inited_data = False
        if not isinstance(op_definition, list):  # single op_def we put into list
            self.op_definitions = [op_definition]
        else:  # is already iterable
            self.op_definitions = op_definition
        self.deembed_method = deembed_method
        self.relevant_duts = relevant_duts

        # bounds
        self.bounds_class = bounds_class
        self._x_bounds = []

        # interpolation
        self.interpolate = False
        self.spline_order = 3
        self.points_out_of_bounds = 1
        self.spline_nr_points = 50
        self.smoothing_factor = 0
        self.spline_weights = None

        # simulation controller object
        self.sim_con = SimCon(n_core=n_core, t_max=t_max)

        # for visualization and gui interaction
        self.ui = None
        self.other_plots = []

        self.labels = []
        self.stopped = False
        self.canceled = False
        self.legend_off = legend_off
        self.main_fig = None

        # op selector stuff
        self.op_selector_fig = None
        self._op_selector_bounds = None

        self.plots_switched = {}
        self.prints_switched = {}
        self.sum_time = 0.0

        # check if just one T
        ts = []
        for op_def in self.op_definitions:
            try:
                t = op_def[specifiers.TEMPERATURE]
                ts.append(t)
            except KeyError:
                pass

        ts = np.unique(ts)
        self.one_t = False
        if len(ts) == 1:
            self.one_t = True

    def __re_init__(self):
        """Workaround to refresh QtSignals after reload."""
        try:
            QObject.__init__(self)
        except RuntimeError:
            pass

        # self.init_data()

    def add_to_xtraction(self, xtraction):
        """Sets the duts from xtraction to the given step

        Parameters
        ----------
        xstep : :class:`~DMT.extraction.XTraction`]
        """

        self.lib = xtraction.lib
        self.technology = xtraction.technology

        self.circuit_sim_dir = xtraction.dirs["sim_dir"]
        self.circuit_database_dir = xtraction.dirs["circuit_database_dir"]

        self.__re_init__()

    def init_data(self):
        self.inited_data = False
        self.data_reference = []
        self.data_model = []
        self.labels = []
        self.collect_data()

        # check if any data has been found
        found = False
        for dut in self.relevant_duts:
            for key in dut.data:
                if self.validate_key(key):
                    found = True
                    break
        if not found:
            raise IOError(f"XStep with name {self.name} did not find any suitable data.")

        # check if data contains what is needed and add to data_reference
        self.ensure_input_correct()
        self.init_data_reference()

        if not self.data_reference:
            raise DataReferenceEmpty(f"The data reference of the step {self.name} are empty.")

        self.order_data_reference()
        if self._initial_guess:
            self.init_parameters_per_line()  # now the number of lines is known, so we can init the parameters per line ONCE
            self.set_initial_guess(self.data_reference)
            self._initial_guess = False  # only do this once...

        self.inited_data = True

        logging.info("Initialized the extraction step %s.", self.name)

    def init_parameters_per_line(self):
        """Initialize a McParameterCollection for each line with paras_to_optimize_per_line."""

        for _line in self.data_reference:
            composition = McParameterCollection()
            for para in self.to_optimize_per_line:
                para = McParameter(para, value=0)
                composition.add(para)

            self.paras_to_optimize_per_line.append(composition)

    def collect_data(self):
        """This method looks for all data in duts in self.relevant_duts and then applies the filter specified by self.op_definition. If data remains, it is considered relevant for this step.

        The function check_key checks the dut key versus self.key, if the data should be part of the current extraction step.
        The check depends on what type is self.key. Possible is:

        * str : Checks if self.key is part of key
        * [str] : Checks if any element of self.key is part of key


        """

        def check_key(key):
            """Does the key checking depending whats in self.key

            Parameters
            ----------
            key : str
                key to check

            Returns
            -------
            {True, False}

            """
            if self.use_exact_key:
                try:
                    if isinstance(self.key, list):
                        if not len(self.key) == 1:
                            raise IOError(
                                'The "use_exact_key" option requires a single string as the key, not a list.'
                            )
                    key_parts = key.split("/")
                    return self.key == key_parts[-1]
                except TypeError:
                    return any([key_a == key for key_a in self.key])  # wont work like this
            elif self.use_regex_key:
                return bool(re.search(self.key, key))
            else:
                try:
                    return self.key in key
                except TypeError:
                    return any([key_a in key for key_a in self.key])

        if self.relevant_duts is None:
            self.relevant_duts = [self.lib.dut_ref]
        elif not isinstance(self.relevant_duts, list):
            self.relevant_duts = [self.relevant_duts]

        for i, op_def in enumerate(self.op_definitions):  # more than one op_definition possible
            for key in list(op_def.keys()):
                if isinstance(key, naming.SpecifierStr):
                    spec_key = key
                else:
                    raise IOError(
                        "DMT -> XStep: Keys of op_definition must be objects of class SpecifierStr. Occurred in XStep "
                        + self.name
                        + "."
                    )

                if not isinstance(spec_key, naming.SpecifierStr):
                    warn_str = (
                        "DMT->"
                        + self.name
                        + ": The op_definition key "
                        + str(key)
                        + " could not be converted into a SpecifierStr. This will result in an error, if you try to generate an extraction documentation."
                    )
                    warnings.warn(warn_str)
                    logging.warning(warn_str)
                else:
                    self.op_definitions[i][spec_key] = self.op_definitions[i].pop(key)

        for dut in self.relevant_duts:
            for key in list(dut.data.keys()):  # to make sure dict can change during iteration
                if check_key(key):  # found a data key with relevant data for this xstep.
                    if key.startswith("_"):
                        continue  # do not access private step data

                    if self.p_o_a is None and key.startswith("q"):
                        continue  # if not poa, do not touch xq data
                    elif self.p_o_a is not None and not key.startswith("q"):
                        continue  # if poa, do not touch normal data

                    key_temp = dut.get_key_temperature(key)

                    for op_definition in self.op_definitions:
                        # check temperature
                        if specifiers.TEMPERATURE in op_definition.keys():
                            temp_def = op_definition[specifiers.TEMPERATURE]
                            if isinstance(temp_def, tuple):
                                if (key_temp < temp_def[0]) or (key_temp > temp_def[1]):
                                    continue
                            elif isinstance(temp_def, (float, int)):
                                if not np.isclose(key_temp, temp_def, atol=1e-3):
                                    continue
                            else:
                                if isinstance(temp_def, list):
                                    temp_def = np.array(temp_def)

                                if not np.isclose(key_temp, temp_def, atol=1e-3).any():
                                    continue

                        data = copy.deepcopy(dut.data[key])  # copy data
                        for op_var, op_var_value in op_definition.items():  # filter data
                            if op_var == specifiers.TEMPERATURE:
                                continue  # was already checked before

                            try:
                                col_op_var = SpecifierStr(op_var)
                                data.ensure_specifier_column(
                                    col_op_var, reference_node=dut.reference_node, ports=dut.nodes
                                )  # assume all duts are of same type
                            except KeyError:  # now we are *ducked. Last Straw: voltage ?!?
                                nodes_in_col = naming.get_nodes(op_var, dut.nodes)
                                sub_specifiers_in_col = naming.get_sub_specifiers(op_var)

                                if op_var.startswith(str(specifiers.VOLTAGE) + "_"):
                                    col_op_var = (
                                        specifiers.VOLTAGE + nodes_in_col + sub_specifiers_in_col
                                    )

                                    try:
                                        data.ensure_specifier_column(
                                            col_op_var,
                                            reference_node=dut.reference_node,
                                            ports=dut.nodes,
                                        )
                                    except (
                                        KeyError
                                    ):  # empty data and break the loop, this df has not the correct columns
                                        data = data[0:0]
                                        break
                                else:  # empty data and break the loop, this df has not the correct columns
                                    data = data[0:0]
                                    break

                            data_col_op_var = data[col_op_var].to_numpy()
                            if isinstance(op_var_value, (float, int)):
                                condition = np.isclose(
                                    data_col_op_var, op_var_value
                                )  # single float or int

                            elif isinstance(op_var_value, (list, np.ndarray)):  # this is ultra slow
                                condition = np.isclose(data_col_op_var, op_var_value[0])
                                for val in op_var_value[1:]:
                                    condition = np.logical_or(
                                        condition, np.isclose(data_col_op_var, val)
                                    )

                            elif isinstance(op_var_value, tuple):
                                condition = np.full_like(data[col_op_var], True, dtype=bool)
                                if op_var_value[1] is not None:  # only apply condition if != None
                                    condition = np.logical_and(
                                        condition, data[col_op_var].to_numpy() <= op_var_value[1]
                                    )

                                if op_var_value[0] is not None:
                                    condition = np.logical_and(
                                        condition, data[col_op_var].to_numpy() >= op_var_value[0]
                                    )

                                if (
                                    len(op_var_value) >= 3
                                ):  # only use this df if more than op_var_value[2] different points inside
                                    vals = np.unique(data_col_op_var)
                                    vals.sort()
                                    if not len(vals) > op_var_value[2]:
                                        data = data[0:0]  # empty data
                                        break
                                    if (
                                        len(op_var_value) == 4
                                    ):  # use only op_var_value[3] equally spaced points
                                        vals = vals[vals <= op_var_value[1]]
                                        vals = vals[vals >= op_var_value[0]]
                                        dist_op, _remain = divmod(
                                            len(vals), op_var_value[3]
                                        )  # integer distance between suitable operating points
                                        condition_dist = np.isclose(data_col_op_var, vals[dist_op])
                                        # condition_dist = data_col_op_var == None
                                        for i, val in enumerate(vals[dist_op + 1 :]):
                                            if i % dist_op == 0:
                                                condition_dist = np.logical_or(
                                                    condition_dist,
                                                    np.isclose(data_col_op_var, val, atol=2e-4),
                                                )
                                        condition = np.logical_and(condition, condition_dist)

                                    else:
                                        raise IOError(
                                            "DMT->XStep: Not more than three element tuples are supported in op_selector keyword argument. Did you mean a list instead of a tuple?"
                                        )

                            else:
                                raise IOError(
                                    "DMT->XStep: Can only collect the data for op_values of class float, int, list, np.ndarray or tuples. \nGiven was the variable "
                                    + str(op_var)
                                    + " with the value "
                                    + str(op_var_value)
                                    + " of the type "
                                    + type(op_var_value)
                                )

                            data = data[condition]

                        if not data.empty:
                            new_key = dut.join_key(
                                "_", self.__class__.__name__, self.name, key
                            )  # get_key methode dutview
                            if self.deembed_method is None:
                                dut.data[new_key] = data  # save new data
                            else:
                                dut.data[new_key] = self.deembed_method(
                                    df=data, mc=self.mcard, t_dev=key_temp, model=self.model
                                )  # save deembeded data

                    # else:
                    #     raise IOError('DMT -> XStep: Did not find any suitable data for dut ' + dut.name + ' in XStep of class ' + self.__class__.__name__+' with name ' + self.name + '.')

    @property
    def plot_methods(self):
        """Returns all methods to plot in the GUI"""
        list_methods = []
        for methodname in dir(self):
            if methodname != "plot_methods":  # prevent loop
                try:
                    method = getattr(self, methodname)
                    if hasattr(method, "_plot_to_gui"):
                        list_methods.insert(0, method)
                        # turn around the order -> application of scaling equation of poa is now at start!
                except Exception:  # pylint: disable=broad-except
                    pass  # if any exception occurs, it is for sure not a plot...

        # sort to make sure that main_plot is first
        plot_methods = []
        for method in list_methods:
            if method.__name__ in self.plots_switched:
                if not self.plots_switched[method.__name__]:
                    continue
            else:
                if not method._plot_to_gui:
                    continue

            if method.__name__ == "main_plot":
                plot_methods.insert(0, method)
            else:
                plot_methods.append(method)

        return plot_methods

    def validate_key(self, key):
        """Checks if the given key belongs to the x_step by checking if the class name AND the object name is part of the key.

        Parameters
        ----------
        key : str

        Returns
        -------
        {True, False}

        """
        key_parts = self.lib[0].split_key(
            key
        )  # just take the first dut in the lib for splitting, make this a class method
        if not self.__class__.__name__ in key_parts:
            return False

        if not self.name in key_parts:
            return False

        return True

    def sort_line(self, line):
        """Sort all values in line with increasing "x" or "y" or self.sort_by and cast everything to numpy.

        Input
        -----
        line :{str:[]}
            A line with at least "x" and "y" keys that can be used for sorting.

        Returns
        -------
        line :{str:[]}
            The sorted line.
        """
        if self.sort_by is None:
            if self.bounds_class in (XBounds, XYBounds):
                indices_new = line["x"].argsort()
            else:
                indices_new = line["y"].argsort()
        else:
            indices_new = line[self.sort_by].argsort()

        # cast lists to numpy array since that is required for further processing
        n_x = np.size(line["x"])
        for key in line.keys():
            if isinstance(line[key], list):
                n_list = np.size(line[key])
                if n_list == n_x:
                    line[key] = np.array(line[key])

        # here the data gets resorted
        for key in line.keys():
            try:
                line[key] = line[key][indices_new]
            except (IndexError, TypeError):
                pass

        return line

    def order_data_reference(self):
        """Order the x,y,y_ref data in data_reference with x"""
        for line in self.data_reference:
            # ok this is hard to explain:
            # If we want to set x_bounds, the data must be ordered such that 'x' is an increasing or decreasing array
            # Similarly, if we want to set y_bounds, the data must be ordered such that 'y' is an increasing or decreasing array
            line = self.sort_line(line)

        if self.op_selector:
            self.op_selector_x = np.zeros(len(self.data_reference))
            self.op_selector_y = np.zeros(len(self.data_reference))
            for n, line in enumerate(self.data_reference):
                self.op_selector_x[n] = line[self.op_selector_along]

    def set_para_inactive(self, para):
        try:
            self.paras_to_optimize.remove(para)
        except KeyError:
            pass

    def set_para_active(self, para):
        try:
            self.paras_to_optimize.add(para)
        except ParaExistsError:
            pass

    def set_para_to_push(self, para):
        try:
            self.paras_to_push.add(para)
        except ParaExistsError:
            pass

    def remove_para_to_push(self, para):
        try:
            self.paras_to_push.remove(para)
        except KeyError:
            pass

    def main_plot(
        self,
        plot_name,
        style="xtraction_color",
        x_specifier=None,
        y_specifier=None,
        x_label=None,
        y_label=None,
        x_scale=None,
        y_scale=None,
        x_log=False,
        y_log=False,
        legend_location="upper left",
    ):  # pylint: disable=unused-argument
        """Creates the main plot that is also displayed in the GUI and printed to the documentation.

        The parameters are not used in the method here, but in the decorator :func:`~DMT.extraction.x_step.plot`

        Parameters
        ----------
        paras_model : :class:`~DMT.core.mc_parameter.McParameterCollection`, optional
            If given, it is set to this XStep before plotting.
        calc_all : {False, True}
            If True, the method :meth:`~DMT.extraction.x_step.XStep.calc_all` is called before plotting.
        """
        if self.interpolate:
            style = "xtraction_interpolated_color"

        if y_specifier is None and y_label is None:
            raise IOError(
                "DMT -> XStep -> main_plot: main_plot needs to be implemented by children of XStep and you need to give either the y_label or y_specifier argument."
            )
        if x_specifier is None and x_label is None:
            raise IOError(
                "DMT -> XStep -> main_plot: main_plot needs to be implemented by children of XStep and you need to give either the x_label or x_specifier argument."
            )

        self.main_fig = Plot(
            plot_name,
            style=style,
            x_specifier=x_specifier,
            y_specifier=y_specifier,
            x_label=x_label,
            y_label=y_label,
            x_scale=x_scale,
            x_log=x_log,
            y_log=y_log,
            y_scale=y_scale,
            num=self.name,
            legend_location=legend_location,
        )

        for line_reference, line_model, label in zip(
            self.data_reference, self.data_model, self.labels
        ):  # add the reference and model data in an alternating way
            if self.legend_off:
                if self.interpolate:
                    self.main_fig.add_data_set(line_reference["x"], line_reference["y"])
                    self.main_fig.add_data_set(line_model["x"], line_model["y_ref"])

                else:
                    self.main_fig.add_data_set(line_reference["x"], line_reference["y"])

                self.main_fig.add_data_set(line_model["x"], line_model["y"])

            else:
                if self.interpolate:
                    self.main_fig.add_data_set(
                        line_reference["x"], line_reference["y"], label="reference " + label
                    )
                    self.main_fig.add_data_set(
                        line_model["x"], line_model["y_ref"], label="interpolated " + label
                    )

                else:
                    self.main_fig.add_data_set(
                        line_reference["x"], line_reference["y"], label="" + label
                    )

                self.main_fig.add_data_set(line_model["x"], line_model["y"], label=None)

        return self.main_fig

    def op_selection_plot(self):  # pylint: disable=unused-argument
        """Creates the main plot that is also displayed in the GUI and printed to the documentation.

        The parameters are not used in the method here, but in the decorator :func:`~DMT.extraction.x_step.plot`

        Parameters
        ----------
        paras_model : :class:`~DMT.core.mc_parameter.McParameterCollection`, optional
            If given, it is set to this XStep before plotting.
        calc_all : {False, True}
            If True, the method :meth:`~DMT.extraction.x_step.XStep.calc_all` is called before plotting.
        """
        if not self.op_selector:
            return None
        else:
            y_data, x_data = np.zeros(len(self.data_reference)), np.zeros(len(self.data_reference))
            self.op_selection_fig = Plot(
                r"Extraction results vs. operating point.",
                num=self.name + "_op_selection_plot",
                style="black_solid",
                x_specifier=self.op_selector_along,
                y_label=self.op_selector_para,
                legend_location="upper left",
            )
            for n in range(len(self.data_reference)):
                x_data[n] = self.data_reference[n][self.op_selector_along]
                y_data[n] = self.paras_to_optimize_per_line[n][self.op_selector_para].value

            self.op_selection_fig.add_data_set(x_data, y_data)
            return self.op_selection_fig

    def switch_plots(self, plots_to_switch: dict):
        """Switch on or off additional plots for the GUI

        Parameters
        ----------
        plots_to_switch : dict
            Names and states to switch to.
            For example: {"plot_ib":True} switches on the extra base current plot for the XVerify-Step.
        """
        self.plots_switched.update(plots_to_switch)

    def switch_prints(self, plots_to_switch: dict):
        """Switch on or off additional plots to print into the automatic documentation

        Parameters
        ----------
        plots_to_switch : dict
            Names and states to switch to.
            For example: {"plot_ib":True} switches on the extra base current plot for the XVerify-Step.
        """

        self.prints_switched.update(plots_to_switch)

    def optimize(self):
        """Fit the model to the reference data."""
        # transform a possibly multidimension problem into a one-dimensional one
        x = np.concatenate([data["x"] for data in self.data_model])
        y = np.concatenate([data["y_ref"] for data in self.data_model])
        paras_optimized = None

        if x.size == 0:
            raise IOError("DMT -> XStep with name " + self.name + " -> optimize: X data is empty.")
        if y.size == 0:
            raise IOError("DMT -> XStep with name " + self.name + " -> optimize: Y data is empty.")

        # normalize the parameters
        p0, p_min, p_max = self.get_normalized_parameters()

        # for debugging, delete after bug found
        # print('id of mcard in XStep.optimize: ' + str(id(self.mcard)))

        old_settings = np.seterr(all="warn")  # all numpy warnings etc are now raised warnings!
        try:
            if self.fit_method == "lm":
                (paras_optimized, _paras_covariance) = sciopt.curve_fit(
                    self.fit_function,
                    x,
                    self.y_normalizer.normalize(y),
                    p0=p0,
                    method=self.fit_method,
                    ftol=self.f_tol,
                    maxfev=self.n_step_max,
                    jac=self.jacobian,
                )

            else:
                time1 = time.time()
                self.sum_time = 0.0
                (paras_optimized, _paras_covariance) = sciopt.curve_fit(
                    self.fit_function,
                    x,
                    self.y_normalizer.normalize(y),
                    p0=p0,
                    bounds=(p_min, p_max),
                    method=self.fit_method,
                    ftol=self.f_tol,
                    maxfev=self.n_step_max,
                    jac=self.jacobian,
                )
                print("our part took: " + str(self.sum_time))
                print("curve_fit overall took: " + str(time.time() - time1))

        except (Stopped, Canceled):
            print(
                "DMT -> XStep -> "
                + self.name
                + " -> optimize: Canceled/Stopped during optimization."
            )
            paras_optimized = p0  # take over initial values
            logging.error("The extraction of the step %s was canceled or stopped.", self.name)
        except RuntimeError:
            print(
                "DMT -> XStep -> " + self.name + " -> optimize: RunTimeError during optimization."
            )
            paras_optimized = p0  # take over initial values
            logging.error("While extraction of the step %s a RuntimeError occurred.", self.name)
        except sciopt.OptimizeWarning:  # who cares?
            print(
                "DMT -> XStep -> "
                + self.name
                + " -> optimize: Cant estimate covariance of parameters."
            )
            logging.warning(
                "While extraction of the step %s a sciopt.OptimizeWarning occurred.", self.name
            )
        except NanInfError:
            paras_optimized = p0  # take over initial values
            print(
                "DMT -> XStep -> "
                + self.name
                + " -> optimize: Nan or Inf during calculations in optimize."
            )
            logging.error("While extraction of the step %s a NanInfError occurred.", self.name)
        except ValueAtBoundsError:
            ## do not take over initial values !
            paras_optimized = self.get_normalized_parameters()  # get current values...
            print(
                "DMT -> XStep -> "
                + self.name
                + " -> optimize: One value was very close to its border and a change had no effect on it!"
            )

        np.seterr(**old_settings)  # all numpy warnings etc are now raised errors!

        # write back the values
        self.set_normalized_parameters(paras_optimized)

        self.mcardChanged.emit()
        self.finished.emit()

    def get_normalized_parameters(self):
        """Get the (normalized) parameters for the optimiziation and the corresponding boundaries.

        If normalize is true, all parameters are tried to be normalized either linear or logarithmic. The boundaries are given accordingly.

        Returns
        -------
        p_0, p_min, p_max : np.array
            Values, minimal bounds and maximal bounds of the parameters in correct order.
        """
        # collect the parameters
        self.paras_to_optimize = self.mcard.get(self.paras_to_optimize)

        # build handy single list
        list_paras = [self.paras_to_optimize] + self.paras_to_optimize_per_line

        # predefine numpy arrays
        nr_parameters = sum([len(paras) for paras in list_paras])
        p_0 = np.empty(nr_parameters)
        p_min = np.empty(nr_parameters)
        p_max = np.empty(nr_parameters)
        i_para = 0
        # iterate over all parameters
        for paras in list_paras:
            for para in paras:
                # first get the values as floats to reduce field accesses
                p_val_a = para.value
                p_min_a = para.min
                p_max_a = para.max

                # catch nans
                if np.isnan(p_val_a):
                    raise IOError("DMT -> XStep: para with name " + para.name + " is Nan.")
                # normalized?
                if self.normalize and (p_min_a != -np.inf) and (p_max_a != np.inf):
                    # log or lin?
                    if para.name in self.list_normalize_log:
                        p_min[i_para] = np.log10(p_min_a)
                        p_max[i_para] = np.log10(1 + p_min_a)
                        p_0[i_para] = self._get_normalized_value(
                            p_val_a, p_min_a, p_max_a, normalized="log"
                        )
                    else:
                        p_min[i_para] = 0.0
                        p_max[i_para] = 1.0
                        p_0[i_para] = self._get_normalized_value(
                            p_val_a, p_min_a, p_max_a, normalized="lin"
                        )
                else:
                    # not normalized
                    p_min[i_para] = p_min_a
                    p_max[i_para] = p_max_a
                    p_0[i_para] = p_val_a

                i_para += 1

        return p_0, p_min, p_max

    def _get_normalized_value(self, value, p_min, p_max, name=None, normalized=None):
        """Returns the normalized value.

        Parameters
        ----------
        value : float
        p_min : float
        p_max : float
        name : str, optional
            Only needed when, normalized is not given.
        normalized : {None, 'log', 'lin', ''}, optional
            If None, normalized is looked up before normalizing.

        Returns
        -------
        value_normalized : float
        """
        if normalized is None:
            if self.normalize and (p_min != -np.inf) and (p_max != np.inf):
                if name in self.list_normalize_log:
                    normalized = "log"
                else:
                    normalized = "lin"
            else:
                normalized = ""

        if normalized == "lin":
            return (value - p_min) / (p_max - p_min)
        elif normalized == "log":
            return np.log10((value - p_min) / (p_max - p_min) + p_min)
        else:
            return value

    def _get_denormalized_value(self, value_normalized, p_min, p_max, name=None, normalized=None):
        """Returns the denormalized value.

        Parameters
        ----------
        value_normalized : float
        p_min : float
        p_max : float
        name : str, optional
            Only needed when, normalized is not given.
        normalized : {None, 'log', 'lin', ''}, optional
            If None, normalized is looked up before denormalizing.

        Returns
        -------
        value_denormalized : float
        """
        if normalized is None:
            if self.normalize and (p_min != -np.inf) and (p_max != np.inf):
                if name in self.list_normalize_log:
                    normalized = "log"
                else:
                    normalized = "lin"
            else:
                normalized = ""

        if normalized == "lin":
            return p_min + value_normalized * (p_max - p_min)
        elif normalized == "log":
            return (np.float_power(10, value_normalized) - p_min) * (p_max - p_min) + p_min
        else:
            return value_normalized

    def set_normalized_parameters(self, values_normalized):
        """Saves the parameters from the optimize to self.paras_to_optimize, self.paras_to_optimize_per_line and self.mcard.

        If necessary it denormalizes the parameters before doing so.

        Parameters
        ----------
        values_normalized : np.array
        """
        index_start = len(self.paras_to_optimize)
        # Write back the values to paras_to_optimize
        for i_para, value in enumerate(values_normalized[0:index_start]):
            para = self.paras_to_optimize.paras[i_para]
            para.value = self._get_denormalized_value(value, para.min, para.max, name=para.name)
            self.paras_to_optimize.set(para)

        # also take over the parameters per line
        for i_line, composition in enumerate(self.paras_to_optimize_per_line):
            index_end = index_start + len(composition)
            for i_para, value in enumerate(values_normalized[index_start:index_end]):
                para = composition.paras[i_para]
                para.value = self._get_denormalized_value(value, para.min, para.max, name=para.name)
                self.paras_to_optimize_per_line[i_line].set(para)

            index_start = index_end

        self.mcard.set(self.paras_to_optimize)

    def ensure_input_correct(self):
        """Ensures that the user-supplied dut views hold the correct column names in their data.

        Overwrite this method, if you need access to all duts in your method!

        """
        for dut in self.relevant_duts:
            for key in dut.data:
                if self.validate_key(key):
                    try:
                        self.ensure_input_correct_per_dataframe(dut.data[key], dut=dut, key=key)
                    except:
                        raise IOError(
                            "A required column was missing in the data frame with the key "
                            + key
                            + ". Available columns: "
                            + str(list(dut.data[key].columns))
                        )  # from err

    def ensure_input_correct_per_dataframe(self, dataframe, dut=None, key=None):
        """
        Parameters
        ----------
        dataframe : DMT.core.DataFrame
            Dataframe to ensure columns
        dut : :class:`~DMT.core.dut_view.DutView`, optional
            The corresponding dut (if dut parameters are needed)
        key : string, optional
            The corresponding key (if ambient temperature is needed)

        Raises
        ------
        KeyError
            If a needed column is not in the frame.
        """
        raise NotImplementedError()

    def init_data_reference(self):
        """This function needs to init self.reference_data = [{'x':x_values, 'y':y_values}] from duts present in self.lib

        Overwrite this method, if you need access to all duts in your method!

        The attributes self.reference_data is a list of dicts.
        Each element of the list represents one line with its x_values and y_values.
        Additional keys can be added, see the x_step_cjc example, where the temperature T of each line has been added.
        """
        for dut in self.relevant_duts:
            for key in dut.data:
                if self.validate_key(key):
                    self.init_data_reference_per_dataframe(
                        dut.data[key], dut.get_key_temperature(key), dut=dut, key=key
                    )

    def init_data_reference_per_dataframe(self, dataframe, t_meas, dut=None, key=None):
        """This function needs to append lines to self.reference_data = [{'x':x_values, 'y':y_values}] from each dataframe in a dut.

        Per default overwrite this method since, generally the extraction steps create one or multiple lines from one dataframe independent of other frames.

        The attributes self.reference_data is a list of dicts.
        Each element of the list represents one line with its x_values and y_values.
        Additional keys can be added, see the x_step_cjc example, where the temperature T of each line has been added.

        Parameters
        ----------
        dataframe : DMT.core.DataFrame
            Dataframe from which reference data can be obtained.
        t_meas : float
            Measurement ambient temperature (obtained from key)
        dut : :class:`~DMT.core.dut_view.DutView`, optional
            The corresponding dut (if dut parameters are needed)
        key : string, optional
            The corresponding key
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_tex(self):
        """Return a tex Representation of the Model that is beeing fitted. This can then be displayed in the UI."""

    def get_tex_docu(self):
        """Returns the tex equation from get_tex a little better suited for the documentation. hmhmhm"""
        tex = self.get_tex()
        tex = tex.replace("$", "")
        tex = tex.replace("\\\\", "\\\\\n")
        tex = tex.replace(" = ", " &= ")
        tex = tex.replace(" \\approx ", "  &\\approx ")
        return tex

    def get_bibtex_entry(self):
        """Return a valid bibtex entry that may be used in the get_tex command. Optional."""
        return None

    def get_description(self):
        """Return a tex description of this XStep. Used for generating the documentation. If not implemented, there is no description for this XStep in the documentation."""
        return None

    @abc.abstractmethod
    def fit(self, data_model: Dict, paras_model: McParameterCollection, dut=None):
        """This function needs to return y-data that corresponds to the reference y-data.

        This function is called several times at each iteration.

        If a DutView is used as a reference device, it is recommended to not to perform the actual simulation inside this function.
        Then this function should only read out the simulation results and postprocess them to create the y-data.
        The actual computation is performed in parallel by simulation the DutView with the user-supplied Sweep object.
        See the calc_all() function.
        This saves simulation time, since it allows parallel computing.
        To access the data of the simulated dut, it is given as a additional parameter.

        If a ModelEquation is used for the extraction, the computation of the y-parameters should be inside this function.
        In this case the simulation speed is not critical. The parameters are then given inside of the parameters dictionary.

        Parameters
        ----------
        data_model : {'x' : ndarray, 'y' : ndarray, 'y_ref' : ndarray}
            Data for the model to calculate.
        paras_model : :class:`~DMT.core.mc_parameter.McParameterCollection`
            Parameters of the model to calculate. Can bei either a full modelcard or only a McParameterCollection.

        Returns
        --------
        y : [np.ndarray()]
            y-data that corresponds the the reference-lines in self.reference_data['y']
        """

    @abc.abstractmethod
    def set_initial_guess(self, reference_data):
        """This methods should set an initial guess for the optimization parameters from the available reference_data array.
        If no initial guess is set for a parameter, the value for the initial guess is taken form the modelcard.
        For steps which use a simulation of a DutCircuit, here the sweep should be defined, too.
        """

    def set_guess_bounds(self):
        """Overwrite this method to set bounds of parameters dependent on the extraction region bounds.
        Make sure to only overwrite the min and max of each parameter and no the value to preserve already extracted values.
        """

    def extract(self):
        """Perform a parameter extraction. This algorithm should be valid for ALL smallest common XSteps. Compositional XSteps will get another algorithm."""
        self.inited_data = False  # recollect the data to allow on the fly deembeding
        self.init()
        self.set_guess_bounds()

        self.optimize()  # perform the actual optimization
        logging.info("Extraction of the step %s finished.", self.name)

    def init(self):
        if not self.inited_data:
            self.init_data()

        self.init_data_model()
        self.init_ynormalizer()

        if self.interpolate:
            self.apply_interpolation()

    def init_ynormalizer(self):
        # initialize an IYNorm object, which can then be used to normalize y_values
        # normalizer now also acts inside of the xbounds by using data_model['y_ref'].
        self.y_normalizer = self.iynorm(np.concatenate([data["y"] for data in self.data_reference]))

    @property
    def x_bounds(self):
        if not self._x_bounds:  #  as long they were not set, just admit that..
            return []

        if len(self._x_bounds) != len(self.data_reference):
            raise IOError(
                "DMT -> XStep: The number of XBounds objects does not match the number of lines in data reference."
            )

        return self._x_bounds

    @x_bounds.setter
    def x_bounds(self, bounds_list):
        """This method initializes one object for each line in the reference data with the user supplied bounds_class."""
        self._x_bounds = []
        if bounds_list is None:
            for line in self.data_reference:
                if self.bounds_class == XBounds:
                    self._x_bounds.append(self.bounds_class(line["x"]))
                elif self.bounds_class == YBounds:
                    self._x_bounds.append(self.bounds_class(line["y"]))
                elif self.bounds_class == XYBounds:
                    self._x_bounds.append(self.bounds_class(line["x"], line["y"]))
        else:
            for bounds in bounds_list:
                if isinstance(bounds, Bounds):
                    self._x_bounds.append(bounds)
                else:
                    if self.bounds_class == XYBounds:
                        try:
                            self._x_bounds.append(
                                self.bounds_class(
                                    xdata=(bounds[0][0], bounds[1][0]),
                                    ydata=(bounds[0][1], bounds[1][1]),
                                )
                            )
                        except TypeError as err:
                            raise TypeError(
                                "XStep: Failed to init bounds. For XYBounds you need to pass a tuple of dimension((2),(2))."
                            ) from err
                    else:
                        self._x_bounds.append(self.bounds_class(bounds))

        try:
            logging.info(
                "Set the bounds of the step %s to %s.",
                self.name,
                " ".join([f"{bound:s}" for bound in self._x_bounds]),
            )

            str_temp = "[" + ", ".join([f"{bound:g}" for bound in self._x_bounds]) + " ]"
            print("To create the bounds in the script use:\nstep.x_bounds = " + str_temp)
        except TypeError:
            pass  # catches nan values

    @property
    def op_selector_bounds(self):
        if not self._op_selector_bounds:  #  as long they were not set, just admit that..
            return []

        return self._op_selector_bounds

    @op_selector_bounds.setter
    def op_selector_bounds(self, bounds_list):
        """This method initializes the bounds for op_selection widget."""
        self._op_selector_bounds = None
        if bounds_list is None:
            self._op_selector_bounds = XBounds(self.op_selector_x)

    def get_bool_array(self, line_ref, bounds):
        """Return a boolean array, where True means that the value in line_ref is inside the bounds.

        Parameters
        ----------
        line_ref : {}
            A dictionarray of a line that has at least the keys "x" and "y"
        bounds : DMT.extraction.XBounds, YBounds or XYBounds
            The boundaries that shall be used to determine which values in bool_array are true

        Returns
        -------
        np.array()
            An array that has "True" where the value in "x" or "y", depending on the type of bounds, is inside the bounds.
        """
        if self.bounds_class == XBounds:
            bool_array = (line_ref["x"] >= bounds.low) & (line_ref["x"] <= bounds.high)
        elif self.bounds_class == YBounds:
            bool_array = (line_ref["y"] >= bounds.low) & (line_ref["y"] <= bounds.high)
        elif self.bounds_class == XYBounds:
            bool_array = (
                (line_ref["x"] >= bounds.low[0])
                & (line_ref["x"] <= bounds.high[0])
                & (line_ref["y"] >= bounds.low[1])
                & (line_ref["y"] <= bounds.high[1])
            )
        else:
            raise IOError("Unkown Bounds class")

        return bool_array

    def init_data_model(self):
        """This method inits the data_model['x'] values according to the self.x_bounds and the data_reference.
        If the self.x_bounds do not match with available x-data, they are adjusted to lie on the nearest availabel x-point.

        """
        # apply bounds to the extraction dut by modifying the sweep
        # if self.sweep is not None:
        #     return
        # raise IOError('DMT -> x_step -> init_data_model(): Only LIST type sweep are supported to ensure matching simulation and measurement data.')

        # force calculation of bounds with new reference data, if x_bounds are empty
        if not self._x_bounds:
            self.x_bounds = None

        # force calculation of bounds with new reference data, if x_bounds are empty
        if not self._op_selector_bounds and self.op_selector:
            self.op_selector_bounds = None

        elif len(self._x_bounds) != len(self.data_reference):
            raise IOError(
                "DMT -> XStep: The number of XBounds objects does not match the number of lines in data reference. (expected {} found {})".format(
                    len(self.data_reference), len(self._x_bounds)
                )
            )

        # adjust the reference data to match the bounds
        self.data_model = []
        for line_ref, x_bounds in zip(self.data_reference, self.x_bounds):
            line_model = {}

            # Step1: get a boolean index array to find out which values are inside the user selected bounds
            bool_array = self.get_bool_array(line_ref, x_bounds)

            # update the model data with the new bounds by coping all the entries. Except, 'y' which is copied to 'y_ref' and the shape is set to 'y'.
            for key, value in line_ref.items():
                if key == "y":
                    line_model["y_ref"] = copy.deepcopy(value[bool_array])
                    line_model["y"] = np.zeros_like(value[bool_array])
                    continue

                try:
                    line_model[key] = copy.deepcopy(value[bool_array])
                except (TypeError, IndexError):
                    # it is a scalar value
                    line_model[key] = copy.deepcopy(value)

            self.data_model.append(line_model)

        logging.info("Applied the bounds the step %s to its data.", self.name)

    def save(self, save_dir):
        """Save the xstep object without the dut_ref, which shall be saved separately."""
        with open(save_dir + ".p", "wb") as handle:
            cpickle.dump(self, handle)

    def __getstate__(self):
        """Return state values to be pickled. Implemented according `to <https://www.ibm.com/developerworks/library/l-pypers/index.html>`_ .
        Notes
        -----
        ..todo:
            iterate through all properties and throw away the HDFStore objects.
        """
        self_dict = copy.copy(self.__dict__)

        list_to_del = [
            "lib",
            "dut_ext",
            "process",
            "finished",
            "mcardChanged",
            "xfunc",
            "objectNameChanged",
            "destroyed",
        ]

        for to_del in list_to_del:
            if to_del in self_dict:
                del self_dict[to_del]

        return self_dict

    def fit_function(self, xdata, *args):
        """This function is passed to curve_fit and is a little abused here, see text below.

        The curve_fit function is passed to scipy alongside with the jacobian function. Scipy will call these functions in an alternating way,
        in order to get the current function value and the jacobian.
        However this would prevent the usage of parallel computing, hence all calculations are performed inside fit_function.
        self.jacobian just returns calculation results that have already been calculated in fit_function.

        This approach also allows easy implementation of multi-dimensional fits.

        Parameters
        ----------
        xdata : np.ndarray
            The argument of the fit_function, scipy.curve_fit wants to calculate.
        *args : list-like
            These represent the current parameter values that curve_fit is interested in. They are expanded by the full local modelcard.

        Returns
        -------
        f_0 : np.ndarray
            The current value of the model function, possibly normalized.
        """
        # take over the global parameters
        self.set_normalized_parameters(args)

        # try:
        self.data_model = self.calc_all(
            xdata, self.mcard, jac=True, reinit=False, n_optimize=len(self.paras_to_optimize)
        )  # perform ALL calculations, also for the jacobian, but do not reinit
        # pylint: disable=try-except-raise
        # except Exception as err:
        #     raise

        self.process.emit()  # the gui can catch this signal to display optimization progress
        if self.stopped:  # user has requested a stop
            self.stopped = False
            raise Stopped

        if self.canceled:  # user has requested a cancel
            self.canceled = False
            raise Canceled

        f = np.concatenate([data["y"] for data in self.data_model])
        f = self.y_normalizer.normalize(f)
        # print(np.sum(f))
        return f

    def jacobian(self, xdata, *args):
        """This function returns the jacobian self.jac and possibly normalizes it. This function is only a helper to work with the curve_fit interface."""
        try:
            return self.jac.reshape(len(xdata), len(args))
        except ValueError as err:
            raise ValueError(
                "In step with name "
                + self.name
                + ": Failed to reshape jacobian during optimization. Likely, this is a real bug that you should report."
            ) from err

    def variate_parameter(self, parameter):
        """Changes the parameter by a small delta value.

        First tries to add the value, if a ValueTooLargeError is risen, the delta is subtracted from the value.

        Parameters
        ----------
        parameter : :class:`~DMT.core.mc_parameter.McParameter`

        Returns
        -------
        parameter : :class:`~DMT.core.mc_parameter.McParameter`
            parameter with new, variated value.
        delta_value : float
            Change of the parameter value.
        """
        delta = float(1e-3)  # delta used to numerically calculate the jacobian
        value_old = self._get_normalized_value(
            parameter.value, parameter.min, parameter.max, name=parameter.name
        )

        if value_old == 0.0:
            value_new = delta
        else:
            value_new = value_old * (1 + delta)
        try:
            parameter.value = self._get_denormalized_value(
                value_new, parameter.min, parameter.max, name=parameter.name
            )
        except ValueTooLargeError:
            # parameter was at upper boundary, try negative change
            if value_old == 0.0:
                value_new = -delta
            else:
                value_new = value_old * (1 - delta)

            parameter.value = self._get_denormalized_value(
                value_new, parameter.min, parameter.max, name=parameter.name
            )

        if value_old == value_new:
            raise ValueAtBoundsError(
                "DMT->XStep: The parameter "
                + parameter.name
                + " is very close to its boundaries and the boundaries are in the range of the floating point eps. This combination results in no visible parameter change."
            )

        return parameter, value_new - value_old

    def calc_all(self, xdata, paras_model, jac=True, reinit=True, n_optimize=None):
        """This method needs to start the calculation of the function to be optimized self.f_0 and its jacobian self.jac .

        Calculating the jacobian here allows to use DMT's parallel computing features, which might be relevant for circuit or TCAD simulations.

        This function is called inside fit_function.

        Parameters
        ----------
        xdata : np.ndarray
            The argument of the fit_function, scipy.curve_fit wants to calculate.
        paras_model : :class:`~DMT.core.mc_parameter.McParameterCollection`
            Parameters of the model to calculate. Can bei either a full modelcard or only a McParameterCollection.
        jac   : {True, False}, optional
            This boolean controls wheather or not the jacobian is computed.
        reinit : Boolean
            What is this?
        n_optimize : integer
            The number of parameters to optimize. Not really needed but for memoization in XVerify.

        Returns
        -------
        self.data_model : dict{}
            This is only returned in order to enable memoization. It is actually not really needed for anything else.

        """
        # for debug
        time1 = time.time()

        if reinit:  # do it always for the plots, it is set off for optimizing
            self.inited_data = False
            self.init()

        # prepare output:
        n_row = sum([len(line["x"]) for line in self.data_model])
        # one column for f, and one for each parameter to be optimized
        n_col = (
            1
            + len(self.paras_to_optimize)
            + len(self.data_reference) * len(self.to_optimize_per_line)
        )
        data = np.zeros((n_row, n_col))

        # if self.model is None:
        if self.DutCircuitClass is not None:  # model also needed for x_verify for control plots...
            # for dut optimization the parameters need to be written back into self.mcard

            # create a list of duts and simulate them with DMT
            self.duts = []
            for line in self.data_reference:
                dut_f = self.get_dut(line, paras_model)
                if self.write_table_model:
                    df = DataFrame(line)
                    dut_f.list_copy.append(df)

                self.duts.append(dut_f)

            if jac:
                for para in self.paras_to_optimize:
                    old_value = para.value
                    para, para_delta = self.variate_parameter(para)
                    paras_model.set(para)  # small change in this direction

                    for line in self.data_reference:
                        dut_jac = self.get_dut(line, paras_model)
                        self.duts.append(dut_jac)

                    para.value = old_value
                    paras_model.set(para)  # small change in this direction

            # scale the modelcards now
            if self.technology is not None:  # no technology -> no scaling
                for dut in self.duts:
                    dut.scale_modelcard()

            # add the duts into the simulation queue
            if len(self.duts) % len(self.data_reference) != 0:
                raise IOError("This makes no sense.")

            index_duts = 0
            self.sim_con.clear_sim_list()  # reset the sim_list
            for _ in range(int(len(self.duts) / len(self.data_reference))):
                for line in self.data_reference:
                    self.sim_con.append_simulation(self.duts[index_duts], line["sweep"])
                    index_duts += 1

            time_run_start = time.time()
            self.sim_con.run_and_read(force=False)  # run the simulation
            print("run, read and save took:" + str(time.time() - time_run_start))

            # write back the simulation results using the user-supplied function
            time_fit_start = time.time()
            try:
                result = self.fit_wrapper(self.data_model, paras_model, duts=self.duts)
                data[:, 0] = result
            except ValueError as err:
                print(f"error in {self.name}: {err}")
            data_0_norm = self.y_normalizer.normalize(data[:, 0])
            print("fit took:" + str(time.time() - time_fit_start))

            if jac:  # oh man :(, but must keep structure same for both parts!
                index = 1
                n_lines = len(self.data_model)
                # jacobian for parameters globally
                for i, para in enumerate(self.paras_to_optimize.paras):
                    old_value = para.value
                    para, para_delta = self.variate_parameter(para)

                    paras_model.set(para)  # small change in this direction
                    # df           = (f(x+-h)                                                           - f(x)       / (x+-h                        -x)
                    data[:, index] = (
                        self.y_normalizer.normalize(
                            self.fit_wrapper(
                                self.data_model,
                                paras_model,
                                self.duts[(i + 1) * n_lines : (i + 2) * n_lines],
                            )
                        )
                        - data_0_norm
                    ) / (para_delta)
                    index += 1
                    para.value = old_value
                    paras_model.set(para)

        else:
            # same as above, however for a Model-Equation we directly compute the data.
            # and the parameters are written back into self.mcard after the optimization
            data[:, 0] = self.fit_wrapper(self.data_model, paras_model)
            data_0_norm = self.y_normalizer.normalize(data[:, 0])

            index = 1
            if jac:
                # jacobian for parameters globally
                for para in self.paras_to_optimize.paras:
                    old_value = para.value
                    para, para_delta = self.variate_parameter(para)

                    paras_model.set(para)  # small change in this direction
                    # df           = (f(x+-h)                                                           - f(x)       / (x+-h                        -x)
                    data[:, index] = (
                        self.y_normalizer.normalize(self.fit_wrapper(self.data_model, paras_model))
                        - data_0_norm
                    ) / (para_delta)
                    index += 1
                    para.value = old_value
                    paras_model.set(para)

                # jacobian for parameters per line
                for composition in self.paras_to_optimize_per_line:
                    for para in composition.paras:
                        old_value = para.value
                        para, para_delta = self.variate_parameter(para)

                        # df           = (f(x+-h)                                                           - f(x)       / (x+-h                        -x)
                        composition.set(para)  # small change in this direction
                        data[:, index] = (
                            self.y_normalizer.normalize(
                                self.fit_wrapper(self.data_model, paras_model)
                            )
                            - data_0_norm
                        ) / (para_delta)
                        index += 1
                        para.value = old_value
                        composition.set(para)

        # make sure that the data in data_model matches f(*arg) where the args (not the case for jacobian)
        index = 0
        for line in self.data_model:
            n_values = len(
                line["x"]
            )  # each line has as many x_values as y_values, so we can just take them here
            line["y"] = data[index : index + n_values, 0]
            index += n_values

        # create the jacobian, as needed for the optimizer, from the simulated data
        if jac:
            self.jac = data[:, 1:]
            # check for Nans Infs in jacobian
            for i in range(self.jac.shape[1]):
                if np.isnan(self.jac[:, i]).any() or np.isinf(self.jac[:, i]).any():
                    raise NanInfError

        delta_time = time.time() - time1
        # print('calc_all took: ' + str(delta_time))
        self.sum_time += delta_time
        return self.data_model  # just to enable memoization

    def fit_wrapper(self, data_model, paras_model, duts=None):
        """Dummy function to wrap the user supplied fit function. This allows a more easy to get interface.

        Parameters
        ----------
        data_model : {'x':np.ndarray,'y':np.ndarray,'y_ref':np.ndarray}
            Data for the model to calculate.
        paras_model : :class:`~DMT.core.mc_parameter.McParameterCollection`
            Parameters of the model to calculate. Can bei either a full modelcard or only a McParameterCollection.

        Returns
        -------
        np.ndarray
            The return on the fit function.
        """
        # remember old_value of op_selector_para
        if self.op_selector:
            old_val = self.mcard[self.op_selector_para].value

        # if self.model is None: # x_verify can have a model for verification of models...
        if self.DutCircuitClass is not None:
            for index, line in enumerate(self.data_model):
                self.data_model[index] = self.sort_line(
                    self.fit(line, paras_model, dut=duts[index])
                )

            for line_ref, line_model, x_bounds in zip(
                self.data_reference, self.data_model, self.x_bounds
            ):
                # Step1: get a boolean index array to find out which values are inside the user selected bounds
                bool_array = self.get_bool_array(line_ref, x_bounds)

                # update the model data with the new bounds by coping all the entries. Except, 'y' which is copied to 'y_ref' and the shape is set to 'y'.
                for key, value in line_model.items():
                    try:
                        line_model[key] = line_model[key][bool_array]
                    except IndexError:
                        pass  # catches y_ref
                    except TypeError:
                        pass  # catches scalar device attributes, sweep and so on

        else:
            for index in range(len(self.data_model)):
                # add paras per line to modelcard
                # todo: not nice Code I think
                # This code may not change the value of self.op_selector_para
                try:
                    composition = self.paras_to_optimize_per_line[index]
                    for para in composition.paras:
                        try:
                            paras_model.set_values({para.name: para.value}, force=True)
                        except KeyError:
                            # dangerous, id(para) in to_optimize_per_line will be same as in mcard
                            paras_model.add(para)

                except IndexError:
                    pass

                try:
                    self.data_model[index] = self.fit(self.data_model[index], paras_model)
                except IndexError:
                    self.data_model[index] = self.data_model[index]

            # remove paras per line from modelcard
            try:
                composition = self.paras_to_optimize_per_line[index]
                for para in composition.paras:
                    if para.name != self.op_selector_para:
                        paras_model.remove(para)
            except IndexError:
                pass

        # reset op_selector_para
        if self.op_selector:
            self.mcard.set_values({self.op_selector_para: old_val})

        for line in self.data_model:
            if line is None:
                raise IOError(
                    'DMT -> XStep: After calling "fit", nothing was returned. Maybe you forgot to return a line object.'
                )
            if np.isnan(line["y"]).any():
                logging.debug(
                    "The fit_wrapper was called with the model_parameters:\n%s",
                    paras_model.print_parameters(line_break=";"),
                )
                logging.debug(
                    "In this step the following parameters are to be optimized:\n%s",
                    paras_model.get(self.paras_to_optimize).print_parameters(line_break=";"),
                )
                logging.debug(
                    "The Nans or infs are obtained at the x-values:\n%s",
                    line["x"][np.isnan(line["y"])],
                )
                raise NanInfError("This error occurred in the step with the name " + self.name)

        # we allocate before we fill, speeding up the code significantly
        n_data = sum([len(line["x"]) for line in self.data_model])
        result = np.zeros(n_data)
        index = 0
        for line in self.data_model:
            try:
                result[index : index + len(line["x"])] = line["y"]
                index += len(line["x"])
            except ValueError:
                dummy = 1

        return result

    def add_plot_method(self, func):
        """Binds the function to self. Func has the method signature func(self) and needs to return a DMT.Plot object

        Parameters
        ----------
        func : callable
            A callable object with signature func(self) that returns a Plot object. Will be binded to self.
        """
        setattr(self, func.__name__, func.__get__(self, self.__class__))
        # not needed anymore?
        # self._plot_methods.append(getattr(self, func.__name__))

    def apply_interpolation(
        self,
        spline_order=None,
        points_out_of_bounds=None,
        nr_points=None,
        smoothing_factor=None,
        weights=None,
    ):
        """Interpolates each line of the self.data_model['y_ref'] using scipy.interpolate.UnivariateSpline.

        Can also be used to smooth the data using the smoothing_factor and the weights can be used to weight the spline. This is only possible if in data_model only 'x', 'y', 'y_ref' and scalar values are present.
        All given parameters which are not None will be saved to the local correspondants. If they are None, they are replaced by the local correspondants.

        Parameters
        ----------
        spline_order : int, optional
            scipy: Degree of the smoothing spline. Must be <= 5. Default is k=3, a cubic spline.
        points_out_of_bounds : int, optional
            Defines how many points of each line outside of the boundaries should be included. Default is 1
        nr_points : int, optional
            Number of points to interpolate using numpy.linspace. Default is 50.
        smoothing_factor : float, optional
            scipy: If None (default), s = len(w) which should be a good value if 1/w[i] is an estimate of the standard deviation of y[i]. If 0, spline will interpolate through all data points.
        weights : array_like, optional
            scipy: Weights for spline fitting. Must be positive. If None (default), weights are all equal.
        """
        if spline_order is None:
            spline_order = self.spline_order
        else:
            self.spline_order = spline_order

        if points_out_of_bounds is None:
            points_out_of_bounds = self.points_out_of_bounds
        else:
            self.points_out_of_bounds = points_out_of_bounds

        if nr_points is None:
            nr_points = self.spline_nr_points
        else:
            self.spline_nr_points = nr_points

        if smoothing_factor is None:
            smoothing_factor = self.smoothing_factor
        else:
            self.smoothing_factor = smoothing_factor

        if weights is None:
            weights = self.spline_weights
        else:
            self.spline_weights = weights

        for line, line_ref, label in zip(self.data_model, self.data_reference, self.labels):
            # if self.bounds_class == YBounds: # i dont know how to do it there, give me an example...
            #     raise NotImplementedError() # but i think it should work, if the xdata is still somehow sorted....

            x = line["x"]
            line["x_orig"] = copy.deepcopy(line["x"])
            line["y_orig"] = copy.deepcopy(line["y_ref"])

            # add points_out_of_bounds from data_reference
            i_x_min = find_nearest_index(x[0], line_ref["x"])
            i_x_max = find_nearest_index(x[-1], line_ref["x"])

            # sorting not needed since it is already done at the bounds
            # just check order
            if i_x_min > i_x_max:
                i_x_max, i_x_min = i_x_min, i_x_max

            if i_x_min > points_out_of_bounds:
                i_x_min = i_x_min - points_out_of_bounds
            else:
                i_x_min = 0

            if i_x_max < len(line_ref["x"]) - points_out_of_bounds - 1:
                i_x_max = i_x_max + points_out_of_bounds + 1
            else:
                i_x_max = len(line_ref["x"]) - 1

            x_extra = line_ref["x"][i_x_min:i_x_max]
            y_extra = line_ref["y"][i_x_min:i_x_max]

            # interpolate
            try:
                obj_spline_y = sciint.UnivariateSpline(
                    x_extra,
                    y_extra,
                    w=weights,
                    k=spline_order,
                    s=smoothing_factor,
                )
            except OSError as err:
                raise OSError(
                    err.args[0]
                    + "\nThis error occurred for the line "
                    + label
                    + ". Most propably the bounds were too thin."
                ) from err

            # linspace, this time ascending...
            x_new = np.linspace(np.min(x), np.max(x), num=nr_points, dtype="float64")

            # update the model data with the new points. Note that numpy array slicing is upper bounds exclusive.
            # by coping all the entries. Except, 'y' which only gets the shape.
            # create new y data

            for col in line:
                if col == "x":
                    line[col] = x_new
                elif col == "y_ref":
                    line[col] = obj_spline_y(x_new)
                elif col == "y":
                    line[col] = np.zeros(x_new.shape)
                elif col[-5:] == "_orig":
                    continue
                else:
                    try:
                        col_extra = line_ref[col][i_x_min:i_x_max]
                    except (TypeError, IndexError):
                        # it is a scalar value, do nothing
                        continue

                    if weights is not None:  # or smoothing_factor != 0:
                        raise IOError(
                            "Smoothing and weighting is not possible if additional data is in data_model! For this XStep "
                            + col
                            + " is an additional column!"
                        )

                    # interpolate it
                    obj_spline = sciint.UnivariateSpline(
                        x_extra,
                        col_extra,
                        w=None,  # here no weighting
                        k=spline_order,
                        s=0,  # here no smoothing
                    )
                    line[col] = obj_spline(x_new)

        logging.info("The extraction step %s applied interpolation to its data.", self.name)

    def get_dut(self, line, paras_model):
        """
        Parameters
        ----------
        line : dict{key:np.ndarray()}
            Line object that contains information of the line to be simulated.
        paras_model: dict()
            The current modelcard parameters as a dict

        Returns
        -------
        dut : subclass of :class:`~DMT.core.dut_view.DutView`
            A DutView object that can be simulated using DMT's SimCon class.
        """
        raise NotImplementedError(
            "get_dut needs to be implemented by XSteps that make use of simulatable DuTs."
        )
