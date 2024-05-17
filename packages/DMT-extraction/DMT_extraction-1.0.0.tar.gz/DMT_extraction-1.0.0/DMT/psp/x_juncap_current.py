""" Extracts the source-bulk and drain-bulk junction current parameters for the PSP model

Parameters:
* either:

* Direct on the I_SB(V_SB) or I_DB(V_SB) characteristics at fixed V_DS=0V AND fixed V_GS=0V

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
import numpy as np
from typing import Literal

from DMT.core import specifiers, DutView, DutLib
from DMT.extraction import XStep, plot, print_to_documentation, IYNormLog
from DMT.psp import McPsp

try:
    from DMT.external.pylatex import Tex
    from pylatex import NoEscape
except ImportError:
    pass


class XJuncapCurrent(XStep):
    """

    Parameters
    ----------
    name                    : str
        Name of this XStep in the parameter extraction flow.
    mcard                   : :class:`~DMT.core.mcard.MCard` or :class:`~DMT.core.mc_parameter.McParameterCollection`
        This MCard needs to hold all relevant parameters of the model and is used for simulations or model equation calculations.
    lib                     : :class:`~DMT.core.dut_lib.DutLib`
        This library of devices need to hold a relevant internal dut with data in one or more DataFrames as fitting reference.
    op_definition           : {key : float, tuple or list}
        Defines how to filter the given data in the duts by setting either a single value (float), a range (2-element tuple) or a list of values (list) for each variable to filter.
    model                   : VerilogAE model
        Model object with all model equations used for this extraction step.
    """

    def __init__(
        self,
        name: str,
        mcard: McPsp,
        lib: DutLib,
        op_definition: dict,
        dut_square: DutView,
        dut_finger: DutView,
        dut_miller: DutView,
        component: Literal["bottom", "STI-edge", "gate-edge", "full"],
        junction: Literal["source-bulk", "drain-bulk"],
        to_optimize_set: Literal["ideal", "srh", "btb", "avalanche"] = "ideal",
        model=None,
        to_optimize=None,
        relevant_duts=None,
        **kwargs,
    ):
        if model is None:
            model = mcard.get_verilogae_model()

        # if to_optimize is not None:
        #     raise IOError(
        #         "DMT-XJuncapCurrent: For this step the parameters to optimize have to be set implicitly!"
        #     )

        self.model_function = self.extract_juncap_current
        self.model_function_name = None

        self.component = component

        if junction == "source-bulk":
            self.junction = "ijs"
            junc = ""
        elif junction == "drain-bulk":
            self.junction = "ijd"
            junc = "d"
        else:
            raise IOError("DMT-XJuncapCurrent: Only source-bulk or drain-bulk junctions are known!")

        if component == "bottom":
            comp = "bot"
            comps = [comp]
        elif component == "STI-edge":
            comp = "sti"
        elif component == "gate-edge":
            comp = "gat"
        elif component == "full":
            comp = ""
            comps = ["bot", "sti", "gat"]
        else:
            raise IOError(
                "DMT-XJuncapCurrent: Only bottom, STI-edge, gate-edge and full components are known!"
            )

        self.model_function_name = f"{self.junction}{comp}_extract"
        if to_optimize is None:
            if to_optimize_set not in ["ideal", "srh", "btb", "avalanche"]:
                raise IOError("DMT-XJuncapCurrent: Unknown to to_optimize set")
            to_optimize_options = {
                "ideal": ["idsatr", "phig"],
                "srh": ["mefftat", "ctat", "csrh"],
                "btb": ["fbbtr", "stfbbt", "cbbt"],
                "avalanche": ["vbr", "pbr"],
            }

            to_optimize = []
            for comp_a in comps:
                to_optimize += [
                    para + comp_a + junc for para in to_optimize_options[to_optimize_set]
                ]
                if comp_a in ["sti", "gat"] and to_optimize_set == "srh":
                    to_optimize.append(f"xjun{comp_a}")

        self.model_function_info = {
            "independent_vars": ("vsb", "vdb", "t_dev"),
            "depends": (model.functions[self.model_function_name],),
        }

        if relevant_duts is None:
            relevant_duts = [dut_square, dut_finger, dut_miller]
        else:
            raise IOError("DMT-XJuncapCurrent: For this step the duts have to be set explicitly!")

        self.dut_square = dut_square
        self.dut_finger = dut_finger
        self.dut_miller = dut_miller

        # init the super class
        super().__init__(
            name,
            mcard,
            lib,
            op_definition,
            model=model,
            to_optimize=to_optimize,
            specifier_paras={},
            relevant_duts=relevant_duts,
            **kwargs,
        )
        self.iynorm = IYNormLog

        if junction == "source-bulk":
            self.col_i_fit_print = specifiers.CURRENT + "S"
            self.col_i_fit = specifiers.CURRENT + "S"
            self.col_v_fit = specifiers.VOLTAGE + ["S", "B"]
        else:
            self.col_i_fit_print = specifiers.CURRENT + "D"
            self.col_i_fit = specifiers.CURRENT + "D"
            self.col_v_fit = specifiers.VOLTAGE + ["D", "B"]

        self.col_vsb = specifiers.VOLTAGE + ["S", "B"]
        self.col_vdb = specifiers.VOLTAGE + ["D", "B"]
        self.col_vds = specifiers.VOLTAGE + ["D", "S"]
        self.col_is = specifiers.CURRENT + "S"
        self.col_id = specifiers.CURRENT + "D"

    @plot()
    @print_to_documentation()
    def main_plot(self):
        main_plot = super(XJuncapCurrent, self).main_plot(
            r"$ "
            + self.col_i_fit_print.to_tex()
            + r" \left( "
            + self.col_v_fit.to_tex()
            + r" \right) $",
            x_specifier=self.col_v_fit,
            y_specifier=self.col_i_fit_print,
            y_log=True,
            legend_location="upper left",
        )
        return main_plot

    def get_tex(self):
        """Return a tex Representation of the Model that is beeing fitted. This can then be displayed in the UI."""
        return self.col_i_fit_print.to_tex()

    def get_description(self):
        doc = Tex()
        doc.append(
            NoEscape(
                r"This extraction step fits the JUNCAP2 Current model directly, without circuit simulation."
            )
        )
        return doc

    def ensure_input_correct_per_dataframe(self, dataframe, dut=None, key=None):
        """Search for all required columns in the data frames."""
        dataframe.ensure_specifier_column(self.col_vsb)
        dataframe.ensure_specifier_column(self.col_vdb)
        dataframe.ensure_specifier_column(self.col_vds)
        dataframe.ensure_specifier_column(self.col_id)
        dataframe.ensure_specifier_column(self.col_is)

    def init_data_reference(self):
        """ """
        if self.junction == "ijs":
            name_ab = "absource"
            name_ls = "lssource"
            name_lg = "lgsource"
        else:
            name_ab = "abdrain"
            name_ls = "lsdrain"
            name_lg = "lgdrain"

        v_j = {}
        i_j_square = {}
        i_j_finger = {}
        i_j_miller = {}
        ls_square = self.dut_square.modelcard[name_ls].value
        ls_finger = self.dut_finger.modelcard[name_ls].value
        ls_miller = self.dut_miller.modelcard[name_ls].value
        ab_square = self.dut_square.modelcard[name_ab].value
        ab_finger = self.dut_finger.modelcard[name_ab].value
        ab_miller = self.dut_miller.modelcard[name_ab].value
        lg_square = self.dut_square.modelcard[name_lg].value
        lg_miller = self.dut_miller.modelcard[name_lg].value
        data_reference = {}
        temps = []
        for key in self.dut_square.data:
            if self.validate_key(key):
                temp = self.dut_square.get_key_temperature(key)
                if temp in temps:
                    raise OSError("Two measurements with the same temp?")

                data = self.dut_square.data[key]
                temps.append(temp)
                v_j[temp] = data[self.col_v_fit]
                i_j_square[temp] = np.real(data[self.col_i_fit].to_numpy())
                i_j_finger[temp] = np.real(self.dut_finger.data[key][self.col_i_fit].to_numpy())
                i_j_miller[temp] = np.real(self.dut_miller.data[key][self.col_i_fit].to_numpy())
                data_reference[temp] = {
                    "x": np.real(data[self.col_v_fit].to_numpy()),
                    self.col_vsb: np.real(data[self.col_vsb].to_numpy()),
                    self.col_vdb: np.real(data[self.col_vdb].to_numpy()),
                    self.col_vds: np.real(data[self.col_vds].to_numpy()),
                    specifiers.TEMPERATURE: temp,
                }

        if self.component == "bottom":
            for temp in temps:
                data_reference[temp]["y"] = (
                    (ls_finger * i_j_square[temp] - ls_square * i_j_finger[temp])
                    / (ls_finger * ab_square - ls_square * ab_finger)
                    * ab_square
                )

        elif self.component == "STI-edge":
            for temp in temps:
                data_reference[temp]["y"] = (
                    (ab_square * i_j_finger[temp] - ab_finger * i_j_square[temp])
                    / (ls_finger * ab_square - ls_square * ab_finger)
                    * ls_square
                )
        elif self.component == "gate-edge":
            for temp in temps:
                i_j_bot = (ls_finger * i_j_square[temp] - ls_square * i_j_finger[temp]) / (
                    ls_finger * ab_square - ls_square * ab_finger
                )
                i_j_sti = (ab_square * i_j_finger[temp] - ab_finger * i_j_square[temp]) / (
                    ls_finger * ab_square - ls_square * ab_finger
                )
                data_reference[temp]["y"] = (
                    (i_j_miller[temp] - ab_miller * i_j_bot - ls_miller * i_j_sti) - lg_miller
                ) * lg_square
        elif self.component == "full":
            for temp in temps:
                data_reference[temp]["y"] = i_j_square[temp]

        self.data_reference = [data_reference[temp_a] for temp_a in temps]
        self.labels = [
            specifiers.TEMPERATURE.to_legend_with_value(temp_a, decimals=0) for temp_a in temps
        ]

    def fit(self, data_model, paras_model, dut=None):
        """Calculate the drain current from known node voltages.

        Parameters
        ----------
        data_model : {'x':np.ndarray(), 'y':np.ndarray(), 'y_ref':np.ndarray(), 'TEMP':float}
            Content of this dict is defined in the method "init_data_reference_per_dataframe".
        paras_model : MCard
            The model parameters for which the drain current "y" should be calculated.

        Returns
        -------
        data_model : [{'x':np.ndarray(), 'y':np.ndarray(), 'y_ref':np.ndarray(), 'TEMP':float}]
            Same dict as input, but "y" now corresponds to the drain current.

        """
        data_model["y"] = self.model_function(
            vsb=data_model[self.col_vsb],
            vdb=data_model[self.col_vdb],
            vds=data_model[self.col_vds],
            t_dev=data_model[specifiers.TEMPERATURE],
            **paras_model.to_kwargs(),
        )
        return data_model

    def extract_juncap_current(self, vsb, vdb, vds, t_dev, **kwargs):
        # PSP uses uppercase model parameters:
        kwargs = {k.upper(): v for k, v in kwargs.items()}

        return self.model.functions[self.model_function_name].eval(
            temperature=t_dev,
            voltages={"br_SIBS": vsb, "br_DIBD": vdb, "br_DISI": vds},
            **kwargs,
        )
