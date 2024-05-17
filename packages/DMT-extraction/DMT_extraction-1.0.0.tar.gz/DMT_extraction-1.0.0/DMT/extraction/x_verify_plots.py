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
from DMT.core import Plot, specifiers, sub_specifiers, natural_scales, DutTcad
from DMT.extraction import plot, print_to_documentation

# This file defines several standard plots that can be used by the XVerify class


@plot()
@print_to_documentation()
def plot_ib(self):
    y_col = specifiers.CURRENT + "B"
    x_col = self.inner_sweep_voltage
    if self.verify_area_densities:
        y_label = r"$J_{\mathrm{B}}\left(\si{\milli\ampere\per\square\micro\meter}\right)$"
        y_scale = 1e3 / (1e6 * 1e6)
    else:
        y_label = r"$I_{\mathrm{B}}\left(\si{\milli\ampere}\right)$"
        y_scale = 1e3
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify ib",
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
@print_to_documentation()
def plot_beta(self):
    y_col = specifiers.CURRENT + "C"
    y_col2 = specifiers.CURRENT + "B"
    x_col = self.inner_sweep_voltage
    sub_plot = Plot(
        r"$ \beta \left( " + x_col.to_tex() + r" \right) $",
        style="xtraction",
        num=self.name + " verify ib",
        x_specifier=x_col,
        y_label=r"$\beta$",
        x_scale=1,
        y_scale=1,  # ma/um^2
        y_log=True,
    )
    try:
        for line_reference, line_model, label in zip(
            self.data_reference, self.data_model, self.labels
        ):  # add the reference and model data in an alternating way
            if self.legend_off:
                sub_plot.add_data_set(
                    line_reference[x_col],
                    line_reference[y_col] / line_reference[y_col2],
                )
                sub_plot.add_data_set(line_model[x_col], line_model[y_col] / line_model[y_col2])
            else:
                sub_plot.add_data_set(
                    line_reference[x_col],
                    line_reference[y_col] / line_reference[y_col2],
                    label=label,
                )
                sub_plot.add_data_set(
                    line_model[x_col],
                    line_model[y_col] / line_model[y_col2],
                )

        return sub_plot

    except KeyError:
        return None


@plot()
@print_to_documentation()
def plot_T(self):
    # plot of self heating from circuit simulator
    style = "color" if self.model is None else "xtraction_color"
    style = "mix"
    x_col = specifiers.CURRENT + "C"
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


@plot()
@print_to_documentation()
def plot_ic(self):
    y_col = specifiers.CURRENT + "C"
    x_col = self.inner_sweep_voltage
    if self.verify_area_densities:
        y_label = r"$J_{\mathrm{C}}\left(\si{\milli\ampere\per\square\micro\meter}\right)$"
        y_scale = 1e3 / (1e6 * 1e6)
    else:
        y_label = r"$I_{\mathrm{C}}\left(\si{\milli\ampere}\right)$"
        y_scale = 1e3
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
@print_to_documentation()
def plot_ft(self):
    x_col = specifiers.CURRENT + "C"
    y_col = specifiers.TRANSIT_FREQUENCY
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left(\si{\milli\ampere\per\square\micro\meter}\right)$"
        x_scale = 1e3 / (1e6 * 1e6)
    else:
        x_label = r"$I_{\mathrm{C}}\left(\si{\milli\ampere}\right)$"
        x_scale = 1e3
    sub_plot = Plot(
        r"$ " + y_col.to_tex() + r" \left( J_{\mathrm{C}} \right) $",
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


@plot()
@print_to_documentation()
def plot_rey12(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        x_log = True
    y_col = specifiers.SS_PARA_Y + "B" + "C" + sub_specifiers.REAL
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Re\left\{ Y_{12} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Re\left\{ Y_{12} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y12",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_rey21(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        x_log = True
    y_col = specifiers.SS_PARA_Y + "C" + "B" + sub_specifiers.REAL
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Re\left\{ Y_{21} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Re\left\{ Y_{21} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y21",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_rey22(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        x_log = True
    y_col = specifiers.SS_PARA_Y + "C" + "C" + sub_specifiers.REAL
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Re\left\{ Y_{22} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Re\left\{ Y_{22} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y22",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_rey11(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        x_log = True
    y_col = specifiers.SS_PARA_Y + "B" + "B" + sub_specifiers.REAL
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Re\left\{ Y_{11} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Re\left\{ Y_{11} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y11",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_imy12(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        # x_log = True
    y_col = specifiers.SS_PARA_Y + "B" + "C" + sub_specifiers.IMAG
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Im\left\{ Y_{12} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Im\left\{ Y_{12} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y12 im",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        # x_log=True,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_imy21(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        # x_log = True
    y_col = specifiers.SS_PARA_Y + "C" + "B" + sub_specifiers.IMAG
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Im\left\{ Y_{21} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Im\left\{ Y_{21} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y21 im",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_imy22(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        # x_log = True
    y_col = specifiers.SS_PARA_Y + "C" + "C" + sub_specifiers.IMAG
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Im\left\{ Y_{22} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Im\left\{ Y_{22} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y22 im",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_imy11(self):
    x_col = self.fit_along
    x_log = False
    if (
        x_col == specifiers.VOLTAGE + ["B", "E"]
        or x_col == specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
    ):
        x_col = specifiers.CURRENT + "C"
        # x_log = True
    y_col = specifiers.SS_PARA_Y + "B" + "B" + sub_specifiers.IMAG
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left( \si{\milli\ampere\per\square\micro\meter} \right)$"
        x_scale = 1e3 / (1e6 * 1e6)
        y_label = (
            r"$\Im\left\{ Y_{11} \right\} \left( \si{\milli\siemens\per\square\micro\meter}\right)$"
        )
        y_scale = 1e3 / (1e6 * 1e6)  # mS/um^2
    else:
        x_scale = natural_scales[x_col.specifier]
        x_label = x_col.to_label(scale=x_scale, divide_by_unit=False)
        y_label = r"$\Im\left\{ Y_{11} \right\} \left( \si{\milli\siemens} \right)$"
        y_scale = 1e3  # mS
    sub_plot = Plot(
        f"$ {y_col.to_tex()} \\left( {x_col.to_tex()} \\right) $",
        style="xtraction_color",
        num=self.name + " verify y11 im",
        x_label=x_label,
        y_label=y_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=y_scale,
        x_log=x_log,
        legend_location="upper left",
    )
    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True, area_y=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_fmax(self):
    x_col = specifiers.CURRENT + "C"
    y_col = specifiers.MAXIMUM_OSCILLATION_FREQUENCY
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}\left(\si{\milli\ampere\per\square\micro\meter}\right)$"
        x_scale = 1e3 / (1e6 * 1e6)
    else:
        x_label = r"$I_{\mathrm{C}}\left(\si{\milli\ampere}\right)$"
        x_scale = 1e3
    sub_plot = Plot(
        r"$ " + y_col.to_tex() + r" \left( J_{\mathrm{C}} \right) $",
        style="xtraction_color",
        num=self.name + " verify fmax",
        x_label=x_label,
        y_specifier=y_col,
        x_scale=x_scale,  # 1e3,
        y_scale=1e-9,
        x_log=True,
        legend_location="upper left",
    )
    if issubclass(type(self.lib.dut_ref), DutTcad):
        return sub_plot

    sub_plot = self.add_data_to_plot(sub_plot, x_col, y_col, area_x=True)

    return sub_plot


@plot()
@print_to_documentation()
def plot_tf(self):
    x_col = specifiers.CURRENT + "C"
    y_col = specifiers.TRANSIT_TIME
    if self.verify_area_densities:
        x_label = r"$J_{\mathrm{C}}/\si{\milli\ampere\per\square\micro\meter}$"
        x_scale = 1e3 / (1e6 * 1e6)
    else:
        x_label = r"$I_{\mathrm{C}}/\si{\milli\ampere}$"
        x_scale = 1e3
    sub_plot = Plot(
        r"$ \tau_{\mathrm{f}} \left( J_{\mathrm{C}} \right) $",
        style="color",
        num=self.name + " verify tf",
        x_label=x_label,
        y_label=r"$\tau_{\mathrm{f}}\left( \si{\pico\second} \right)$",
        y_scale=1e12,
        x_scale=x_scale,
        x_log=False,
        legend_location="upper left",
    )
    if x_col not in self.data_model[0] or y_col not in self.data_model[0]:
        return sub_plot

    for line_model, label in zip(
        self.data_model, self.labels
    ):  # add the reference and model data in an alternating way
        sub_plot.add_data_set(line_model[x_col], line_model[y_col], label)

    return sub_plot
