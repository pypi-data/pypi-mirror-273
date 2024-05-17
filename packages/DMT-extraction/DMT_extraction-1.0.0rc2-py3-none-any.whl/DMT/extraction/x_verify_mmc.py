""" Step to verify the extracted model by simulating and plotting measurement data and simulation data. Also allows global fitting but it is not recommended to fit too many parameters at once.

This XVerify allows multiple modelcards and even no reference data.

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
from typing import List
from cycler import cycler

from DMT.core import (
    Plot,
    specifiers,
    sub_specifiers,
    Sweep,
    natural_scales,
    MCard,
)
from DMT.exceptions import DataReferenceEmpty
from DMT.extraction import (
    XVerify,
    plot,
    find_nearest_index,
    print_to_documentation,
)

try:
    from DMT.external.pylatex import Tex
    from pylatex import NoEscape
except ImportError:
    pass


class XVerifyMMC(XVerify):
    """XVerify step with mutliple modelcards and optional reference data

    Parameters
    ----------
    sweep : Sweep, optional
    """

    def __init__(
        self,
        *args,
        sweeps: List[Sweep] = None,
        modelcards_other: List[MCard] = None,
        names_other: List[str] = None,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        if sweeps is None:
            self.sweeps = []
        else:
            self.sweeps = sweeps
        if modelcards_other is None:
            self.modelcards_other = []
        else:
            self.modelcards_other = modelcards_other
        if names_other is None:
            self.names_other = [f"other {i_mc}" for i_mc in range(len(self.modelcards_other))]
        else:
            self.names_other = names_other
        self.lines_other = []
        self.labels_other = []

    @plot()
    @print_to_documentation()
    def main_plot(self):
        """Overwrite main plot."""
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
            y_scale = 1e3 / (1e6 * 1e6)  # mA/um^2
            y_label = (
                r"$J_{\mathrm{"
                + self.quantity_fit.nodes[0]
                + r"}}\left(\si{\milli\ampere\per\square\micro\meter}\right)$"
            )

        # DC log quantity?
        y_log = self.quantity_fit.specifier == specifiers.CURRENT and (
            self.inner_sweep_voltage == specifiers.VOLTAGE + "B" + "E" + sub_specifiers.FORCED
            or self.inner_sweep_voltage == specifiers.VOLTAGE + "B" + "C" + sub_specifiers.FORCED
        )

        # AC log quantity?
        y_log = y_log or sub_specifiers.IMAG in self.quantity_fit

        x_log = (
            self.fit_along == specifiers.FREQUENCY or self.fit_along.specifier == specifiers.CURRENT
        )

        self.main_fig = Plot(
            f"$ {self.quantity_fit.to_tex()} \\left( {self.fit_along.to_tex()} \\right) $",
            style="xtraction_color",
            x_specifier=self.fit_along,
            y_specifier=self.quantity_fit,
            y_label=y_label,
            x_scale=x_scale,
            x_log=x_log,
            y_log=y_log,
            y_scale=y_scale,
            num=self.name,
            legend_location="upper left",
        )

        for line_reference, line_model, label in zip(
            self.data_reference, self.data_model, self.labels
        ):  # add the reference and model data in an alternating way
            if self.legend_off:
                self.main_fig.add_data_set(line_reference["x"], line_reference["y"])
                self.main_fig.add_data_set(line_model["x"], line_model["y"])

            else:
                self.main_fig.add_data_set(
                    line_reference["x"], line_reference["y"], label="reference " + label
                )
                self.main_fig.add_data_set(line_model["x"], line_model["y"], label=None)

        for line_other, label_other in zip(self.lines_other, self.labels_other):
            self.main_fig.add_data_set(
                line_other["x"],
                line_other["y"],
                label=label_other,
                style=line_other["linestyle"],
            )

        return self.main_fig

    def init_data(self):
        # must overwrite to turn off some checks
        self.inited_data = False
        self.data_reference = []
        self.data_model = []
        self.labels = []
        self.collect_data()

        # # check if any data has been found
        # found = False
        # for dut in self.relevant_duts:
        #     for key in dut.data:
        #         if self.validate_key(key):
        #             found = True
        #             break
        # if not found:
        #     raise IOError(f"XStep with name {self.name} did not find any suitable data.")

        # check if data contains what is needed and add to data_reference
        self.ensure_input_correct()
        self.init_data_reference()

        if not self.data_reference:
            raise DataReferenceEmpty(f"The data reference of the step {self.name} are empty.")

    # only need to take care for case of no reference data
    def init_data_reference(self):
        """Overwrite to allow passing a sweep directly"""
        self.lines_other = []
        self.labels_other = []
        if not self.sweeps:
            super().init_data_reference()
        elif not self.modelcards_other:
            raise IOError("Neither sweep nor other modelcards given -> use the usual XVerify!")
        else:
            # inside this variant we can always assume AC
            if not self.is_ac:
                self.is_ac = True
                self.required_specifiers |= self.ac_specifiers

            # generate the reference data from the first other modelcard
            col_outer = self.outer_sweep_voltage
            col_inner = self.inner_sweep_voltage
            i_mc = 0

            # create a list of duts and simulate them with DMT
            dut_ref = self.get_dut(None, self.modelcards_other[0])

            # scale the modelcards now
            if self.technology is not None:  # no technology -> no scaling
                dut_ref.scale_modelcard()

            self.sim_con.clear_sim_list()  # reset the sim_list
            self.sim_con.append_simulation(dut=dut_ref, sweep=self.sweeps)
            self.sim_con.run_and_read(force=False)  # run the simulation

            for sweep in self.sweeps:
                data = dut_ref.get_data(sweep=sweep, key="iv")
                t_meas = sweep.othervar[specifiers.TEMPERATURE]

                # single frequency ?
                for op_definition in self.op_definitions:
                    if specifiers.FREQUENCY in op_definition.keys():
                        if isinstance(op_definition[specifiers.FREQUENCY], (float, int)):
                            data = data[
                                np.isclose(
                                    data[specifiers.FREQUENCY], op_definition[specifiers.FREQUENCY]
                                )
                            ]

                data.ensure_specifier_column(self.quantity_fit, ports=self.relevant_duts[0].nodes)
                data.ensure_specifier_column(self.outer_sweep_voltage)
                data.ensure_specifier_column(self.inner_sweep_voltage)
                data.ensure_specifier_column(self.fit_along, ports=self.relevant_duts[0].nodes)

                for specifier in self.required_specifiers:
                    data.ensure_specifier_column(specifier, ports=self.relevant_duts[0].nodes)

                # internal HICUM data, not always possible..
                try:
                    t_dev = data["TK"].to_numpy()
                except KeyError:
                    t_dev = t_meas

                if self.fit_along.specifier in ["V", "I"]:
                    line_x, filter_x = np.unique(
                        np.round(data[self.fit_along].to_numpy(), decimals=10), return_index=True
                    )
                    line_y = np.real(data[self.quantity_fit].to_numpy())[filter_x]

                    line = {
                        "x": np.where(line_x == 0, 1e-30, line_x),
                        "y": np.where(line_y == 0, 1e-30, line_y),
                        "sweep": sweep,
                        specifiers.TEMPERATURE: t_dev,
                        "area_scale": False,
                    }
                    for specifier in self.required_specifiers:
                        line[specifier] = data[specifier].to_numpy()[filter_x]

                    self.data_reference.append(line)
                    if self.outer_sweep_voltage.specifier == "I":
                        self.labels.append(
                            f"{self.names_other[i_mc]}: ${self.outer_sweep_voltage.to_tex()}"
                            + r" = \SI{"
                            + f"{data[col_outer].to_numpy()[0]*1e3:.2f}"
                            + r"}{\milli\ampere} T=\SI{"
                            + f"{t_meas:.2f}"
                            + r"}{\kelvin}$"
                        )  # ensures nice labels in the plot
                    else:
                        self.labels.append(
                            f"{self.names_other[i_mc]}: ${self.outer_sweep_voltage.to_tex()}"
                            + r" = \SI{"
                            + f"{data[col_outer].to_numpy()[0]:.2f}"
                            + r"}{\volt} T=\SI{"
                            + f"{t_meas:.2f}"
                            + r"}{\kelvin}$"
                        )  # ensures nice labels in the plot

                else:
                    # unique inner voltage
                    v_outer = data[self.outer_sweep_voltage].unique()
                    for i_inner, v_inner, df_inner in data.iter_unique_col(
                        self.inner_sweep_voltage, decimals=3
                    ):
                        line_x = df_inner[self.fit_along].to_numpy()
                        line_y = np.real(df_inner[self.quantity_fit].to_numpy())

                        line = {
                            "x": np.where(line_x == 0, 1e-30, line_x),
                            "y": np.where(line_y == 0, 1e-30, line_y),
                            specifiers.TEMPERATURE: t_dev,
                            "sweep": sweep,
                            "area_scale": False,
                        }
                        for specifier in self.required_specifiers:
                            line[specifier] = df_inner[specifier].to_numpy()

                        self.data_reference.append(line)
                        self.labels.append(
                            f"{self.names_other[i_mc]}: $({self.outer_sweep_voltage.to_tex()},{+ self.inner_sweep_voltage.to_tex()} ) = ("
                            + f"{v_outer:.2f},{v_inner:.2f}"
                            + r")\si{\volt} $"
                        )  # ensures nice labels in the plot

        # if self.sweeps:
        #     i_color = len(self.lines_other) // (len(self.modelcards_other) - 1)
        # else:
        #     i_color = len(self.lines_other) // len(self.modelcards_other)
        colors = [
            "#006400",  # darkgreen
            "#00008b",  # darkblue
            "#b03060",  # maroon3
            "#ff0000",  # red
            "#9467bd",  # yellow -> replaced by violett/brown combo
            "#deb887",  # curlywood
            "#00ff00",  # lime
            "#00ffff",  # aqua
            "#ff00ff",  # fuchsia
            "#6495ed",  # cornflower
        ]  # [i_color % 10]
        linestyles = ["-", "--", "-.", ":"]

        duts = []
        sweeps = [line["sweep"] for line in self.data_reference]

        for i_mc, mc_other in enumerate(self.modelcards_other):
            if i_mc == 0 and self.sweeps:
                duts.append(None)  # index for duts same as in modelcards_other
                continue  # already used as fake reference

            # create a list of duts and simulate them with DMT
            dut_other = self.get_dut(None, mc_other)

            # scale the modelcards now
            if self.technology is not None:  # no technology -> no scaling
                dut_other.scale_modelcard()

            self.sim_con.append_simulation(dut=dut_other, sweep=sweeps)
            duts.append(dut_other)

        self.sim_con.run_and_read(force=False)  # run the simulation

        for i_mc, mc_other in enumerate(self.modelcards_other):
            if i_mc == 0 and self.sweeps:
                continue  # already used as fake reference

            dut_other = duts[i_mc]

            for i_sweep, sweep in enumerate(sweeps):
                i_color = i_sweep % len(colors)
                data = dut_other.get_data(sweep=sweep, key="iv")
                t_meas = sweep.othervar[specifiers.TEMPERATURE]

                # single frequency ?
                for op_definition in self.op_definitions:
                    if specifiers.FREQUENCY in op_definition.keys():
                        if isinstance(op_definition[specifiers.FREQUENCY], (float, int)):
                            data = data[
                                np.isclose(
                                    data[specifiers.FREQUENCY], op_definition[specifiers.FREQUENCY]
                                )
                            ]

                data.ensure_specifier_column(self.quantity_fit, ports=self.relevant_duts[0].nodes)
                data.ensure_specifier_column(self.outer_sweep_voltage)
                data.ensure_specifier_column(self.inner_sweep_voltage)
                data.ensure_specifier_column(self.fit_along, ports=self.relevant_duts[0].nodes)

                for specifier in self.required_specifiers:
                    data.ensure_specifier_column(specifier, ports=self.relevant_duts[0].nodes)

                # internal HICUM data, not always possible..
                try:
                    t_dev = data["TK"].to_numpy()
                except KeyError:
                    t_dev = t_meas

                if self.fit_along.specifier in ["V", "I"]:
                    line_x, filter_x = np.unique(
                        np.round(data[self.fit_along].to_numpy(), decimals=10), return_index=True
                    )
                    line_y = np.real(data[self.quantity_fit].to_numpy())[filter_x]

                    line = {
                        "x": np.where(line_x == 0, 1e-30, line_x),
                        "y": np.where(line_y == 0, 1e-30, line_y),
                        "sweep": sweep,
                        specifiers.TEMPERATURE: t_dev,
                        "linestyle": linestyles[i_mc % len(linestyles)] + colors[i_color],
                        "mc": mc_other,
                    }
                    for specifier in self.required_specifiers:
                        line[specifier] = data[specifier].to_numpy()[filter_x]

                    self.lines_other.append(line)
                    if self.outer_sweep_voltage.specifier == "I":
                        self.labels_other.append(
                            f"{self.names_other[i_mc]}: ${self.outer_sweep_voltage.to_tex()}"
                            + r" = \SI{"
                            + f"{data[self.outer_sweep_voltage].to_numpy()[0]*1e3:.2f}"
                            + r"}{\milli\ampere} T=\SI{"
                            + f"{t_meas:.2f}"
                            + r"}{\kelvin}$"
                        )  # ensures nice labels in the plot
                    else:
                        self.labels_other.append(
                            f"{self.names_other[i_mc]}: ${self.outer_sweep_voltage.to_tex()}"
                            + r" = \SI{"
                            + f"{data[self.outer_sweep_voltage].to_numpy()[0]:.2f}"
                            + r"}{\volt} T=\SI{"
                            + f"{t_meas:.2f}"
                            + r"}{\kelvin}$"
                        )  # ensures nice labels in the plot

                else:
                    v_outer = data[self.outer_sweep_voltage].unique()
                    for i_inner, v_inner, df_inner in data.iter_unique_col(
                        self.inner_sweep_voltage, decimals=3
                    ):
                        # get correct line :/
                        if not np.isclose(
                            v_inner, data_model[self.inner_sweep_voltage][0], atol=1e-3
                        ):
                            continue

                        line_x = df_inner[self.fit_along].to_numpy()
                        line_y = np.real(df_inner[self.quantity_fit].to_numpy())

                        line = {
                            "x": np.where(line_x == 0, 1e-30, line_x),
                            "y": np.where(line_y == 0, 1e-30, line_y),
                            specifiers.TEMPERATURE: t_meas,
                            "sweep": sweep,
                            "linestyle": linestyles[i_mc % len(linestyles)] + colors[i_color],
                            "mc": mc_other,
                        }
                        for specifier in self.required_specifiers:
                            line[specifier] = df_inner[specifier].to_numpy()
                        self.lines_other.append(line)

                        self.labels_other.append(
                            f"{self.names_other[i_mc]}: $({self.outer_sweep_voltage.to_tex()},{+ self.inner_sweep_voltage.to_tex()} ) = ("
                            + f"{v_outer:.2f},{v_inner:.2f}"
                            + r")\si{\volt} $"
                        )  # ensures nice labels in the plot

                        break  # only done once for correct v_inner

    # # ▲▲▲▲▲▲▲
    # # These two functions need to go "hand in hand". The temperature that corresponds to each line is needed to allow multidimensional fits.
    # # ▾▾▾▾▾▾▾▾

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
                        np.isclose(data[specifiers.FREQUENCY], op_definition[specifiers.FREQUENCY])
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
        except KeyError:
            pass

        if self.fit_along.specifier in ["V", "I"]:
            data_model["x"] = np.real(data[self.fit_along].to_numpy())
            data_model["y"] = np.real(data[self.quantity_fit].to_numpy())

            data_model[self.outer_sweep_voltage] = data[self.outer_sweep_voltage].to_numpy()
            data_model[self.inner_sweep_voltage] = data[self.inner_sweep_voltage].to_numpy()
            for specifier in self.required_specifiers:
                data_model[specifier] = data[specifier].to_numpy()

        else:
            v_outer = data[self.outer_sweep_voltage].unique()
            for i_inner, v_inner, df_inner in data.iter_unique_col(
                self.inner_sweep_voltage, decimals=3
            ):
                # get correct line :/
                if not np.isclose(v_inner, data_model[self.inner_sweep_voltage][0], atol=1e-3):
                    continue

                data_model["x"] = np.real(df_inner[self.fit_along].to_numpy())
                data_model["y"] = np.real(df_inner[self.quantity_fit].to_numpy())

                data_model[self.outer_sweep_voltage] = np.real(
                    df_inner[self.outer_sweep_voltage].to_numpy()
                )
                data_model[self.inner_sweep_voltage] = np.real(
                    df_inner[self.inner_sweep_voltage].to_numpy()
                )
                for specifier in self.required_specifiers:
                    data_model[specifier] = df_inner[specifier].to_numpy()
                break  # done only once for correct v_inner

        data_model["x"] = np.where(data_model["x"] == 0, 1e-30, data_model["x"])  # avoid zero
        data_model["y"] = np.where(data_model["y"] == 0, 1e-30, data_model["y"])  # avoid zero
        if data_model["area_scale"]:
            data_model["y"] = data_model["y"] / data_model["dut_area"]

        return data_model  # abort here...

        if self.sweeps and len(self.modelcards_other) == 1:
            return data_model  # abort here...
        elif self.sweeps:
            i_color = len(self.lines_other) // (len(self.modelcards_other) - 1)
        else:
            i_color = len(self.lines_other) // len(self.modelcards_other)
        color = [
            "#006400",  # darkgreen
            "#00008b",  # darkblue
            "#b03060",  # maroon3
            "#ff0000",  # red
            "#9467bd",  # yellow -> replaced by violett/brown combo
            "#deb887",  # curlywood
            "#00ff00",  # lime
            "#00ffff",  # aqua
            "#ff00ff",  # fuchsia
            "#6495ed",  # cornflower
        ][i_color % 10]
        linestyles = ["-", "--", "-.", ":"]

        sweep = data_model["sweep"]
        duts = []

        for i_mc, mc_other in enumerate(self.modelcards_other):
            if i_mc == 0 and self.sweeps:
                duts.append(None)  # index for duts same as in modelcards_other
                continue  # already used as fake reference

            # create a list of duts and simulate them with DMT
            dut_other = self.get_dut(None, mc_other)

            # scale the modelcards now
            if self.technology is not None:  # no technology -> no scaling
                dut_other.scale_modelcard()

            self.sim_con.append_simulation(dut=dut_other, sweep=sweep)
            duts.append(dut_other)

        self.sim_con.run_and_read(force=False)  # run the simulation

        for i_mc, mc_other in enumerate(self.modelcards_other):
            if i_mc == 0 and self.sweeps:
                continue  # already used as fake reference

            dut_other = duts[i_mc]

            data = dut_other.get_data(sweep=sweep, key="iv")
            t_meas = sweep.othervar[specifiers.TEMPERATURE]

            # single frequency ?
            for op_definition in self.op_definitions:
                if specifiers.FREQUENCY in op_definition.keys():
                    if isinstance(op_definition[specifiers.FREQUENCY], (float, int)):
                        data = data[
                            np.isclose(
                                data[specifiers.FREQUENCY], op_definition[specifiers.FREQUENCY]
                            )
                        ]

            data.ensure_specifier_column(self.quantity_fit, ports=self.relevant_duts[0].nodes)
            data.ensure_specifier_column(self.outer_sweep_voltage)
            data.ensure_specifier_column(self.inner_sweep_voltage)
            data.ensure_specifier_column(self.fit_along, ports=self.relevant_duts[0].nodes)

            for specifier in self.required_specifiers:
                data.ensure_specifier_column(specifier, ports=self.relevant_duts[0].nodes)

            # internal HICUM data, not always possible..
            try:
                t_dev = data["TK"].to_numpy()
            except KeyError:
                t_dev = t_meas

            if self.fit_along.specifier in ["V", "I"]:
                line_x, filter_x = np.unique(
                    np.round(data[self.fit_along].to_numpy(), decimals=10), return_index=True
                )
                line_y = np.real(data[self.quantity_fit].to_numpy())[filter_x]

                line = {
                    "x": np.where(line_x == 0, 1e-30, line_x),
                    "y": np.where(line_y == 0, 1e-30, line_y),
                    "sweep": sweep,
                    specifiers.TEMPERATURE: t_dev,
                    "linestyle": linestyles[i_mc % len(linestyles)] + color,
                    "mc": mc_other,
                }
                for specifier in self.required_specifiers:
                    line[specifier] = data[specifier].to_numpy()[filter_x]

                self.lines_other.append(line)
                if self.outer_sweep_voltage.specifier == "I":
                    self.labels_other.append(
                        f"{self.names_other[i_mc]}: ${self.outer_sweep_voltage.to_tex()}"
                        + r" = \SI{"
                        + f"{data[self.outer_sweep_voltage].to_numpy()[0]*1e3:.2f}"
                        + r"}{\milli\ampere} T=\SI{"
                        + f"{t_meas:.2f}"
                        + r"}{\kelvin}$"
                    )  # ensures nice labels in the plot
                else:
                    self.labels_other.append(
                        f"{self.names_other[i_mc]}: ${self.outer_sweep_voltage.to_tex()}"
                        + r" = \SI{"
                        + f"{data[self.outer_sweep_voltage].to_numpy()[0]:.2f}"
                        + r"}{\volt} T=\SI{"
                        + f"{t_meas:.2f}"
                        + r"}{\kelvin}$"
                    )  # ensures nice labels in the plot

            else:
                v_outer = data[self.outer_sweep_voltage].unique()
                for i_inner, v_inner, df_inner in data.iter_unique_col(
                    self.inner_sweep_voltage, decimals=3
                ):
                    # get correct line :/
                    if not np.isclose(v_inner, data_model[self.inner_sweep_voltage][0], atol=1e-3):
                        continue

                    line_x = df_inner[self.fit_along].to_numpy()
                    line_y = np.real(df_inner[self.quantity_fit].to_numpy())

                    line = {
                        "x": np.where(line_x == 0, 1e-30, line_x),
                        "y": np.where(line_y == 0, 1e-30, line_y),
                        specifiers.TEMPERATURE: t_meas,
                        "sweep": sweep,
                        "linestyle": linestyles[i_mc % len(linestyles)] + color,
                        "mc": mc_other,
                    }
                    for specifier in self.required_specifiers:
                        line[specifier] = df_inner[specifier].to_numpy()
                    self.lines_other.append(line)

                    self.labels_other.append(
                        f"{self.names_other[i_mc]}: $({self.outer_sweep_voltage.to_tex()},{+ self.inner_sweep_voltage.to_tex()} ) = ("
                        + f"{v_outer:.2f},{v_inner:.2f}"
                        + r")\si{\volt} $"
                    )  # ensures nice labels in the plot

                    break  # only done once for correct v_inner

        return data_model

    def get_tex(self):
        return r"\text{Comparing multiple modelcards}"

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
                + r"$ from measurements vs. multiple full HICUM circuit simulations."
            )
        )
        if self.additional_tex_description:
            doc.append(NoEscape(self.additional_tex_description))

        return doc

    def add_data_to_plot(self, plot_obj, x_col, y_col, area_x=False, area_y=False):
        plot_obj = super().add_data_to_plot(plot_obj, x_col, y_col, area_x=area_x, area_y=area_y)

        for line_other, label_other in zip(self.lines_other, self.labels_other):
            try:
                plot_obj.add_data_set(
                    line_other[x_col],
                    line_other[y_col],
                    label=label_other,
                    style=line_other["linestyle"],
                )

            except KeyError:
                pass

        return plot_obj

    def get_dut(self, line, paras_model, dut_size=None):
        """Overwritten from XStep. See doc in XStep."""
        if dut_size is None:
            dut_size = self.relevant_duts[0]

        dut = self.DutCircuitClass(
            database_dir=self.circuit_database_dir,
            dut_type=dut_size.dut_type,
            inp_circuit=paras_model,
            technology=self.technology,
            width=dut_size.width,
            length=dut_size.length,
            contact_config=dut_size.contact_config,
            reference_node=dut_size.reference_node,
            get_circuit_arguments=self.get_circuit_arguments,
            sim_dir=self.circuit_sim_dir,
        )
        return dut
