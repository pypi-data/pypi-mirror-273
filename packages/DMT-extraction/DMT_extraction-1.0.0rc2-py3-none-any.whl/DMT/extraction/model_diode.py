r""" Specifies the model structure for a very simple diode
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

from DMT.core import constants
from DMT.core.circuit import CircuitElement, RESISTANCE, CURRENT
from DMT.extraction.model import Model


class ModelDiode(Model):
    """Implements a simple diode model for testing purposes of the Model class that represents compact models."""

    def __init__(self):
        super().__init__("diode", 1.0, ["A", "C"], ["v", "i", "t"])

        self.model_i_temp_info = {"depends": ("scale_is_temp",)}
        self.netlist.append(
            CircuitElement(CURRENT, "I_D", ("A", "mid"))
        )  # , method=self.model_i_temp
        self.netlist.append(CircuitElement(RESISTANCE, "R_S", ("mid", "C")))
        # , method=self.model_series_resistance_temp

    def model_i_temp(self, v, t, m=None, **kwargs):
        """Diode current as a function of model parameters m, i_s0, zeta and tnom"""
        i_s = self.scale_is_temp(t, **kwargs)
        vt = constants.P_K * t / constants.P_Q  # thermal voltage
        return i_s * np.expm1(v / m / vt)  # final diode current

    def scale_is_temp(self, t, i_s0=None, tnom=None, zeta=None, **_kwargs):
        """Scale saturation current"""
        return i_s0 * (t / tnom) ** zeta

    def model_series_resistance_temp(self, t_dev=None, r=None, zeta=None, tnom=None, **_kwargs):
        """Temperature dependent series resistance"""
        return r * (t_dev / (tnom + constants.P_CELSIUS0)) ** zeta
