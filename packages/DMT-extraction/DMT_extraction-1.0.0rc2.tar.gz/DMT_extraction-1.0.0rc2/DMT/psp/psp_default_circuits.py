""" Defines some psp default circuits.


"""

# DMT
# Copyright (C) from 2022  SemiMod
# <https://gitlab.com/dmt-development/dmt-extraction>
#
# This file is part of DMT-extraction.
#
# DMT_extraction is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# DMT_extraction is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from DMT.core import Circuit, CircuitElement
from DMT.core.circuit import RESISTANCE, VOLTAGE, SHORT, CAPACITANCE


def get_circuit(circuit_type, modelcard):
    """
    Currently implemented:

    * 'common_source' : Common source configuration of a PSP MOSFET with temperature and bulk nodes and resistors that represents the parasitic connections to the transistor.

    Parameters
    ----------
    circuit_type : str
        For allowed types, see above
    modelcard : :class:`~DMT.psp.mc_psp.McPsp`

    Returns
    -------
    circuit : :class:`~DMT.core.circuit.Circuit`

    """
    circuit_elements = []
    if circuit_type == "common_source":
        # model instance
        circuit_elements.append(
            CircuitElement(
                modelcard.default_module_name,
                "Q_V",
                ["n_D", "n_G", "n_S", "n_B", "n_T"],
                parameters=modelcard,
            )
        )
        # GATE NODE CONNECTION #############
        # metal resistance between contact base point and real collector
        try:
            rgm = modelcard.get("_rgm").value
        except KeyError:
            rgm = 1e-3

        circuit_elements.append(
            CircuitElement(RESISTANCE, "Rgm", ["n_G_FORCED", "n_G"], parameters=[("R", str(rgm))])
        )
        # shorts for current measurement
        circuit_elements.append(
            CircuitElement(
                SHORT,
                "I_G",
                ["n_GX", "n_G_FORCED"],
            )
        )
        # capacitance since AC already deembeded Rgm
        circuit_elements.append(
            CircuitElement(CAPACITANCE, "Cgm", ["n_G_FORCED", "n_G"], parameters=[("C", str(1))])
        )

        # DRAIN NODE CONNECTION #############
        circuit_elements.append(
            CircuitElement(
                SHORT,
                "I_D",
                ["n_DX", "n_D_FORCED"],
            )
        )
        # metal resistance between contact collector point and real collector
        try:
            rdm = modelcard.get("_rdm").value
        except KeyError:
            rdm = 1e-3

        circuit_elements.append(
            CircuitElement(RESISTANCE, "Rdm", ["n_D_FORCED", "n_D"], parameters=[("R", str(rdm))])
        )
        # capacitance since AC already deembeded Rcm
        circuit_elements.append(
            CircuitElement(CAPACITANCE, "Cdm", ["n_D_FORCED", "n_D"], parameters=[("C", str(1))])
        )
        # SOURCE NODE CONNECTION #############
        circuit_elements.append(
            CircuitElement(
                SHORT,
                "I_S",
                ["n_SX", "n_S_FORCED"],
            )
        )
        # metal resistance between contact emiter point and real emiter
        try:
            rsm = modelcard.get("_rsm").value
        except KeyError:
            rsm = 1e-3

        circuit_elements.append(
            CircuitElement(RESISTANCE, "Rsm", ["n_S_FORCED", "n_S"], parameters=[("R", str(rsm))])
        )
        # capacitance since AC already deembeded Rcm
        circuit_elements.append(
            CircuitElement(CAPACITANCE, "Csm", ["n_S_FORCED", "n_S"], parameters=[("C", str(1))])
        )
        # BULK NODE CONNECTION #############
        circuit_elements.append(
            CircuitElement(
                SHORT,
                "I_B",
                ["n_BX", "n_B_FORCED"],
            )
        )
        # metal resistance between contact emiter point and real emiter
        try:
            rbm = modelcard.get("_rbm").value
        except KeyError:
            rbm = 1e-3

        circuit_elements.append(
            CircuitElement(RESISTANCE, "Rbm", ["n_B_FORCED", "n_B"], parameters=[("R", str(rbm))])
        )
        # capacitance since AC already deembeded Rcm
        circuit_elements.append(
            CircuitElement(CAPACITANCE, "Cbm", ["n_B_FORCED", "n_B"], parameters=[("C", str(1))])
        )
        # VOLTAGE SOURCES ##################
        circuit_elements.append(
            CircuitElement(VOLTAGE, "V_G", ["n_GX", "0"], parameters=[("Vdc", "V_G"), ("Vac", "1")])
        )
        circuit_elements.append(
            CircuitElement(VOLTAGE, "V_D", ["n_DX", "0"], parameters=[("Vdc", "V_D"), ("Vac", "1")])
        )
        circuit_elements.append(
            CircuitElement(VOLTAGE, "V_S", ["n_SX", "0"], parameters=[("Vdc", "V_S"), ("Vac", "1")])
        )
        circuit_elements.append(
            CircuitElement(VOLTAGE, "V_B", ["n_BX", "0"], parameters=[("Vdc", "V_B"), ("Vac", "1")])
        )
        # resistance at T node so that it is not open
        circuit_elements.append(
            CircuitElement(RESISTANCE, "R_T", ["n_T", "0"], parameters=[("R", "1e10")])
        )

        circuit_elements += [
            "V_G=0",
            "V_D=0",
            "V_S=0",
            "V_B=0",
            "ac_switch=0",
            "V_G_ac=1-ac_switch",
            "V_D_ac=ac_switch",
            "V_B_ac=0",
            "V_S_ac=0",
        ]
    else:
        raise IOError("The circuit type " + circuit_type + " is unknown!")

    return Circuit(circuit_elements)
