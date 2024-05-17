""" Extracts the gate-source and gate-drain capacitance parameters for the PSP model

Parameters:
* cgov
* nov

* Direct on the C_CG(V_G) = C_DG + C_SG characteristics at fixed V_DS=0V ANDS fixed V_BS=0V

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
from DMT.core import specifiers, DataFrame, DutView
from DMT.extraction import XStep, plot, IYNormLog, print_to_documentation

try:
    from DMT.external.pylatex import Tex
    from pylatex import NoEscape
except ImportError:
    pass


class XCcg(XStep):
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

        self.model_function = self.extract_ccg
        self.model_function_info = {
            "independent_vars": ("vgs", "vds", "vbs", "t_dev"),
            "depends": (model.functions["Qg_dVg"],),
        }

        if to_optimize is None:
            if mcard.get("swgeo").value == 0:
                to_optimize = ["cgov", "nov"]
            elif mcard.get("swgeo").value == 1:
                # raise NotImplementedError("CGOV does not exists for SWGEO = 1 (global)")
                to_optimize = ["toxovdo", "novo"]

            elif mcard.get("swgeo").value == 2:
                to_optimize = [
                    "pocgov",
                    "plcgov",
                    "pwcgov",
                    "plwcgov",
                    "ponov",
                    "plnov",
                    "pwnov",
                    "plwnov",
                ]

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
        self.col_vbs = specifiers.VOLTAGE + ["B", "S"]
        self.col_cgs = specifiers.CAPACITANCE + ["G", "S"]
        self.col_cgd = specifiers.CAPACITANCE + ["G", "D"]
        self.col_cgg = specifiers.CAPACITANCE + ["G", "G"]
        self.col_id = specifiers.CURRENT + "D"

        self.iynorm = IYNormLog

        self.verify_area_densities = verify_area_densities

    @plot()
    @print_to_documentation()
    def main_plot(self):
        main_plot = super(XCcg, self).main_plot(
            r"$ " + r"C_{\mathrm{CG}}" + r" \left( " + self.col_vgs.to_tex() + r" \right) $",
            x_specifier=self.col_vgs,
            y_label=r"$C_{\mathrm{CG}} ( \si{\femto\farad} ) $",
            y_scale=1e15,
            legend_location="upper left",
        )
        return main_plot

    def get_tex(self):
        """Return a tex Representation of the Model that is beeing fitted. This can then be displayed in the UI."""
        return r"C_{CG} = f( V_{GS} )"

    def get_description(self):
        doc = Tex()
        doc.append(
            NoEscape(
                r"This extraction step fits the CCG model directly, without circuit simulation."
            )
        )
        return doc

    def ensure_input_correct_per_dataframe(self, dataframe, dut=None, key=None):
        """Search for all required columns in the data frames."""
        dataframe.ensure_specifier_column(self.col_vgs)
        dataframe.ensure_specifier_column(self.col_vds)
        dataframe.ensure_specifier_column(self.col_vbs)
        dataframe.ensure_specifier_column(self.col_cgs, ports=["G", "D"])
        dataframe.ensure_specifier_column(self.col_cgd, ports=["G", "D"])
        dataframe.ensure_specifier_column(self.col_cgg, ports=["G", "D"])
        dataframe.ensure_specifier_column(self.col_id)

    def set_initial_guess(self, data_reference):
        """Find suitable initial guesses for (some of the) model parameters from the given reference data."""
        pass

    def init_data_reference_per_dataframe(
        self, dataframe: DataFrame, t_meas: float, dut: DutView = None, key: str = None
    ):
        """Find the reference data for each line in the supplied dataframe or database.
        Write the data into the data_model attribute of this XStep object.
        """
        label = f"$T=\\SI{{{t_meas:.1f}}}{{\\kelvin}},\\,$"
        if self.mcard["swgeo"] != 0:
            label = (
                f"$l=\\SI{{{dut.length*1e6:.1f}}}{{\\micro\\metre}},\\,w=\\SI{{{dut.width*1e6:.1f}}}{{\\micro\\metre}},\\,$"
                + label
            )

        for _i_vd, v_d, data_filtered_ds in dataframe.iter_unique_col(self.col_vds, decimals=3):
            for _i_vb, v_b, data_filtered_bs in data_filtered_ds.iter_unique_col(
                self.col_vbs, decimals=3
            ):
                vgs = data_filtered_bs[self.col_vgs].to_numpy().real
                cgs = data_filtered_bs[self.col_cgs].to_numpy().real
                cgd = data_filtered_bs[self.col_cgd].to_numpy().real
                ccg = cgs + cgd
                cgg_cal = data_filtered_bs[self.col_cgg].to_numpy().real
                try:
                    temp = data_filtered_bs[specifiers.TEMPERATURE].to_numpy().real
                except KeyError:
                    temp = t_meas
                line = {
                    "x": vgs,
                    "y": ccg,
                    "vds": v_d.real,
                    "vbs": v_b.real,
                    specifiers.TEMPERATURE: temp,
                    "length": dut.length,
                    "width": dut.width,
                }
                self.data_reference.append(line)
                self.labels.append(
                    label
                    + self.col_vds.to_legend_with_value(v_d.real)
                    + ",\\,"
                    + self.col_vbs.to_legend_with_value(v_b.real)
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
        data_model["y"] = self.extract_ccg(
            vgs=data_model["x"],
            vds=data_model["vds"],
            vbs=data_model["vbs"],
            t_dev=data_model[specifiers.TEMPERATURE],
            width=data_model["width"],
            length=data_model["length"],
            **paras_model.to_kwargs(),
        )
        return data_model

    def extract_ccg(self, vgs, vds, vbs, t_dev, width=0.0, length=0.0, **kwargs):
        kwargs["l"] = length
        kwargs["w"] = width
        # PSP uses uppercase model parameters:
        kwargs = {k.upper(): v for k, v in kwargs.items()}
        voltages = {"br_DT": 0, "br_GPSI": vgs, "br_DISI": vds, "br_SIBP": -vbs}

        # call model function in VerilogAE
        cgg = self.model.functions["Qg_dVg"].eval(temperature=t_dev, voltages=voltages, **kwargs)

        # fringe caps
        cfr = self.model.functions["CFR_i"].eval(temperature=t_dev, voltages=voltages, **kwargs)
        cfrd = self.model.functions["CFRD_i"].eval(temperature=t_dev, voltages=voltages, **kwargs)
        cgov = self.model.functions["CGOV_i"].eval(temperature=t_dev, voltages=voltages, **kwargs)
        cgovd = self.model.functions["CGOVD_i"].eval(temperature=t_dev, voltages=voltages, **kwargs)
        cgbov = self.model.functions["CGBOV_i"].eval(temperature=t_dev, voltages=voltages, **kwargs)

        return cgg + cfr + cfrd + cgov + cgovd + cgbov
