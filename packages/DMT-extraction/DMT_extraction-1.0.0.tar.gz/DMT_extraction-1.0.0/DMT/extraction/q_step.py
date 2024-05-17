""" File contains only class QStep, see below.

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
import scipy.optimize as sciopt
import numpy as np
import abc

from DMT.core import McParameter, McParameterCollection

from DMT.extraction import XStep
from DMT.exceptions import Stopped, Canceled


class QStep(XStep):
    """Subclass of XStep. QSteps (Q for Quantity) steps are a special case of XSteps.
    They do not extract model parameters like XSteps, but bias dependent electrical quantities from measured or simulated data.

    | A Bias dependent PoA Analysis is an example for a QStep.
    | Subclasses of this class need to implement set_initial_guess_line and write_back_results in addition to the usual XStep abstract methods.
    | See the XPoa class for an example of this class.

    Parameters
    ----------
    same as XStep.

    Attributes
    ----------
    same as XStep except:
    para_compositions : [McParameterCollection]
        Holds artificial model parameters for each measured operating point. This allows to use the powerfull XStep infrastructure without changing much.
        For an PoA Analysis at 10 operating points, there would be 10 McParameterCollections, each with the area and perimeter component that is to be extracted.
        Numerically this is porbably not the fastest solution, but who cares.
    """

    def __init__(self, *args, **kwargs):
        super(QStep, self).__init__(*args, **kwargs)
        self.para_compositions = []  # one composition per line is beeing optimized

    def set_initial_guess(self, data_reference):
        """In contrast to XStep set_initial_guess, this method needs to set an initial guess for each line and init the parameter arrays."""
        # for each line, create one McParameter Composition
        for line in data_reference:
            composition = McParameterCollection()
            for para in self.paras_possible:
                para = McParameter(para.name, value=0)
                composition.add(para)

            self.para_compositions.append(composition)

        # for each line, get an initial guess for the possible paras
        for composition, line in zip(self.para_compositions, data_reference):
            self.set_initial_guess_line(composition, line)

    @abc.abstractmethod
    def set_initial_guess_line(self, composition, line):
        """This method need to set an initial guess for parameters in composition for each line."""

    def optimize(self):
        """Slightly changed compared to XStep. Here we fit all parameters for each line, simultaneously. Jacoby currently not implemented."""
        # transform a possibly multidimension problem into a one-dimensional one
        x = np.concatenate([data["x"] for data in self.data_model])
        y = np.concatenate([data["y_ref"] for data in self.data_model])
        paras_optimized = None

        # normalize the parameters
        self.paras_to_optimize = self.mcard.get(self.paras_to_optimize)
        if self.normalize:
            for composition in self.para_compositions:
                composition.normalize()

        # form arrays for p0 and the bounds from the McParameterCollections that may be passed to the optimizer.
        p0, bounds_lower, bounds_upper = [], [], []
        for composition in self.para_compositions:
            for para in composition:
                p0.append(para.value_normalized[0])
                bounds_lower.append(para.min)
                bounds_upper.append(para.max)

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
                    # jac    = self.jacobian,
                )

            else:
                (paras_optimized, _paras_covariance) = sciopt.curve_fit(
                    self.fit_function,
                    x,
                    self.y_normalizer.normalize(y),
                    p0=p0,
                    bounds=(bounds_lower, bounds_upper),
                    method=self.fit_method,
                    ftol=self.f_tol,
                    maxfev=self.n_step_max,
                    # jac    = self.jacobian,
                )

        except (Stopped, Canceled) as e:
            return  # stopped by gui, do not write modelcard!
        except RuntimeError as e:
            print(e)

        # write back the values
        try:
            n = 0
            for composition in self.para_compositions:
                for para in composition:
                    para.value = [paras_optimized[n]]
                    n += 1
        except TypeError:
            for composition in self.para_compositions:
                composition.denormalize()
            return

        self.write_back_results()
        self.mcardChanged.emit()
        self.finished.emit()

    def fit_function(self, xdata, *args):
        """Very similar to XStep. Here we need to write args back into the McParameterCompositon in exactly the same way as we have passed them in self.optimize()"""
        n = 0
        for composition in self.para_compositions:
            for para in composition:
                para.value = [args[n]]
                n += 1

        return super().fit_function(xdata, args)

    def calc_all(self, xdata, paras_model, jac=True, reinit=False):
        """Much simpler than for XStep. No DutTcad support and no Jacobian support."""
        self.init()
        self.set_bounds()

        data = []
        data.append(self.fit_wrapper(self.data_model, self.para_compositions))

        # make sure that the data in data_model matches f(*arg) where the args (not the case for jacobian)
        for line, y_model in zip(self.data_model, data[0]):
            line["y"] = y_model

        return self.data_model

    @abc.abstractmethod
    def fit(self, data_model, compositions):
        """This needs to be implemented for subclasses.
        | The method shall calculate the corresponding y-data for each line in data_model.
        | The ModelParameters for each line are to be calculated using the McParameterCollections in compositions.
        | See XPoa for an implementation example. It is simpler than it sounds...
        """
