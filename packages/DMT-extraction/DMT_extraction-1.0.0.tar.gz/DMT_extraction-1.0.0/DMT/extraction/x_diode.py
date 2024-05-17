"""  Extracts model parameters for a very simple diode model and is used for the Jupyter Docs only as a reference!

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
import numpy as np

from DMT.core import constants, specifiers
from DMT.extraction import XStep, plot, IYNormLog


class XDiode(XStep):
    """Class for extraction of DMT.extraction.Diode I(V) model parameters. The arguments to this Xstep
    are described in the DMT.extraction.XStep class.
    """

    def __init__(
        self, name, mcard, lib, op_definition, model, relevant_duts=None, to_optimize=None, **kwargs
    ):
        # this is the model equation to be fitted by this XStep
        self.model_function = model.model_i_temp

        # init the super class
        super().__init__(
            name, mcard, lib, op_definition, model=model, to_optimize=to_optimize, **kwargs
        )
        self.iynorm = IYNormLog

        if relevant_duts is None:
            self.relevant_duts = [lib.dut_ref]
        else:
            self.relevant_duts = relevant_duts

        self.col_v = specifiers.VOLTAGE + "D"
        self.col_i = specifiers.CURRENT + "D"
        self.col_t = specifiers.TEMPERATURE

    @plot()
    def main_plot(self):
        """Overwrite main plot method from XStep and adjust for the diode I(V) characteristics."""
        main_plot = super(XDiode, self).main_plot(
            r"$ " + self.col_i.to_tex() + r" \left( " + self.col_v.to_tex() + r" \right) $",
            x_specifier=self.col_v,
            y_specifier=self.col_i,
            y_scale=1e3,
            legend_location="upper left",
            y_log=True,
        )
        return main_plot

    def get_tex(self):
        """Return a tex Representation of the Model that is being fitted. This string then be displayed in the GUI."""
        return r"$I_{\mathrm{D}}=f\left( V_{\mathrm{D}} ,T \right)$"

    def ensure_input_correct_per_dataframe(self, dataframe, **_kwargs):
        """Search for the required columns for this XStep in the Pandas DataFrame objects."""
        dataframe.ensure_specifier_column(self.col_v)
        dataframe.ensure_specifier_column(self.col_i)

    def set_initial_guess(self, data_reference):
        """Find suitable initial guesses for (some of the) model parameters from the given reference data."""

        # find the line at the nominal temperature:
        tnom = self.mcard.get("tnom").value
        i_tnom = np.argmin([np.abs(line[specifiers.TEMPERATURE] - tnom) for line in data_reference])

        # find the point with the lowest absolute voltage at the nominal temperature
        v_T = constants.calc_VT(data_reference[i_tnom][specifiers.TEMPERATURE])

        i_v_mean = int(len(data_reference[i_tnom]["x"]) / 2)

        v_1 = data_reference[i_tnom]["x"][i_v_mean]
        v_2 = data_reference[i_tnom]["x"][i_v_mean + 1]
        i_1 = data_reference[i_tnom]["y"][i_v_mean]
        i_2 = data_reference[i_tnom]["y"][i_v_mean + 1]

        m_guess = (v_1 - v_2) / (v_T * np.log(i_1 / i_2))
        is0_guess = i_2 / np.expm1(v_2 / (m_guess * v_T))

        try:
            self.mcard.set_values(
                {
                    "i_s0": is0_guess,
                    "m": m_guess,
                }
            )
        except ValueError:
            pass

        # zeta
        try:
            i_t2 = next(
                index
                for index, line in enumerate(data_reference)
                if line[specifiers.TEMPERATURE] != data_reference[i_tnom][specifiers.TEMPERATURE]
            )
            t_2 = data_reference[i_t2][specifiers.TEMPERATURE]
            v_T = constants.calc_VT(t_2)
            v_2 = data_reference[i_t2]["x"][i_v_mean + 1]
            i_2 = data_reference[i_t2]["y"][i_v_mean + 1]
            is0_t2 = i_2 / np.expm1(v_2 / (m_guess * v_T))
            self.mcard.set_values(
                {
                    "zeta": np.log(is0_t2 / is0_guess) / np.log(t_2 / tnom),
                }
            )
        except StopIteration:
            pass

    def init_data_reference_per_dataframe(self, dataframe, t_meas, **_kwargs):
        """Find the required data in the user supplied dataframe or database and write them into
        the data_reference attribute of the XStep object.
        """
        v = dataframe[self.col_v].to_numpy()
        i = dataframe[self.col_i].to_numpy()
        line = {"x": v, "y": i, specifiers.TEMPERATURE: t_meas}
        self.data_reference.append(line)
        self.labels.append(
            r"$ T=\SI{" + str(t_meas) + r"}{\kelvin} $"
        )  # ensures nice labels in the plot

    def fit(self, line, paras_model):
        """Calculate the diode current for each line from the current modelcard paras_model."""
        line["y"] = self.model_function(
            v=line["x"],
            t=line[specifiers.TEMPERATURE],
            **paras_model.to_kwargs(),
        )
        return line
