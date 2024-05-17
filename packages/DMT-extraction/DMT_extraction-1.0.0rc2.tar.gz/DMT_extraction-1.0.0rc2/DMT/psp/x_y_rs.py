""" Extracts the series resistance from MOSFET transistors
* RS

Direct on the I_D(V_GS) characteristics at fixed V_DS AND fixed V_BS. V_DS must be chosen very low.

R. Trevisoli et al., "A New Method for Series Resistance Extraction
of Nanometer MOSFETs", IEEE TED, 2017.

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
from DMT.core import specifiers, sub_specifiers, constants, Plot
from DMT.extraction import XStep, plot, print_to_documentation
import numpy as np

try:
    from DMT.external.pylatex import Tex
    from pylatex import NoEscape
except ImportError:
    pass


class XYRs(XStep):
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
        name,
        mcard,
        lib,
        op_definition,
        model=None,
        relevant_duts=None,
        to_optimize=None,
        **kwargs,
    ):
        if model is None:
            model = mcard.get_verilogae_model()

        self.model_function = self.extract_rs
        self.model_function_info = {
            "independent_vars": ("vgs", "vds", "vbs", "vdb", "t_dev"),
            "depends": (self.extract_rs,),
        }

        if to_optimize is None:
            to_optimize = (["vt"],)

        # init the super class
        super().__init__(
            name,
            mcard,
            lib,
            op_definition,
            model=model,
            to_optimize=to_optimize,
            specifier_paras={},
            **kwargs,
        )

        if relevant_duts is None:
            self.relevant_duts = [self.lib.dut_ref]
        else:
            self.relevant_duts = relevant_duts

        self.col_vgs = specifiers.VOLTAGE + ["G", "S"]
        self.col_vds = specifiers.VOLTAGE + ["D", "S"]
        self.col_vdb = specifiers.VOLTAGE + ["D", "B"]
        self.col_vbs = specifiers.VOLTAGE + ["B", "S"]

        self.col_vgs_forced = self.col_vgs + sub_specifiers.FORCED
        self.col_vds_forced = self.col_vds + sub_specifiers.FORCED
        self.col_vdb_forced = self.col_vdb + sub_specifiers.FORCED
        self.col_vbs_forced = self.col_vbs + sub_specifiers.FORCED

        self.col_id = specifiers.CURRENT + "D"

    @plot()
    @print_to_documentation()
    def main_plot(self):
        main_plot = super(XYRs, self).main_plot(
            r"$ R_{\mathrm{T}} \left( g_{\mathrm{m}}^{0.5}/I_{\mathrm{D}} \right) $",
            y_label=r"$R_{\mathrm{T}} \left( \kilo\ohm \si{} \right)$",
            x_label=r"$g_{\mathrm{m}}^{0.5}/I_{\mathrm{D}} \left( \si{\square\volt} \right)$",
            y_scale=1e-3,
            x_scale=1,
            legend_location="upper left",
        )
        return main_plot

    def get_tex(self):
        """Return a tex Representation of the Model that is beeing fitted. This can then be displayed in the UI."""
        return r"RT= f( V_{GS}, Y)"

    def get_description(self):
        doc = Tex()
        doc.append(
            NoEscape(r"This extraction step uses the Y function to extract the series resistance.")
        )
        return doc

    def ensure_input_correct_per_dataframe(self, dataframe, dut=None, key=None):
        """Search for all required columns in the data frames."""
        dataframe.ensure_specifier_column(self.col_vgs)
        dataframe.ensure_specifier_column(self.col_vds)
        dataframe.ensure_specifier_column(self.col_vbs)
        dataframe.ensure_specifier_column(self.col_vdb)
        dataframe.ensure_specifier_column(self.col_vgs_forced)
        dataframe.ensure_specifier_column(self.col_vds_forced)
        dataframe.ensure_specifier_column(self.col_vbs_forced)
        dataframe.ensure_specifier_column(self.col_vdb_forced)
        dataframe.ensure_specifier_column(self.col_id)

    def set_initial_guess(self, data_reference):
        """Find suitable initial guesses for (some of the) model parameters from the given reference data."""
        pass

    def init_data_reference_per_dataframe(self, dataframe, t_meas, dut=None, key=None):
        """Find the reference data for each line in the supplied dataframe or database.
        Write the data into the data_model attribute of this XStep object.
        """
        label = f"$T=\\SI{{{t_meas:.1f}}}{{\\kelvin}},\\,$"
        if self.mcard["swgeo"] != 0:
            label = (
                f"$l=\\SI{{{dut.length*1e6:.1f}}}{{\\micro\\metre}},\\,w=\\SI{{{dut.width*1e6:.1f}}}{{\\micro\\metre}},\\,$"
                + label
            )
        for _i_vb, v_bs_f, data_filtered_bs in dataframe.iter_unique_col(
            self.col_vbs_forced, decimals=3
        ):
            for _i_vg, v_ds_f, data_filtered_ds in data_filtered_bs.iter_unique_col(
                self.col_vds_forced, decimals=3
            ):
                v_gs = data_filtered_ds[self.col_vgs].to_numpy().real
                v_db = data_filtered_ds[self.col_vdb].to_numpy().real
                v_ds = data_filtered_ds[self.col_vds].to_numpy().real
                v_bs = data_filtered_ds[self.col_vbs].to_numpy().real
                i_d = data_filtered_ds[self.col_id].to_numpy().real
                gm = np.gradient(i_d, v_gs)
                yfun = np.abs(i_d) / np.sqrt(np.abs(gm))
                rt = v_ds / i_d
                try:
                    temp = data_filtered_bs[specifiers.TEMPERATURE].to_numpy().real
                except KeyError:
                    temp = t_meas

                line = {
                    "x": 1 / yfun,
                    "y": rt,
                    self.col_vds: v_ds,
                    self.col_id: i_d,
                    self.col_vbs: v_bs,
                    self.col_vdb: v_db,
                    specifiers.TEMPERATURE: temp,
                    "length": dut.length,
                    "width": dut.width,
                }
                self.data_reference.append(line)
                self.labels.append(
                    label
                    + self.col_vds.to_legend_with_value(v_ds_f)
                    + ",\\,"
                    + self.col_vbs.to_legend_with_value(v_bs_f)
                )

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
        data_model["y"] = self.extract_rs(
            yfun=data_model["x"],
            vds=data_model[self.col_vds],
            vbs=data_model[self.col_vbs],
            vdb=data_model[self.col_vdb],
            t_dev=data_model[specifiers.TEMPERATURE],
            width=data_model["width"],
            length=data_model["length"],
            **paras_model.to_kwargs(),
        )
        return data_model

    def extract_rs(
        self, yfun, vds, vbs, vdb, t_dev, *, k=None, rs=None, width=0.0, length=0.0, **kwargs
    ):
        # kwargs["l"] = length
        # kwargs["w"] = width
        # PSP uses uppercase model parameters:
        # kwargs = {k.upper(): v for k, v in kwargs.items()}

        # call model function in VerilogAE
        return k * yfun + rs
