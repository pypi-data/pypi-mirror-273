""" This XStep is used to extract resistances from I(V) data. It is explicitly made to be subclassed.
Input   : I(V) Data
Outpout : Resistance parameter with name as specified in the constructor.

Author: Markus Müller Markus.Mueller3@tu-dresden.de
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
import numpy as np

from DMT.exceptions import ValueTooSmallError
from DMT.extraction import XStep, plot
from DMT.core import specifiers


class XRes(XStep):
    """Base class for resistance extractions.

    Parameters
    ----------
    name            : str
        Name of this specific xres object.
    mcard           : :class:`~DMT.core.mc_parameter.McParameterCollection`
        This parameter collection needs to hold all relevant parameters of the model and is used for simulations or model equation calculations.
    lib             : :class:`~DMT.core.dut_lib.DutLib` or list[:class:`~DMT.core.dut_lib.DutView`]
        Library or list of devices with the measured resistance.
    op_definition   : {key : float, tuple or list}
        Defines how to filter the given data in the duts by setting either a single value (float), a range (2-element tuple) or a list of values (list) for each variable to filter.
    model                   : :class:`~DMT.extraction.model.Model`
        Model object with all model equations used for this extraction step.

    res_name : string
        Parameter name for the resistance to be extracted.
    col_voltage : :class:`~DMT.core.specifiers.SpecifierStr`
        Voltage to use for the extraction.
    col_current : :class:`~DMT.core.specifiers.SpecifierStr`
        Current to use.
    """

    def __init__(
        self, name, mcard, lib, op_definition, model, res_name, col_voltage, col_current, **kwargs
    ):
        # choose the model function
        self.model_function = self.model_resistance
        self.res_name = res_name

        self.model_function_info = {
            "independent_vars": ("v",),
            "depends": (
                self.res_name,
                "_constant",
            ),
        }

        # init the super class
        super().__init__(name, mcard, lib, op_definition, model=model, **kwargs)

        self.col_voltage = col_voltage
        self.col_current = col_current

        self.relevant_duts = [dut for dut in self.lib]

    @plot()
    def main_plot(self):
        """Overwrite main plot."""
        main_plot = super().main_plot(
            r"$I_{\mathrm{"
            + self.res_name
            + r"}} \left (V_{\mathrm{"
            + self.res_name
            + r"}} \right)$",
            x_specifier=specifiers.VOLTAGE,
            y_specifier=specifiers.CURRENT,
        )
        return main_plot

    def get_tex(self):
        """Return a tex Representation of the Model that is beeing fitted. This can then be displayed in the UI."""
        return (
            r"$V_\mathrm{"
            + self.res_name
            + r"} = R_{\mathrm{"
            + self.res_name
            + r"}}I_{\mathrm{"
            + self.res_name
            + r"}}$"
        )

    def ensure_input_correct_per_dataframe(self, dataframe, **_kwargs):
        """Search for all required columns in the data frames."""
        dataframe.ensure_specifier_column(self.col_voltage)
        dataframe.ensure_specifier_column(self.col_current)

    def model_resistance(self, v=None, res=None, _constant=0, **_kwargs):
        """Method to extract a resistance from a current/voltage dependence."""
        return v / res + _constant

    def set_initial_guess(self, data_reference):
        """Find suitable initial guesses for (some of the) model parameters from the given reference data and in this case also for the x_bounds."""
        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    data = dut.data[key]
                    curr = data[self.col_current].to_numpy()
                    voltage = data[self.col_voltage].to_numpy()
                    res = self.mcard.get(self.res_name)
                    res.value = 2e-6
                    res.min = 1e-6
                    try:
                        res.value = np.polyfit(curr, voltage, 1)[0]
                    except (ValueTooSmallError, ValueError) as e:
                        res.value = 1e-6

                    res.max = (
                        1e2  # no metallization should have a resistance higher than 100 Ohms..
                    )
                    self.mcard.set(res)

    def init_data_reference_per_dataframe(self, dataframe, t_meas, dut=None, key=None):
        """Find the required data in the user supplied dataframe or database and write them into data_model attribute of XStep object. In this case we want to optimize dVBE/dP !"""
        curr = dataframe[self.col_current].to_numpy()
        voltage = dataframe[self.col_voltage].to_numpy()
        line = {"x": voltage, "y": curr, "y_ref": curr}
        self.data_reference.append(line)
        self.labels.append(r"$T=\SI{" + str(t_meas) + r"}{\kelvin}$")

    # ▲▲▲▲▲▲▲
    # These two functions need to go "hand in hand". The temperature that corresponds to each line is needed to allow multidimensional fits.
    # ▾▾▾▾▾▾▾▾

    def fit(self, line, paras_model):
        """
        | The input data_model is a list of dicts [{'x':np.ndarray(), 'y':np.ndarray()}].
        | The x-values are already correct (bounds considered), however this function needs to write the y values.
        | This method needs to either:
        | - Calculate the data_model's y values for the x-values, if the x-step uses a ModelEquation
        | - Return the data_model's y values for the x-values, if the x-step uses a dut+sweep combination.
        |   In this cases, XStep already carried out dut+sweep simulations with the parameters before calling the function. Promised.
        |   Reason: This allows to use DMT's multithreading capabilities, speeding up the extraction significantly.
        """
        # dV_BE/dP using numerical derivative.
        res = paras_model[self.res_name]
        line["y"] = self.model_function(v=line["x"], res=res.value)
        return line
