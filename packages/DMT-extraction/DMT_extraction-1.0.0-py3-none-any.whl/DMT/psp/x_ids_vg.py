""" Extracts the drain source current parameters for PSP model

Parameters:
* neff
* betn
* mue
* themu
* k

* Direct on the I_D(V_G) characteristics at fixed V_DS ANDS fixed V_BS

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

from DMT.core import specifiers, sub_specifiers, constants
from DMT.extraction import XStep, plot, IYNormLog, print_to_documentation
from DMT.psp import find_dtj

try:
    from DMT.external.pylatex import Tex
    from pylatex import NoEscape
except ImportError:
    pass


class XIdsVg(XStep):
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
        verify_area_densities=False,
        **kwargs,
    ):
        if model is None:
            model = mcard.get_verilogae_model()

        self.model_function = self.extract_ids
        self.model_function_name = "ide"  # ids
        self.model_function_info = {
            "independent_vars": ("vgs", "vds", "vbs", "vdb", "t_dev"),
            "depends": (model.functions[self.model_function_name],),
        }

        if to_optimize is None:
            if mcard.get("swgeo").value == 0:
                to_optimize = ["neff", "betn", "mue", "themu", "k"]
            elif mcard.get("swgeo").value == 1:
                to_optimize = ["nsubo"]
            elif mcard.get("swgeo").value == 2:
                to_optimize = ["poneff"]
            else:
                raise IOError("SWGEO can only be 0,1,2")

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

        self.iynorm = IYNormLog

        self.verify_area_densities = verify_area_densities

    @plot()
    @print_to_documentation()
    def main_plot(self):
        main_plot = super(XIdsVg, self).main_plot(
            r"$ " + self.col_id.to_tex() + r" \left( " + self.col_vgs.to_tex() + r" \right) $",
            x_specifier=self.col_vgs,
            y_specifier=self.col_id,
            y_scale=1e3,
            y_log=True,
            legend_location="upper left",
        )
        return main_plot

    def get_tex(self):
        """Return a tex Representation of the Model that is beeing fitted. This can then be displayed in the UI."""
        return r"I_D = f( V_{GS}, V_{DS}, V_{BS})"

    def get_description(self):
        doc = Tex()
        doc.append(
            NoEscape(
                r"This extraction step fits the drain current model directly, without circuit simulation."
            )
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
        label = specifiers.TEMPERATURE.to_legend_with_value(t_meas, decimals=1)
        if self.mcard["swgeo"] != 0:
            label = (
                f"$l=\\SI{{{dut.length*1e6:.1f}}}{{\\micro\\metre}},\\,w=\\SI{{{dut.width*1e6:.1f}}}{{\\micro\\metre}},\\,$"
                + label
            )

        for _i_vds, v_ds_f, data_filtered_ds in dataframe.iter_unique_col(
            self.col_vds_forced, decimals=3
        ):
            for _i_vbs, v_bs_f, data_filtered_bs in data_filtered_ds.iter_unique_col(
                self.col_vbs_forced, decimals=3
            ):
                v_gs = data_filtered_bs[self.col_vgs].to_numpy().real
                i_d = data_filtered_bs[self.col_id].to_numpy().real
                v_db = data_filtered_bs[self.col_vdb].to_numpy().real
                v_ds = data_filtered_bs[self.col_vds].to_numpy().real
                v_bs = data_filtered_bs[self.col_vbs].to_numpy().real
                try:
                    temp = data_filtered_bs[specifiers.TEMPERATURE].to_numpy().real
                except KeyError:
                    temp = t_meas

                line = {
                    "x": v_gs,
                    "y": i_d,
                    self.col_id: i_d,
                    self.col_vds: v_ds,
                    self.col_vbs: v_bs,
                    self.col_vdb: v_db,
                    specifiers.TEMPERATURE: temp,
                    "length": dut.length,
                    "width": dut.width,
                }
                self.data_reference.append(line)
                self.labels.append(
                    label
                    + ",\\,"
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
        data_model["y"] = self.extract_ids(
            vgs=data_model["x"],
            vds=data_model[self.col_vds],
            vbs=data_model[self.col_vbs],
            vdb=data_model[self.col_vdb],
            t_dev=data_model[specifiers.TEMPERATURE],
            i_d=data_model[self.col_id],
            width=data_model["width"],
            length=data_model["length"],
            **paras_model.to_kwargs(),
        )
        return data_model

    def extract_ids(self, vgs, vds, vbs, vdb, t_dev, i_d, width=0.0, length=0.0, **kwargs):
        kwargs["l"] = length
        kwargs["w"] = width
        # PSP uses uppercase model parameters:
        kwargs = {k.upper(): v for k, v in kwargs.items()}

        voltages = {
            "br_DT": 0,
            "br_GPSI": vgs,
            "br_DISI": vds,
            "br_SIBP": -vbs,
            "br_SIBS": -vbs,
            "br_DIBP": vdb,
            "br_DIBD": vdb,
        }

        return self.model.functions[self.model_function_name].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )

        sigVds = np.where(vds, np.sign(vds), 1)  # 0 equals to positve sign.

        # call model function in VerilogAE
        # if (sigVds > 0.0) begin
        #     I(DI, BP)    <+  CHNL_TYPE * MULT_i * Iimpact;
        #     I(DI, SI)    <+  CHNL_TYPE * MULT_i * (Ids + Idsedge);
        #     I(GP, SI)    <+  CHNL_TYPE * MULT_i * Igcs;
        #     I(GP, DI)    <+  CHNL_TYPE * MULT_i * Igcd;
        # end else begin
        #     I(SI, BP)    <+  CHNL_TYPE * MULT_i * Iimpact;
        #     I(SI, DI)    <+  CHNL_TYPE * MULT_i * (Ids + Idsedge);
        #     I(GP, DI)    <+  CHNL_TYPE * MULT_i * Igcs;
        #     I(GP, SI)    <+  CHNL_TYPE * MULT_i * Igcd;
        # end
        iimpact = self.model.functions["evaluateblock.Iimpact"].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )

        ids = self.model.functions["evaluateblock.Ids"].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )
        idsedge = self.model.functions["evaluateblock.Idsedge"].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )

        igcs = self.model.functions["evaluateblock.Igcs"].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )
        igcd = self.model.functions["evaluateblock.Igcd"].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )

        # I(GP, DI)    <+  CHNL_TYPE * MULT_i * Igdov;
        # I(DI, BP)    <+  CHNL_TYPE * MULT_i * Igidl;
        # I(BD, DI)    <+  CHNL_TYPE * MULT_i * ijun_d;
        igdov = self.model.functions["evaluateblock.Igdov"].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )
        igidl = self.model.functions["Igidl"].eval(temperature=t_dev, voltages=voltages, **kwargs)
        ijun_d = self.model.functions["evaluateblock.ijun_d"].eval(
            temperature=t_dev, voltages=voltages, **kwargs
        )

        if kwargs["TYPE"] >= 0:
            chnl_type = 1
        else:
            chnl_type = -1

        nf = kwargs["NF"] if kwargs["NF"] > 1.0 else 1.0
        mult = kwargs["MULT"] * nf
        mult = mult if mult > 0.0 else 0.0

        id_sum = -igdov + igidl - ijun_d

        id_sum = np.where(sigVds, id_sum + iimpact, id_sum)
        id_sum = np.where(sigVds, id_sum + ids + idsedge, id_sum - ids - idsedge)
        id_sum = np.where(sigVds, id_sum, id_sum - igcs)
        id_sum = np.where(sigVds, id_sum - igcd + idsedge, id_sum)

        # id_sum = ids

        return chnl_type * mult * id_sum
