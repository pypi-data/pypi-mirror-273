""" Step to verify the extracted model by simulating and plotting measurement data and simulation data. Also allows global fitting but it is not recommended to fit too many parameters at once.

Author: Mario Krattenmacher | Mario.Krattenmacher@semimod.de
Author: Markus Müller       | Markus.Mueller3@tu-dresden.de
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

from DMT.core import (
    Plot,
    specifiers,
    sub_specifiers,
    Sweep,
    get_sweepdef,
    natural_scales,
    DutTcad,
    DutType,
    DutTypeFlag,
    constants,
)
from DMT.ngspice import DutNgspice
from DMT.core.sweep_def import (
    SweepDefConst,
    SweepDefList,
)
from DMT.extraction import (
    XStep,
    plot,
    find_nearest_index,
    print_to_documentation,
    XQPoaBilinearFull,
    IYNormLog_1,
)
from DMT.extraction.model import memoize

try:
    from DMT.external.pylatex import Tex
    from pylatex import NoEscape
except ImportError:
    pass

# for convenience, we define some specifiers
col_vbe = specifiers.VOLTAGE + ["B", "E"]
col_vse = specifiers.VOLTAGE + ["S", "E"]
col_vbc = specifiers.VOLTAGE + ["B", "C"]
col_vce = specifiers.VOLTAGE + ["C", "E"]
col_ic = specifiers.CURRENT + "C"
col_ib = specifiers.CURRENT + "B"

col_vgs = specifiers.VOLTAGE + ["G", "S"]
col_vgd = specifiers.VOLTAGE + ["G", "D"]
col_vds = specifiers.VOLTAGE + ["D", "S"]
col_vbs = specifiers.VOLTAGE + ["B", "S"]
col_id = specifiers.CURRENT + "D"
col_ig = specifiers.CURRENT + "G"


class XVerify(XStep):
    """XVerify implements parameter extraction steps that require circuit simulation for MOS and BJT
    type devices. Typically these steps are the last part of a parameter extraction flow,
    this is why they are used for "verification and tuning".

    Parameters
    ----------
    same as for XStep, and additionally:

    verify_area_densities : Bool, False
        If True, currents and charges are normalized to the DutView.area for BJT type devices and to the
        device width for MOS type devices. These attributes must be stored in the DutView objects supplied
        to this XStep.
    fit_along           : Specifiers.Current or Specifiers.Voltage or Specifiers.Frequency, default=V_BE|FORCED
        The inner quantity that shall be fitted along.
    inner_sweep_voltage": Specifiers.Current or Specifiers.Voltage, default=V_BE|FORCED
        The inner sweep specifier (voltage or current) that shall be simulated.
    outer_sweep_voltage": Specifiers.Current or Specifiers.Voltage, default=V_BC|FORCED
        The outer sweep specifier (voltage or current) that shall be simulated.
    quantity_fit": None
        The electrical quantity that shall be fitted.
    """

    def __init__(
        self,
        name,
        mcard,
        lib,
        op_definition,
        DutCircuitClass,
        model_deemb_method=None,
        verify_area_densities=False,
        required_specifiers=None,
        **kwargs,
    ):
        if "fit_along" not in kwargs and "inner_sweep_voltage" in kwargs:
            kwargs["fit_along"] = kwargs["inner_sweep_voltage"]

        # init the super class
        super().__init__(
            name,
            mcard,
            lib,
            op_definition,
            DutCircuitClass=DutCircuitClass,
            specifier_paras={
                "fit_along": col_vbe + sub_specifiers.FORCED,
                "inner_sweep_voltage": col_vbe + sub_specifiers.FORCED,
                "outer_sweep_voltage": col_vbc + sub_specifiers.FORCED,
                "quantity_fit": None,
            },
            **kwargs,
        )

        if self.relevant_duts is None:
            self.relevant_duts = [lib.dut_ref]

        self.fit_along = self.specifier_paras["fit_along"]
        self.inner_sweep_voltage = self.specifier_paras["inner_sweep_voltage"]
        self.outer_sweep_voltage = self.specifier_paras["outer_sweep_voltage"]
        self.quantity_fit = self.specifier_paras["quantity_fit"]

        self.iynorm = IYNormLog_1
        self.is_ac = False
        self.model_deemb_method = model_deemb_method
        self.verify_area_densities = verify_area_densities

        # flags that we can use throughout the whole code
        self.is_bjt = self.relevant_duts[0].dut_type.is_subtype(DutTypeFlag.flag_bjt)
        self.is_mos = self.relevant_duts[0].dut_type.is_subtype(DutTypeFlag.flag_mos)

        # define a set of specifiers that we always wish to have next to inner_sweep_voltage, outer_sweep_voltage and quantity_fit (minimum requirement)
        if required_specifiers is None:
            self.required_specifiers = set()
        else:
            self.required_specifiers = set(required_specifiers)

        self.required_specifiers |= {
            self.inner_sweep_voltage,
            self.outer_sweep_voltage,
            self.quantity_fit,
            self.fit_along,
        }

        self.dc_specifiers = set()

        self.ac_specifiers = set()
        self.ac_specifiers.add(specifiers.FREQUENCY)
        self.ac_specifiers.add(specifiers.TRANSIT_FREQUENCY)
        self.ac_specifiers.add(specifiers.TRANSIT_TIME)
        self.ac_specifiers.add(specifiers.MAXIMUM_STABLE_GAIN)
        self.ac_specifiers.add(specifiers.UNILATERAL_GAIN)

        # AC quantities that make no sense for FET, but for BJT:
        if self.is_bjt:
            self.ac_specifiers.add(specifiers.MAXIMUM_OSCILLATION_FREQUENCY)

        if self.is_bjt:
            # bjt specific specifiers
            self.dc_specifiers.add(col_vbe)
            self.dc_specifiers.add(col_vbc)
            self.dc_specifiers.add(col_vce)

            self.dc_specifiers.add(col_vbe + sub_specifiers.FORCED)
            self.dc_specifiers.add(col_vbc + sub_specifiers.FORCED)
            self.dc_specifiers.add(col_vce + sub_specifiers.FORCED)

            self.dc_specifiers.add(col_ic)
            self.dc_specifiers.add(col_ib)
            # self.dc_specifiers.add(specifiers.OUTPUT_CONDUCTANCE)

            self.col_y11 = specifiers.SS_PARA_Y + ["B", "B"]
            self.col_y21 = specifiers.SS_PARA_Y + ["C", "B"]
            self.col_y12 = specifiers.SS_PARA_Y + ["B", "C"]
            self.col_y22 = specifiers.SS_PARA_Y + ["C", "C"]

        elif self.is_mos:
            # mos specific
            self.dc_specifiers.add(col_vgs)
            self.dc_specifiers.add(col_vgd)
            self.dc_specifiers.add(col_vds)

            self.dc_specifiers.add(col_vgs + sub_specifiers.FORCED)
            self.dc_specifiers.add(col_vgd + sub_specifiers.FORCED)
            self.dc_specifiers.add(col_vds + sub_specifiers.FORCED)

            self.dc_specifiers.add(col_id)
            self.dc_specifiers.add(col_ig)

            self.col_y11 = specifiers.SS_PARA_Y + ["G", "G"]
            self.col_y21 = specifiers.SS_PARA_Y + ["D", "G"]
            self.col_y12 = specifiers.SS_PARA_Y + ["G", "D"]
            self.col_y22 = specifiers.SS_PARA_Y + ["D", "D"]

        else:
            raise IOError("DMT->XVerify: Unknown DutType")

        self.ac_specifiers.add(self.col_y11)
        self.ac_specifiers.add(self.col_y21)
        self.ac_specifiers.add(self.col_y12)
        self.ac_specifiers.add(self.col_y22)

        self.ac_specifiers.add(self.col_y11 + sub_specifiers.REAL)
        self.ac_specifiers.add(self.col_y12 + sub_specifiers.REAL)
        self.ac_specifiers.add(self.col_y21 + sub_specifiers.REAL)
        self.ac_specifiers.add(self.col_y22 + sub_specifiers.REAL)

        self.ac_specifiers.add(self.col_y11 + sub_specifiers.IMAG)
        self.ac_specifiers.add(self.col_y12 + sub_specifiers.IMAG)
        self.ac_specifiers.add(self.col_y21 + sub_specifiers.IMAG)
        self.ac_specifiers.add(self.col_y22 + sub_specifiers.IMAG)

        self.ac_specifiers.add(self.col_y21 + sub_specifiers.MAG)
        self.ac_specifiers.add(self.col_y21 + sub_specifiers.PHASE)

        self.additional_tex_description = ""

        # these variables are useful for plotting later, it makes the code generic for BJT and MOS devices
        self.i_unit = 1e3
        self.i_unit_tex = r"\si{\milli\ampere}"
        self.y_im_unit = 1e15
        self.y_im_unit_tex = r"\si{\femto\farad}"
        self.y_re_unit = 1e3
        self.y_re_unit_tex = r"\si{\milli\siemens}"
        if self.is_bjt:
            self.col_v10 = col_vbe + sub_specifiers.FORCED
            self.col_v20 = col_vce + sub_specifiers.FORCED
            self.col_v30 = col_vse + sub_specifiers.FORCED
            self.col_v12 = col_vbc + sub_specifiers.FORCED
            self.col_i2 = col_ic
            self.col_i1 = col_ib
            if self.verify_area_densities:
                self.i_unit = 1e3 / 1e6 / 1e6
                self.i_unit_tex = r"\si{\milli\ampere\per\square\micro\meter}"
                self.y_im_unit = 1e15 / 1e6 / 1e6
                self.y_im_unit_tex = r"\si{\femto\farad\per\square\micro\meter}"
                self.y_re_unit = 1e3 / 1e6 / 1e6
                self.y_re_unit_tex = r"\si{\milli\siemens\per\square\micro\meter}"

        elif self.is_mos:
            self.col_v10 = col_vgs + sub_specifiers.FORCED
            self.col_v20 = col_vds + sub_specifiers.FORCED
            self.col_v30 = col_vbs + sub_specifiers.FORCED
            self.col_v12 = col_vgd + sub_specifiers.FORCED
            self.col_i2 = col_id
            self.col_i1 = col_ig
            if self.verify_area_densities:
                self.i_unit = 1e3 / 1e6
                self.i_unit_tex = r"\si{\milli\ampere\per\micro\meter}"
                self.y_im_unit = 1e15 / 1e6
                self.y_im_unit_tex = r"\si{\femto\farad\per\micro\meter}"
                self.y_re_unit = 1e3 / 1e6
                self.y_re_unit_tex = r"\si{\milli\siemens\per\micro\meter}"

    @plot()
    @print_to_documentation()
    def main_plot(self):
        """Overwrite main plot from parent class."""
        if self.fit_along.specifier == specifiers.FREQUENCY:
            x_scale = 1e-9  # GHz
        else:
            x_scale = 1

        try:
            y_scale = natural_scales[self.quantity_fit.specifier]
        except KeyError:
            y_scale = 1
        try:
            x_scale = natural_scales[self.fit_along.specifier]
        except KeyError:
            x_scale = 1

        y_label = None
        if self.quantity_fit.specifier == specifiers.CURRENT and self.verify_area_densities:
            y_scale = self.i_unit
            y_label = (
                r"$J_{\mathrm{"
                + self.quantity_fit.nodes[0]
                + r"}}\left("
                + self.i_unit_tex
                + r"\right)$"
            )

        if sub_specifiers.REAL in self.quantity_fit or sub_specifiers.MAG in self.quantity_fit:
            y_scale = 1e3
            y_label = "$" + self.quantity_fit.to_tex() + "\\left( \\si{\\milli\\siemens} \\right)$"
            if self.verify_area_densities:
                y_scale = 1e3 / 1e6 / 1e6
                y_label = (
                    "$"
                    + self.quantity_fit.to_tex()
                    + "\\left( \\si{\\milli\\siemens\\per\\square\\micro\\meter} \\right)$"
                )

        # DC log quantity?
        y_log = self.quantity_fit.specifier == specifiers.CURRENT and (
            self.inner_sweep_voltage == self.col_v10 + sub_specifiers.FORCED
            or self.inner_sweep_voltage == self.col_v12 + sub_specifiers.FORCED
            or self.inner_sweep_voltage == self.col_i1
        )

        # AC quantity normalized to omega?
        if sub_specifiers.IMAG in self.quantity_fit:
            y_scale = 1e15
            y_label = (
                "$" + self.quantity_fit.to_tex() + "/\omega\\left( \\si{\\femto\\farad} \\right)$"
            )
            if self.verify_area_densities:
                y_scale = self.y_im_unit
                y_label = (
                    "$"
                    + self.quantity_fit.to_tex()
                    + "/\omega\\left( "
                    + self.y_im_unit_tex
                    + " \\right)$"
                )

        x_log = self.fit_along == specifiers.FREQUENCY or (
            self.fit_along.specifier == specifiers.CURRENT
        )

        main_plot = super(XVerify, self).main_plot(
            r"$ "
            + self.quantity_fit.to_tex()
            + r" \left( "
            + self.fit_along.to_tex()
            + r" \right) $",
            x_specifier=self.fit_along,
            y_specifier=self.quantity_fit,
            y_label=y_label,
            y_scale=y_scale,
            x_scale=x_scale,
            y_log=y_log,
            x_log=x_log,
        )
        # if self.fit_along == specifiers.FREQUENCY: #x axis log bugs
        #   main_plot.x_axis_scale = 'log'
        main_plot.legend_location = "upper left"
        return main_plot

    def ensure_input_correct(self):
        """Search for all required columns in the data frames."""
        # determine if this is an AC verification?
        if not self.is_ac:  # do this only once
            for dut in self.relevant_duts:
                for key in dut.data.keys():
                    if self.validate_key(key):
                        if specifiers.FREQUENCY in dut.data[key].columns:  # AC
                            self.is_ac = True
                            break

                if self.is_ac:  # if it is true, we can stop
                    break

            # ok, we also need AC specifiers
            self.required_specifiers |= self.dc_specifiers
            if self.is_ac:
                self.required_specifiers |= self.ac_specifiers

        # now ensure the required specifiers
        try:
            super().ensure_input_correct()
        except:
            pass

    def ensure_input_correct_per_dataframe(self, dataframe, dut=None, key=None, **_kwargs):
        for specifier in self.required_specifiers:
            try:
                dataframe.ensure_specifier_column(specifier, ports=dut.nodes)
            except:
                pass
                # raise IOError(
                #     "The column "
                #     + specifier
                #     + " could not be calculated. Available columns: "
                #     + str(dut.data[key].columns)
                # ) from err

    def init_data_reference_per_dataframe(self, dataframe, t_meas, dut=None, key=None):
        """Find the required data in the user supplied dataframe or database and write them into data_model attribute of XStep object."""
        col_outer = self.outer_sweep_voltage
        col_inner = self.inner_sweep_voltage

        configs = [dut.contact_config for dut in self.relevant_duts]
        configs = list(set(configs))
        # possible approaches...maybe we need to test which is better
        # one sweep per line:
        # - matches the XStep architecture
        # - can easily account for parasitic metal resistances without putting them into the circuit simulation
        # alternative one sweep for all dataframes (old version):
        # - faster(?) ->maybe big advantage
        # - need all ref data in one df somehow <- not the case for Markus and probably big disadvantage
        # - need to filter the data after the simulation
        # Test which is better!
        area_scale = False
        if (
            self.verify_area_densities
            and (
                self.quantity_fit.specifier == specifiers.CURRENT
                or specifiers.SS_PARA_Y in self.quantity_fit
            )
            and not sub_specifiers.PHASE in self.quantity_fit
        ):
            area_scale = True
            try:
                aeff = XQPoaBilinearFull.get_effective_area(
                    dut.length,
                    dut.width,
                    dlE=self.mcard["dlE"].value,
                    dbE=self.mcard["dbE"].value,
                    gamma_l=self.mcard["gamma_l"].value,
                    gamma_b=self.mcard["gamma_b"].value,
                    recr=self.mcard["recr"].value,
                )
            except:
                aeff = dut.area
            dut.area_effective = aeff
        else:
            dut.area_effective = dut.area

        if col_outer.specifier == specifiers.VOLTAGE.specifier:
            decimals = 3
        else:
            decimals = 5

        for _i, v_outer, data in dataframe.iter_unique_col(col_outer, decimals):
            outputdef = list(self.required_specifiers)
            if self.DutCircuitClass == DutNgspice:
                outputdef.append("OpVar")

            othervar = {specifiers.TEMPERATURE: t_meas}

            if not data.columns.is_unique:
                raise IOError("not unique")

            # in general, col_v30 is the Bulk-Source or Substrate-Emitter voltage. We allow
            # to generate voltage sweeps where v30 has a constant value, too.
            if self.col_v30 != col_outer:
                sweepdef = get_sweepdef(
                    data,
                    inner_sweep_voltage=col_inner,
                    outer_sweep_voltage=col_outer,
                    col_third=self.col_v30,
                )
            else:
                sweepdef = get_sweepdef(
                    data,
                    inner_sweep_voltage=col_inner,
                    outer_sweep_voltage=col_outer,
                    col_third=self.col_v20,
                )

            if self.is_ac:
                sweep_order_f = max([swd.sweep_order for swd in sweepdef]) + 1
                if len(data[specifiers.FREQUENCY].unique()) == 1:
                    sweepdef.append(
                        SweepDefConst(
                            specifiers.FREQUENCY,
                            data[specifiers.FREQUENCY].unique(),
                            sweep_order=sweep_order_f,
                        ),
                    )
                else:
                    # ngspice => should recast this there
                    # raise IOError('NGspice AC sweep not supported in XVerify.')
                    # freqs = data[specifiers.FREQUENCY].unique()
                    # f_min = np.min(freqs)
                    # f_max = np.max(freqs)
                    # n     = len(freqs)
                    # sweepdef.append(
                    #     {'var_name':specifiers.FREQUENCY, 'sweep_order':4, 'sweep_type':'LOG', 'value_def':[f_min,f_max,n]},
                    # )
                    sweepdef.append(
                        SweepDefList(
                            specifiers.FREQUENCY,
                            value_def=data[specifiers.FREQUENCY].unique(),
                            sweep_order=sweep_order_f,
                        )
                    )

            if self.fit_along.specifier in ["V", "I"]:
                line_x, filter_x = np.unique(
                    np.round(data[self.fit_along].to_numpy(), decimals=10),
                    return_index=True,
                )
                line_y = np.real(data[self.quantity_fit].to_numpy())[filter_x]
                if area_scale:
                    if self.is_bjt:
                        line_y = line_y / dut.area_effective
                    elif self.is_mos:
                        line_y = line_y / dut.width

                nfinger = 1
                try:
                    nfinger = dut.ndevices
                except AttributeError:
                    pass

                line = {
                    "x": np.where(line_x == 0, 1e-30, line_x),
                    "y": np.where(line_y == 0, 1e-30, line_y),
                    "length": dut.length,
                    "width": dut.width,
                    "config": dut.contact_config,
                    "nfinger": nfinger,
                    "sweep": Sweep(
                        key.split("/")[-1],
                        sweepdef=sweepdef,
                        outputdef=outputdef,
                        othervar=othervar,
                    ),
                    specifiers.TEMPERATURE: t_meas,
                    "dut_area": dut.area_effective,
                    "area_scale": area_scale,
                }
                for specifier in self.required_specifiers:
                    line[specifier] = data[specifier].to_numpy()[filter_x]

                self.data_reference.append(line)
                if len(self.relevant_duts) == 1:
                    if self.outer_sweep_voltage.specifier == "I":
                        if self.one_t:
                            self.labels.append(
                                f"${self.outer_sweep_voltage.to_tex()}"
                                + r"$ = \SI{"
                                + f"{np.real(data[col_outer].to_numpy()[0])*1e3:.2f}"
                                + r"}{\milli\ampere}, \quad"
                                + f"$T$ = \\SI{{{t_meas:.2f}}}{{\\kelvin}}"
                            )
                        else:
                            self.labels.append(
                                f"${self.outer_sweep_voltage.to_tex()}"
                                + r"$ = \SI{"
                                + f"{np.real(data[col_outer].to_numpy()[0])*1e3:.2f}"
                                + r"}{\milli\ampere}"
                            )
                    else:
                        if self.one_t:
                            self.labels.append(
                                f"${self.outer_sweep_voltage.to_tex()}"
                                + r"$ = \SI{"
                                + f"{np.real(data[col_outer].to_numpy()[0]):.2f}"
                                + r"}{\volt}"
                            )
                        else:
                            self.labels.append(
                                f"${self.outer_sweep_voltage.to_tex()}"
                                + r"$ = \SI{"
                                + f"{np.real(data[col_outer].to_numpy()[0]):.2f}"
                                + r"}{\volt}, \quad "
                                + f"$T$ = \\SI{{{t_meas:.2f}}}{{\\kelvin}}"
                            )
                else:
                    if len(configs) > 1:
                        self.labels.append(
                            dut.contact_config
                            + r", $"
                            + self.outer_sweep_voltage.to_tex()
                            + r" = \SI{"
                            + f"{np.real(data[col_outer].to_numpy()[0]):.2f}"
                            + r"}{\volt}, \left( l_{\mathrm{E0}}, b_{\mathrm{E0}} \right) =\left( "
                            + f"{dut.length * 1e6:.2f}"
                            + ","
                            + f"{dut.width * 1e6:.2f}"
                            + r" \right)\si{\micro\meter} $"
                        )
                    else:
                        self.labels.append(
                            r"$"
                            + self.outer_sweep_voltage.to_tex()
                            + r" = \SI{"
                            + f"{np.real(data[col_outer].to_numpy()[0]):.2f}"
                            + r"}{\volt}, \left( l_{\mathrm{E0}}, b_{\mathrm{E0}} \right) =\left( "
                            + f"{dut.length * 1e6:.2f}"
                            + ","
                            + f"{dut.width * 1e6:.2f}"
                            + r" \right)\si{\micro\meter} $"
                        )
            else:
                # unique inner voltage
                df_inner = data
                df_inner[self.inner_sweep_voltage] = df_inner[self.inner_sweep_voltage].round(
                    3
                )  # cheat
                inner_unique = df_inner[self.inner_sweep_voltage].unique()
                for i_inner, v_inner in enumerate(inner_unique):
                    df_single_inner = df_inner[df_inner[self.inner_sweep_voltage] == v_inner]
                    line_x = df_single_inner[self.fit_along].to_numpy()
                    line_y = np.real(df_single_inner[self.quantity_fit].to_numpy())
                    if area_scale:
                        if self.is_bjt:
                            line_y = line_y / dut.area_effective
                        elif self.is_mos:
                            line_y = line_y / dut.width

                    ndevices = 1
                    try:
                        ndevices = dut.ndevices
                    except AttributeError:
                        pass

                    line = {
                        "x": np.where(line_x == 0, 1e-30, line_x),
                        "y": np.where(line_y == 0, 1e-30, line_y),
                        "length": dut.length,
                        "width": dut.width,
                        "config": dut.contact_config,
                        "nfinger": ndevices,
                        specifiers.TEMPERATURE: t_meas,
                        "dut_area": dut.area_effective,
                        "area_scale": area_scale,
                    }
                    for specifier in self.required_specifiers:
                        line[specifier] = df_single_inner[specifier].to_numpy()

                    # for ImY(f) plots, normalize to omega
                    if (
                        self.fit_along == specifiers.FREQUENCY
                        and sub_specifiers.IMAG in self.quantity_fit
                    ):
                        omega = 2 * np.pi * line["x"]
                        line["y"] = line["y"] / omega

                    # modify the sweep, so that inner sweep voltage becomes constant as well
                    for sub_sweep in sweepdef:
                        # this does not work for BC-BE, only for CE-BE
                        # TODO stupid fix: always manipulate sweep order 3
                        # if sub_sweep['var_name'] == specifiers.VOLTAGE + self.inner_sweep_voltage.nodes[0]:
                        if sub_sweep.sweep_order == 4:
                            sub_sweep.sweep_type = "CONST"
                            if sub_sweep.var_name.nodes[0] == self.inner_sweep_voltage.nodes[0]:
                                sub_sweep.value_def = [inner_unique[i_inner]]
                            elif sub_sweep.var_name.nodes[0] == self.inner_sweep_voltage.nodes[1]:
                                # when the sub sweep potential is the second potential of the sweep voltage -> potential is negative...
                                # this case happens for BC sweeps: B and C are 0, emitter is sweept negative
                                sub_sweep.value_def = [-1 * inner_unique[i_inner]]
                            else:
                                raise IOError(
                                    "DMT->XVerify: The inner sweep voltage nodes are not present in the sweep with order 3. Something bad happend..."
                                )

                    line["sweep"] = Sweep(
                        self.key,
                        sweepdef=sweepdef,
                        outputdef=outputdef,
                        othervar=othervar,
                    )

                    self.data_reference.append(line)
                    if len(self.relevant_duts) == 1:
                        self.labels.append(
                            r"$("
                            + self.outer_sweep_voltage.to_tex()
                            + r","
                            + self.inner_sweep_voltage.to_tex()
                            + r") = ("
                            + f"{np.real(v_outer):.2f}"
                            + r","
                            + f"{np.real(inner_unique[i_inner]):.2f}"
                            + r")\si{\volt} $"
                        )  # ensures nice labels in the plot
                    else:
                        configs = []
                        for dut in self.relevant_duts:
                            try:
                                configs.append(dut.contact_configuration)
                            except AttributeError:
                                configs.append("TBD")
                        self.labels.append(
                            r"$"
                            + self.outer_sweep_voltage.to_tex()
                            + r" = \SI{"
                            + f"{np.real(df_single_inner[col_outer].to_numpy()[0]):.2f}"
                            + r"}{\volt}, \left( l_{\mathrm{E0}}, b_{\mathrm{E0}} \right) =\left( "
                            + f"{dut.length * 1e6:.2f}"
                            + ","
                            + f"{dut.width * 1e6:.2f}"
                            + r" \right)\si{\micro\meter} $"
                        )  # ensures nice labels in the plot

    # ▲▲▲▲▲▲▲
    # These two functions need to go "hand in hand". The temperature that corresponds to each line is needed to allow multidimensional fits.
    # ▾▾▾▾▾▾▾▾

    def fit(self, data_model, paras_model, dut=None):
        """cite from XStep docs:
        | - Return the data_model's y values for the x-values, if the x-step uses a dut+sweep combination.
        |   In this cases, XStep already carried out dut+sweep simulations with the parameters before calling the function. Promised.
        |   Reason: This allows to use DMT's multithreading capabilities, speeding up the extraction significantly.
        """
        try:
            sweep = data_model["sweep"]
            key = dut.join_key(dut.get_sweep_key(sweep), "iv")
            data = dut.data[key]
        except KeyError as err:
            if "data" in locals():
                pass  # in case of key error, use data from line['sweep'] before... Oo
            else:
                raise IOError(
                    "DMT -> XVerify -> {}: probably the simulation of {} went wrong (available keys in dut {}: {}).".format(
                        self.name,
                        dut.get_sweep_key(data_model["sweep"]),
                        dut.get_sim_folder(data_model["sweep"]),
                        dut.data.keys(),
                    )
                ) from err

        # single frequency ?
        for op_definition in self.op_definitions:
            if specifiers.FREQUENCY in op_definition.keys():
                if isinstance(op_definition[specifiers.FREQUENCY], (float, int)):
                    data = data[
                        np.isclose(
                            data[specifiers.FREQUENCY],
                            op_definition[specifiers.FREQUENCY],
                        )
                    ]

        data.ensure_specifier_column(self.quantity_fit, ports=dut.nodes)
        data.ensure_specifier_column(self.outer_sweep_voltage)
        data.ensure_specifier_column(self.inner_sweep_voltage)
        data.ensure_specifier_column(self.fit_along, ports=dut.nodes)

        for specifier in self.required_specifiers:
            data.ensure_specifier_column(specifier, ports=dut.nodes)

        # internal HICUM data, not always possible..
        try:
            data_model[specifiers.TEMPERATURE] = data["TK"].to_numpy()
            data_model[specifiers.TRANSIT_TIME] = data["TF"].to_numpy()
            data_model["CdEi_ddx"] = data["CdEi_ddx"].to_numpy()
            data_model["Cjei"] = data["Cjei"].to_numpy()
            data_model["CdCi_ddx"] = data["CdCi_ddx"].to_numpy()
            data_model["Cjci"] = data["Cjci"].to_numpy()
            data_model["I_CK"] = data["ick"].to_numpy()
            data_model["V_ciei"] = data["Vciei"].to_numpy()
        except KeyError:
            pass

        # apply bounds from reference data to the simulated data
        # ..todo: alternative we could apply the bounds to the sweepdef. Maybe even smarter?
        # ..todo: this should be put into XStep anyway I think, since it could be valid for all steps that use DutCircuit
        if self.fit_along.specifier in ["V", "I"]:
            x_with_bounds = data_model["x"]
            i_min = find_nearest_index(x_with_bounds.min(), data[self.fit_along].to_numpy())
            i_max = find_nearest_index(x_with_bounds.max(), data[self.fit_along].to_numpy())
            if i_min > i_max:
                i_min, i_max = i_max, i_min

            # Markus: realy needed?
            # data = data[i_min:i_max+1]

            data_model["x"] = np.real(data[self.fit_along].to_numpy())
            data_model["y"] = np.real(data[self.quantity_fit].to_numpy())

            data_model[self.outer_sweep_voltage] = data[self.outer_sweep_voltage].to_numpy()
            data_model[self.inner_sweep_voltage] = data[self.inner_sweep_voltage].to_numpy()
            for specifier in self.required_specifiers:
                data_model[specifier] = data[specifier].to_numpy()

        else:
            # unique inner voltage
            df_inner = data
            df_inner[self.inner_sweep_voltage] = df_inner[self.inner_sweep_voltage].round(
                3
            )  # cheat
            inner_unique = df_inner[self.inner_sweep_voltage].unique()
            for v_inner in inner_unique:
                # get correct line :/
                if v_inner != data_model[self.inner_sweep_voltage][0]:
                    continue

                df_single_inner = df_inner[df_inner[self.inner_sweep_voltage] == v_inner]

                x_with_bounds = data_model["x"]
                i_min = find_nearest_index(
                    x_with_bounds.min(), df_single_inner[self.fit_along].to_numpy()
                )
                i_max = find_nearest_index(
                    x_with_bounds.max(), df_single_inner[self.fit_along].to_numpy()
                )
                if i_min > i_max:
                    i_min, i_max = i_max, i_min

                df_single_inner = df_single_inner[i_min : i_max + 1]

                data_model["x"] = np.real(df_single_inner[self.fit_along].to_numpy())
                data_model["y"] = np.real(df_single_inner[self.quantity_fit].to_numpy())

                data_model[self.outer_sweep_voltage] = np.real(
                    df_single_inner[self.outer_sweep_voltage].to_numpy()
                )
                data_model[self.inner_sweep_voltage] = np.real(
                    df_single_inner[self.inner_sweep_voltage].to_numpy()
                )
                # line[specifiers.TEMPERATURE]   = np.real(df_single_inner['TK'].to_numpy())
                for specifier in self.required_specifiers:
                    data_model[specifier] = df_single_inner[specifier].to_numpy()

        data_model["x"] = np.where(data_model["x"] == 0, 1e-30, data_model["x"])  # avoid zero
        data_model["y"] = np.where(data_model["y"] == 0, 1e-30, data_model["y"])  # avoid zero
        if data_model["area_scale"]:
            if self.is_bjt:
                data_model["y"] = data_model["y"] / data_model["dut_area"]
            elif self.is_mos:
                data_model["y"] = data_model["y"] / data_model["width"]

        if self.fit_along == specifiers.FREQUENCY and sub_specifiers.IMAG in self.quantity_fit:
            omega = 2 * np.pi * data_model["x"]
            data_model["y"] = data_model["y"] / omega

        return data_model

    @memoize  # here we memoize calc all, since this is slow with a circuit simulator
    def calc_all(self, *args, **kwargs):
        return super().calc_all(*args, **kwargs)

    def get_tex(self):
        return r"\text{Final verification}"

    def set_initial_guess(self, reference_data):
        pass  # required to overwrite this, however not useful in such a general step

    def get_description(self):
        doc = Tex()
        doc.append(
            NoEscape(
                r"This extraction step compares $"
                + self.quantity_fit.to_tex()
                + r"$ as a function of $"
                + self.inner_sweep_voltage.to_tex()
                + r"$ at different $"
                + self.outer_sweep_voltage.to_tex()
                + r"$ from measurements vs. full compact model circuit simulations."
            )
        )
        if self.additional_tex_description:
            doc.append(NoEscape(self.additional_tex_description))

        return doc

    # from here on in the code, we define some generic plots:

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_i1(self):
        y_col = self.col_i1
        x_col = self.inner_sweep_voltage
        y_label = r"$" + self.col_i1.to_tex() + r"\left(" + self.i_unit_tex + r"\right)$"
        y_scale = self.i_unit

        if self.is_bjt:
            name = " verify ib"
        elif self.is_mos:
            name = " verify ig"
        sub_plot = Plot(
            f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
            style="xtraction_color",
            num=self.name + name,
            x_specifier=x_col,
            y_specifier=y_col,
            y_label=y_label,
            x_scale=1,
            y_scale=y_scale,
            y_log=True,
        )
        sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_y=True)

        return sub_plot

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_go(self):
        y_col = specifiers.OUTPUT_CONDUCTANCE
        x_col = self.inner_sweep_voltage
        y_label = r"$g_{\mathrm{o}}\left(" + self.y_re_unit_tex + r"\right)$"
        y_scale = self.y_re_unit
        sub_plot = Plot(
            f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
            style="xtraction_color",
            num=self.name + " verify go",
            x_specifier=x_col,
            y_specifier=y_col,
            y_label=y_label,
            x_scale=1,
            y_scale=y_scale,
            y_log=True,
        )
        sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_y=True)

        return sub_plot

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_gm(self):
        y_col = specifiers.TRANSCONDUCTANCE
        x_col = self.inner_sweep_voltage
        i_col = self.col_i2

        sub_plot = Plot(
            r"$ " + y_col.to_tex() + r" \left( " + x_col.to_tex() + r" \right) $",
            style="xtraction_color",
            num=self.name + " verify gm",
            x_specifier=x_col,
            y_specifier=y_col,
            x_scale=1,
            y_scale=1,
            y_log=True,
        )
        try:
            for line_reference, line_model, label in zip(
                self.data_reference, self.data_model, self.labels
            ):  # add the reference and model data in an alternating way
                sub_plot.add_data_set(
                    line_reference[x_col],
                    np.gradient(line_reference[i_col], line_reference[x_col]),
                    label=None if self.legend_off else label,
                )
                sub_plot.add_data_set(
                    line_model[x_col], np.gradient(line_model[i_col], line_model[x_col])
                )

            return sub_plot

        except KeyError:
            return None

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_gm_ic(self):
        y_col = specifiers.TRANSCONDUCTANCE
        i_col = self.col_i2
        v_col = self.inner_sweep_voltage
        x_col = specifiers.CURRENT + "C"

        sub_plot = Plot(
            r"$ " + y_col.to_tex() + r" \left( " + x_col.to_tex() + r" \right) $",
            style="xtraction_color",
            num=self.name + " verify gm",
            x_specifier=x_col,
            y_specifier=y_col,
            x_scale=1,
            y_scale=1,
            x_log=True,
            y_log=True,
        )
        try:
            for line_reference, line_model, label in zip(
                self.data_reference, self.data_model, self.labels
            ):  # add the reference and model data in an alternating way
                sub_plot.add_data_set(
                    line_reference[x_col],
                    np.gradient(line_reference[i_col], line_reference[v_col]),
                    label=None if self.legend_off else label,
                )
                sub_plot.add_data_set(
                    line_model[x_col], np.gradient(line_model[i_col], line_model[v_col])
                )

            return sub_plot

        except KeyError:
            return None

    def plot_beta(self):
        y_col = self.col_i2
        y_col2 = self.col_i1
        x_col = self.inner_sweep_voltage
        sub_plot = Plot(
            r"$ \beta \left( " + x_col.to_tex() + r" \right) $",
            style="xtraction",
            num=self.name + " verify beta",
            x_specifier=x_col,
            y_label=r"$\beta$",
            x_scale=1,
            y_scale=1,
            y_log=True,
        )
        try:
            for line_reference, line_model, label in zip(
                self.data_reference, self.data_model, self.labels
            ):  # add the reference and model data in an alternating way
                if self.legend_off:
                    sub_plot.add_data_set(
                        line_reference[x_col], line_reference[y_col] / line_reference[y_col2]
                    )
                    sub_plot.add_data_set(line_model[x_col], line_model[y_col] / line_model[y_col2])
                else:
                    sub_plot.add_data_set(
                        line_reference[x_col],
                        line_reference[y_col] / line_reference[y_col2],
                        label=label,
                    )
                    sub_plot.add_data_set(line_model[x_col], line_model[y_col] / line_model[y_col2])

            return sub_plot

        except KeyError:
            return None

    # @plot()
    def plot_T(self):
        # plot of self heating from circuit simulator
        style = "color" if self.model is None else "xtraction_color"
        style = "mix"
        x_col = col_ic
        x_col = self.inner_sweep_voltage
        y_col = specifiers.TEMPERATURE  # needs to be in the verilog file, only works with ads
        sub_plot = Plot(
            "T(V_BE)",
            style=style,
            num=self.name + " verify T",
            x_specifier=x_col,
            y_label=r"$T/\si{\kelvin}$",
        )

        for line_reference, line_model, label in zip(
            self.data_reference, self.data_model, self.labels
        ):  # add the reference and model data in an alternating way
            # if self.legend_off:
            sub_plot.add_data_set(line_model[x_col], line_model[y_col])
            # else:
            #     sub_plot.add_data_set(line_model[x_col], line_model[y_col], label="HICUM " + label)

            # if self.model is not None:
            #     p = line_reference["I_C"] * (
            #         line_reference["V_C"] - line_reference["V_E"]
            #     ) + line_reference["I_B"] * (line_reference["V_B"] - line_reference["V_E"])
            #     t_dev = line_reference[specifiers.TEMPERATURE] + self.model.find_dtj(
            #         t_dev=line_reference[specifiers.TEMPERATURE], p=p, **self.mcard.to_kwargs()
            #     )
            #     if self.legend_off:
            #         sub_plot.add_data_set(line_reference[x_col], t_dev)
            #     else:
            #         sub_plot.add_data_set(line_reference[x_col], t_dev, label="model " + label)

        sub_plot.legend_location = "upper left"
        return sub_plot

    def add_data_to_plot(self, plot_obj, x_col, y_col, area_x=False, area_y=False, omega=False):
        """This method adds x and y-axis data from self.data_reference and self.line_model to the plot object "plot_obj".

        Parameters
        -----------
        plot_obj : DMT.Plot
            This is the plot to which the lines shall be added.
        x_col : string or DMT.specifier
            This is the key for the x-axis data in self.data_reference and self.data_model.
        y_col : string or DMT.specifier
            This is the key for the y-axis data in self.data_reference and self.data_model.
        area_x : Bool, False
            If True, the x-axis data is normalized to the device area (BJT) or device width (MOS).
        area_y : Bool, False
            If True, the y-axis data is normalized to the device area (BJT) or device width (MOS).
        omega : Bool, False
            If True, the y-axis data is normalized to the angular frequency.
        """
        norm_x = 1
        norm_y = 1

        if self.is_bjt:
            key_dens = "dut_area"
        elif self.is_mos:
            key_dens = "width"

        for line_reference, line_model, label in zip(
            self.data_reference, self.data_model, self.labels
        ):  # add the reference and model data in an alternating way
            if self.verify_area_densities:
                if area_x:
                    norm_x = line_reference[key_dens]
                if area_y:
                    norm_y = line_reference[key_dens]

            omega_array = 1
            if omega:
                omega_array = line_reference["FREQ"] * 2 * np.pi

            try:
                plot_obj.add_data_set(
                    line_reference[x_col] / norm_x,
                    line_reference[y_col] / norm_y / omega_array,
                    label=None if self.legend_off else label,
                )
            except KeyError:
                pass

            omega_array = 1
            if omega:
                omega_array = line_reference["FREQ"] * 2 * np.pi

            try:
                plot_obj.add_data_set(
                    line_model[x_col] / norm_x, line_model[y_col] / norm_y / omega_array
                )
            except KeyError:
                pass

        return plot_obj

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_i2(self):
        y_col = self.col_i2
        x_col = self.inner_sweep_voltage
        y_label = r"$" + y_col.to_tex() + r"\left(" + self.i_unit_tex + r"\right)$"
        y_scale = self.i_unit
        sub_plot = Plot(
            f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
            style="xtraction_color",
            num=self.name + " verify ic",
            x_specifier=x_col,
            y_specifier=y_col,
            y_label=y_label,
            x_scale=1,
            y_scale=y_scale,
            y_log=True,
        )
        sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_y=True)

        return sub_plot

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_ft(self):
        x_col = self.col_i2
        y_col = specifiers.TRANSIT_FREQUENCY
        x_label = r"$" + x_col.to_tex() + r"\left(" + self.i_unit_tex + r"\right)$"
        x_scale = self.i_unit
        sub_plot = Plot(
            r"$ " + y_col.to_tex() + r" \left( " + x_col.to_tex() + r" \right) $",
            style="xtraction_color",
            num=self.name + " verify ft",
            x_label=x_label,
            y_specifier=y_col,
            x_scale=x_scale,  # 1e3,
            y_scale=1e-9,
            x_log=True,
            legend_location="upper left",
        )
        sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True)

        return sub_plot

    def get_plt_y(self, y_col, real=False):
        """Generic method that generates a plot for the given y-Parameter y_col.

        Parameters
        ----------
        y_col : DMT.core.SpecifierStr
            A Specifier that should correspond to a Y-parameter.
        real  : Bool, False
            If True, plot a real part, else an imaginary part.
        """
        if not self.is_ac:
            return None

        x_col = self.fit_along
        x_log = False
        y_log = False

        if real:
            y_log = True

        y_col_tex = y_col.to_tex()

        if x_col == self.col_v10 or x_col == self.col_v10 + sub_specifiers.FORCED:
            x_col = self.col_i2
            x_log = True
        if self.verify_area_densities:
            x_label = r"$" + self.col_i2.to_tex() + r"\left( " + self.i_unit_tex + r" \right)$"
            x_scale = self.i_unit
        else:
            x_scale = natural_scales[x_col.specifier]
            x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)

        if real:
            if self.verify_area_densities:
                y_label = r"$" + y_col_tex + r" \left( " + self.y_re_unit_tex + r" \right)$"
                y_scale = self.y_re_unit
            else:
                y_label = r"$" + y_col_tex + r" \left( \si{\milli\ampere} \right)$"
                y_scale = 1e3  # mA

        else:  # imaginary, divided by angular frequency omega=2pif
            if self.verify_area_densities:
                y_label = r"$" + y_col_tex + r"/\omega \left( " + self.y_im_unit_tex + r" \right)$"
                y_scale = self.y_im_unit
            else:
                y_label = r"$" + y_col_tex + r"/\omega \left( \si{\femto\farad} \right)$"
                y_scale = 1e15  # fF

        # if the Y specifier is of kind "phase", we must modify y_label and y_scale
        if sub_specifiers.PHASE in y_col:
            y_label = r"$" + y_col_tex + r"/\omega \left( \si{\degree} \right)$"
            y_scale = 1

        sub_plot = Plot(
            f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
            style="xtraction_color",
            num=self.name + r" verify " + y_col.to_tex() + r" im",
            x_label=x_label,
            y_label=y_label,
            y_specifier=y_col,
            x_scale=x_scale,
            y_scale=y_scale,
            x_log=x_log,
            y_log=y_log,
            legend_location="upper left",
        )
        sub_plot = self.add_data_to_plot(
            sub_plot, x_col, y_col, area_x=True, area_y=True, omega=True
        )

        return sub_plot

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_rey12(self):
        return self.get_plt_y(self.col_y12 + sub_specifiers.REAL, real=True)

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_magy21(self):
        return self.get_plt_y(self.col_y21 + sub_specifiers.MAG, real=True)

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_rey22(self):
        return self.get_plt_y(self.col_y22 + sub_specifiers.REAL, real=True)

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_rey11(self):
        return self.get_plt_y(self.col_y11 + sub_specifiers.REAL, real=True)

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_phasey21(self):
        return self.get_plt_y(self.col_y21 + sub_specifiers.PHASE)

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_imy11(self):
        return self.get_plt_y(self.col_y11 + sub_specifiers.IMAG)

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_imy22(self):
        return self.get_plt_y(self.col_y22 + sub_specifiers.IMAG)

    @plot()
    @print_to_documentation(print_to_documentation=False)
    def plot_imy12(self):
        return self.get_plt_y(self.col_y12 + sub_specifiers.IMAG)

    @plot(plot_to_gui=True)
    @print_to_documentation(print_to_documentation=False)
    def plot_fmax(self):
        if self.is_mos:
            return None

        x_col = self.col_i2
        y_col = specifiers.MAXIMUM_OSCILLATION_FREQUENCY
        x_label = r"$J_{\mathrm{C}}\left(" + self.i_unit_tex + r"\right)$"
        x_scale = self.i_unit
        sub_plot = Plot(
            r"$ " + y_col.to_tex() + r" \left( " + x_col.to_tex() + r" \right) $",
            style="xtraction_color",
            num=self.name + " verify fmax",
            x_label=x_label,
            y_specifier=y_col,
            x_scale=x_scale,
            y_scale=1e-9,
            x_log=True,
            legend_location="upper left",
        )
        if issubclass(type(self.lib.dut_ref), DutTcad):
            return sub_plot

        sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True)

        return sub_plot

    @plot(plot_to_gui=False)
    @print_to_documentation(print_to_documentation=False)
    def plot_tf(self):
        if self.is_mos:
            return None
        x_col = col_ic
        y_col = specifiers.TRANSIT_TIME
        if self.verify_area_densities:
            x_label = r"$J_{\mathrm{C}}/\si{\milli\ampere\per\square\micro\meter}$"
            x_scale = 1e3 / (1e6 * 1e6)
        else:
            x_label = r"$I_{\mathrm{C}}/\si{\milli\ampere}$"
            x_scale = 1e3
        sub_plot = Plot(
            r"$ \tau_{\mathrm{f}} \left( J_{\mathrm{C}} \right) $",
            style="xtraction_color",
            num=self.name + " verify tf",
            x_label=x_label,
            y_label=r"$\tau_{\mathrm{f}}\left( \si{\pico\second} \right)$",
            y_scale=1e12,
            x_scale=x_scale,
            x_log=False,
            legend_location="upper left",
        )

        sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True)

        return sub_plot

    @plot(plot_to_gui=False)
    @print_to_documentation(print_to_documentation=False)
    def plot_gm_norm_vs_log_jc(self):
        if self.is_mos:
            return None

        if self.verify_area_densities:
            x_label = r"$J_{\mathrm{C}}/\si{\milli\ampere\per\square\micro\meter}$"
            x_scale = 1e3  # / (1e6 * 1e6)
        else:
            x_label = r"$I_{\mathrm{C}}/\si{\milli\ampere}$"
            x_scale = 1e3
        sub_plot = Plot(
            r"$ g_{\mathrm{m,norm}} \left( J_{\mathrm{C}} \right) $",
            style="xtraction_color",
            num=self.name + " verify gm_nom(JC)",
            x_label=x_label,
            y_label=r"$g_{\mathrm{m}}V_T/J_{\mathrm{C}}$",
            y_scale=1,
            x_scale=x_scale,
            x_log=True,
            legend_location="upper left",
        )

        sp_gm = specifiers.TRANSCONDUCTANCE
        sp_ic = specifiers.CURRENT + "C"
        sp_vbe = specifiers.VOLTAGE + ["B", "E"]
        sp_t = specifiers.TEMPERATURE

        for line_reference, line_model, label in zip(
            self.data_reference, self.data_model, self.labels
        ):  # add the reference and model data in an alternating way
            try:
                v_t_ref = constants.calc_VT(line_reference[sp_t])
            except KeyError:
                v_t_ref = constants.vT_300
            gm = np.gradient(line_reference[sp_ic], line_reference[sp_vbe])

            sub_plot.add_data_set(
                line_reference[sp_ic],
                gm * v_t_ref / line_reference[sp_ic],
                label=None if self.legend_off else label,
            )

            try:
                v_t_mod = constants.calc_VT(line_model[sp_t])
            except KeyError:
                v_t_mod = constants.vT_300
            gm = np.gradient(line_model[sp_ic], line_model[sp_vbe])

            sub_plot.add_data_set(line_model[sp_ic], gm * v_t_mod / line_model[sp_ic])

        return sub_plot

    def get_dut(self, line, paras_model):
        """Overwritten from XStep. See doc in XStep."""
        dut = self.DutCircuitClass(
            database_dir=self.circuit_database_dir,
            dut_type=self.relevant_duts[0].dut_type,
            input_circuit=paras_model,
            technology=self.technology,
            width=line["width"],
            length=line["length"],
            contact_config=line["config"],
            nfinger=line["nfinger"],
            reference_node=self.relevant_duts[0].reference_node,
            get_circuit_arguments=self.get_circuit_arguments,
            sim_dir=self.circuit_sim_dir,
            copy_va_files=False,
            # list_copy      = [self.mcard.va_file],# very slow!
        )
        return dut
