"""  Allows to extract multiple steps at once. All steps are fit at once...

Author: Mario Krattenmacher | Mario.Krattenmacher@semimod.de
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
import logging
import time
import numpy as np
import scipy.optimize as sciopt

from DMT.extraction import XStep, plot
from DMT.exceptions import Stopped, Canceled, NanInfError, ValueAtBoundsError, ParaExistsError


class MXStep(XStep):
    """Multiple extraction step"""

    def __init__(self, name, mcard, **kwargs):
        self._mcard = mcard
        self._paras_to_optimize_per_line = []
        self._steps = []

        # duck type
        depend_fnc = lambda x: x  # dummy function
        depend_fnc.parameters = mcard.name  # all parameters as attribute
        self.model_function_info = {"depends": (depend_fnc,)}  # add to info_dict as dependent

        # init the super class :/
        super().__init__(name, mcard, None, {}, **kwargs)
        self.set_para_inactive(self.paras_to_optimize)  # set all parameters to inactive!
        self.index_main_plot = 0

    def add(self, xstep, has_main_plot=False):
        """Adding a step the the multi-step"""
        self._steps.append(xstep)

        # change parameters to optimize
        for para in xstep.paras_to_optimize:
            self.set_para_active(para)

        xstep._mcard = self.mcard
        # now all steps in mxstep have the same mcard object! Does not work in all cases, as soon as one parameter is changed, the parameter is copied again
        self.mcardChanged.connect(self.refresh_mcards)

        if has_main_plot:
            self.index_main_plot = len(self._steps) - 1
            self.main_plot = xstep.main_plot
            self.get_tex = xstep.get_tex

        for composition in xstep.paras_to_optimize_per_line:
            self._paras_to_optimize_per_line.append(composition)

    def refresh_mcards(self):
        for xstep in self._steps:
            xstep.mcard = self.mcard

    @property
    def mcard(self):
        return self._mcard

    @mcard.setter
    def mcard(self, mcard_new):
        self._mcard = mcard_new

        for xstep in self._steps:
            xstep.mcard = mcard_new

    @property
    def paras_to_optimize_per_line(self):
        return self._paras_to_optimize_per_line

    @paras_to_optimize_per_line.setter
    def paras_to_optimize_per_line(self, paras_to_optimize_per_line_new):
        self._paras_to_optimize_per_line = paras_to_optimize_per_line_new

        i_start = 0
        for xstep in self._steps:
            i_end = i_start + len(xstep.paras_to_optimize_per_line)
            xstep.paras_to_optimize_per_line = paras_to_optimize_per_line_new[i_start:i_end]
            i_start = i_end

    def set_normalized_parameters(self, values_normalized):
        super().set_normalized_parameters(values_normalized)

        i_start = 0
        for xstep in self._steps:
            i_end = i_start + len(xstep.paras_to_optimize_per_line)
            xstep.paras_to_optimize_per_line = self.paras_to_optimize_per_line[i_start:i_end]
            i_start = i_end

    def ensure_input_correct_per_dataframe(self, *_args, **_kwargs):
        pass

    def init_data_reference_per_dataframe(self, *_args, **_kwargs):
        pass

    def set_initial_guess(self, data_reference):
        """Find suitable initial guesses for (some of the) model parameters from the given reference data."""
        pass

    def extract(self):
        """Perform a parameter extraction. This algorithm should be valid for ALL smallest common XSteps. Compositional XSteps will get another algorithm."""
        for xstep in self._steps:
            xstep.init()
            xstep.set_guess_bounds()

        self.optimize()  # perform the actual optimization

        logging.info("Extraction of the MXStep %s finished.", self.name)

    def optimize(self):
        """Fit the model to the reference data."""
        # transform a possibly multidimension problem into a one-dimensional one
        x = np.empty(0)
        y = np.empty(0)

        for xstep in self._steps:
            for data in xstep.data_model:
                x = np.concatenate([x, data["x"]])
                y = np.concatenate([y, xstep.y_normalizer.normalize(data["y_ref"])])

        if x.size == 0:
            raise IOError("DMT -> XStep -> optimize: X data is empty.")
        if y.size == 0:
            raise IOError("DMT -> XStep -> optimize: Y data is empty.")

        # normalize the parameters
        p0, p_min, p_max = self.get_normalized_parameters()

        old_settings = np.seterr(all="warn")  # all numpy warnings etc are now raised warnings!
        paras_optimized = None
        try:
            if self.fit_method == "lm":
                (paras_optimized, _paras_covariance) = sciopt.curve_fit(
                    self.fit_function,
                    x,
                    y,
                    p0=p0,
                    method=self.fit_method,
                    ftol=self.f_tol,
                    maxfev=self.n_step_max,
                    # jac    = self.jacobian,
                )

            else:
                time1 = time.time()
                self.sum_time = 0.0
                (paras_optimized, _paras_covariance) = sciopt.curve_fit(
                    self.fit_function,
                    x,
                    y,
                    p0=p0,
                    bounds=(p_min, p_max),
                    method=self.fit_method,
                    ftol=self.f_tol,
                    maxfev=self.n_step_max,
                    # jac    = self.jacobian,
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

    def jacobian(self, xdata, *args):
        """This function returns the jacobian self.jac and possibly normalizes it. This function is only a helper to work with the curve_fit interface."""
        jac = np.empty(0)
        for xstep in self._steps:
            jac = np.concatenate([jac, xstep.jac])
        return self.jac.reshape(len(xdata), len(args))

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

        i_start = 0
        i_end = 0
        for xstep in self._steps:
            i_end = len(np.concatenate([data["x"] for data in xstep.data_model]))
            xstep.data_model = xstep.calc_all(
                xdata[i_start:i_end], self.mcard, jac=True, reinit=False
            )
            i_start = i_end

        self.process.emit()  # the gui can catch this signal to display optimization progress
        if self.stopped:  # user has requested a stop
            self.stopped = False
            raise Stopped

        if self.canceled:  # user has requested a cancel
            self.canceled = False
            raise Canceled

        f = np.empty(0)
        for xstep in self._steps:
            for data in xstep.data_model:
                f = np.concatenate([f, xstep.y_normalizer.normalize(data["y"])])
        return f

    def set_para_inactive(self, para):
        try:
            self.paras_to_optimize.remove(para)
        except KeyError:
            pass

        for xstep in self._steps:
            xstep.set_para_inactive(para)

    def set_para_active(self, para):
        try:
            self.paras_to_optimize.add(para)
        except ParaExistsError:
            pass

        for xstep in self._steps:
            xstep.set_para_active(para)

    def set_para_to_push(self, para):
        try:
            self.paras_to_push.add(para)
        except ParaExistsError:
            pass

        for xstep in self._steps:
            xstep.set_para_to_push(para)

    def remove_para_to_push(self, para):
        try:
            self.paras_to_push.remove(para)
        except KeyError:
            pass

        for xstep in self._steps:
            try:
                xstep.paras_to_push.remove(para)
            except KeyError:
                pass

    def model_function(self, *args, **kwargs):
        """Defining a model function to allow parameter grabbing"""
