""" Extracts PoA parameters using bilinear scaling for a given quantity. Subclass this for easier PoA separations such as the classical one.

* quantity_a       -> area related quantitiy
* quantity_l       -> length related quantity
* quantity_b       -> width related quantity
* quantity_corner  -> corner related quantity

Author: Markus Müller       | Markus.Mueller3@tu-dresden.de
Author: Mario Krattenmacher | Mario.Krattenmacher@semimod.de
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
import warnings
from DMT.core import McParameter, Plot, specifiers
from DMT.extraction import plot, print_to_documentation, XQPoaBilinearFull
from DMT.extraction import find_nearest_index, IYNormNone

# pylint: disable=redefined-outer-name


class XQPoaBilinearFullReg(XQPoaBilinearFull):
    """XPoa is the superclass for PoA analysis of electrical quantities. It implements a linear PoA analysis of a given quantity at multiple operating points using the QStep framework.

    | XPoaBilinearFull can perform a length and/or width related PoA separation for many operating point at the same time
    |
    | (1) quantity(op) = quantity_a(op) * area + quantity_l * length + quantity_b * width + quantity_corner
    | length           = length + delta_length
    | width            = width + delta_width
    |
    | at different operating points, depending on the parameter that are passed to this object. The deltas are optimized globally.

    Parameters
    ----------
    name           : string
        name of this XStep.
    mcard          : DMT.core.McParamterCompositon
        Modelcard where the parameters dl and db are stored (they will be unique)
    lib            : DMT.core.DutLib
        Library object that stores all devices of interest for this XStep.
    op_definition  : {DMT.core.specifier:val}
        Dict whose keys and values define the operating regions for this XStep. E.g. specifiers:TEMPERATURE:300 would only allow data at temperature 300K.
    quantity       : DMT.core.specifier
        The quantity to be scaled, e.g. specifiers.CAPACITANCE + 'B' + 'E'.
    quantity_scale : float
        The scaling factor to determine the unit of the quantity, e.g. 1e3 will cause the quantity to be plotted as milli.
    sweep_voltage  : DMT.core.specifier
        The voltage that is to be used for sweeping during PoA analysis.
    dut_type       : DMT.core.DutType
        The device type, e.g. DutType.npn.
    scale_along    : string
        Either ''width', 'length' or 'both'. If 'width' or 'length', only devices with different scale_along will be used for scaling at fixed other dimension specified by scale_at .
    scale_at       : float
        Only active if scale_along is 'width' or 'length'. The other dimension is the fixed at scale_at .
    legend_off     : bool, True
        Turn the legend in the main_plot off or on.
    negative       : bool
        If negative values are to be scaled, this will invert them to generate nicer plots.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iynorm = IYNormNone  # logarithmic normalization is advantageous for currents

    @plot()
    @print_to_documentation()
    def main_plot(self):
        """Overwrite main plot."""
        y_label = (
            r"$"
            + self.quantity.to_tex()
            + r"/A_{\mathrm{E,drawn}}/"
            + self.quantity.get_tex_unit(scale=self.quantity_scale, add=r"\per\square\micro\meter")
            + r"$"
        )
        if self.negative:
            y_label = (
                r"$-"
                + self.quantity.to_tex()
                + r"/A_{\mathrm{E,drawn}}/"
                + self.quantity.get_tex_unit(
                    scale=self.quantity_scale, add=r"\per\square\micro\meter"
                )
                + r"$"
            )

        main_plot = super().main_plot(
            r"$" + self.quantity.to_tex() + r"(P/A)$",
            x_specifier=specifiers.POWER,
            x_label=r"$P_{\mathrm{E,drawn}}/A_{\mathrm{E,drawn}}/\si{ \per\micro\meter }$",
            x_scale=1e-6,
            y_label=y_label,
            y_scale=self.quantity_scale * 1e-12,  # per um^2
            legend_location="upper left",
        )
        main_plot.x_limits = (0, None)
        main_plot.y_limits = (0, None)
        return main_plot

    def set_initial_guess_line(self, composition, line):
        """For this simple linear extraction the starting guess need not be very clever. Just assume that quantity_p=0."""
        val_a = None
        val_p = None
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            try:
                [val_p, val_a] = np.polyfit(line["x"], line["quantity_per_area0"], 1)
            except np.RankWarning:
                val_p = (
                    np.max(line["quantity_per_area0"]) - np.min(line["quantity_per_area0"])
                ) / (np.max(line["x"]) - np.min(line["x"]))
                val_a = line["quantity_per_area0"][0] - val_p * line["x"][0]

        para_a = McParameter("quantity_per_area", value=np.abs(val_a))
        para_a.min = [0]
        para_a.max = [np.abs(val_a) * 2]
        composition.set(para_a)

        para_l = McParameter(
            "quantity_per_length", value=np.abs(val_p)
        )  # nice staring value i think
        para_l.min = [0]
        para_l.max = [np.abs(val_p) * 2]
        composition.set(para_l)

        para_b = McParameter(
            "quantity_per_width", value=np.abs(val_p)
        )  # nice staring value i think
        para_b.min = [0]
        para_b.max = [np.abs(val_p) * 2]
        composition.set(para_b)

        para_c = McParameter("quantity_corner", value=1e-20)
        para_c.min = [0]
        para_c.max = [np.abs(val_p)]
        composition.set(para_c)

    def fit(self, data_model, compositions):
        """Set the y-values, using one quantity_a for each line and one quantity_p for all lines."""
        if self.name_dlE in compositions[0].name:
            dlE = compositions[0][self.name_dlE].value
        else:
            dlE = self.mcard[self.name_dlE].value

        if self.name_dbE in compositions[0].name:
            dbE = compositions[0][self.name_dbE].value
        else:
            dbE = self.mcard[self.name_dbE].value

        for line, composition in zip(data_model, compositions[1:]):
            line["y"] = self.model_function(
                dlE=dlE,
                dbE=dbE,
                b_E0=line["b_E0"],
                l_E0=line["l_E0"],
                **composition.to_kwargs(),
            ) / (line["b_E0"] * line["l_E0"])
            line["y_model_real"] = line["y"]
            line["y"] = np.log10(line["y"]) - np.log10(line["quantity_per_area0"])

        # regularization finding
        # the quantities are at this point per line, but we want them along lines...so this is basically a reshape
        composition_paras = np.zeros((len(compositions[1:]), len(compositions[1])))
        voltages = np.zeros((len(compositions[1:]), len(compositions[1])))
        for i, composition in enumerate(compositions[1:]):
            composition_paras[i, 0] = composition.value
            composition_paras[i, 1] = composition.value[1]
            composition_paras[i, 2] = composition.value[2]
            composition_paras[i, 3] = composition.value[3]

        for i, line in enumerate(data_model):
            voltages[i, :] = line["voltage"]
            voltages[i, :] = voltages[i, :]

        # go through cols and apply regularization function
        for i in range(composition_paras.shape[1]):
            composition_paras[:, i] = np.gradient(np.log(composition_paras[:, i]), voltages[:, i])
            composition_paras[:, i] = np.gradient(composition_paras[:, i], voltages[:, i])

        # add a piece of the regularization to each line
        for line, row in zip(data_model, composition_paras):
            line["y"] += 5e-7 * np.sum(np.abs(row))

        return data_model

    def init_data_reference(self):
        """Go through all relevant duts and extract I_B."""
        v_in_all_df = None
        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    data = dut.data[key]
                    voltages = np.round(self.get_operating_points(data), 3)
                    if v_in_all_df is None:
                        v_in_all_df = voltages
                        continue

                    v_in_all_df = [voltage for voltage in v_in_all_df if voltage in voltages]

        for voltage in v_in_all_df:
            quantities, quantities_per_area0, l_E0, b_E0 = [], [], [], []

            for dut in self.relevant_duts:
                for key in dut.data.keys():
                    if self.validate_key(key):
                        data = dut.data[key]
                        quantity = self.get_quantity(data, voltage)
                        if quantity:
                            quantities.append(quantity)
                            quantities_per_area0.append(quantity / (dut.length * dut.width))
                            l_E0.append(dut.length)
                            b_E0.append(dut.width)

            # if not quantities or any(quantity < 0 for quantity in quantities):
            # continue

            if len(quantities) < 2:  # need at least 2 points for the polyfit...
                continue

            quantities_per_area0 = np.asarray(quantities_per_area0)
            l_E0 = np.asarray(l_E0)
            b_E0 = np.asarray(b_E0)
            quantities = np.asarray(quantities)

            # if the quantity that shall be scaled is negative, we invert the sign here
            sign = 1
            if self.negative:
                sign = -1

            line = {
                "y": np.zeros_like(quantities_per_area0),
                "x": 2 * (l_E0 + b_E0) / (l_E0 * b_E0),
                "quantity": sign * quantities,
                "quantity_per_area0": sign * quantities_per_area0,
                "l_E0": l_E0,
                "b_E0": b_E0,
                "area": l_E0 * b_E0,
                "voltage": voltage,
            }

            self.data_reference.append(line)
            self.labels.append(
                r"$" + self.voltage.to_tex() + r"=\SI{" + str(voltage) + r"}{V}$"
            )  # ensures nice labels in the plot

    def calc_all(self, xdata, paras_model, jac=True, reinit=False):
        """Much simpler than for XStep. No DutTcad support and no Jacobian support."""
        self.init()
        self.set_bounds()

        data = []
        data.append(self.fit_wrapper(self.data_model, self.para_compositions))

        # make sure that the data in data_model matches f(*arg) where the args (not the case for jacobian)
        for line, y_model in zip(self.data_model, data[0]):
            line["y"] = y_model

        return self.data_model

    # Just plotting from here on ###############

    @plot()
    @print_to_documentation()
    def plot_quantity_scaled_fit(self):
        """Plot quantity as a function of operating point meas vs fit for multiple geometries for all analyzed duts"""
        plot = Plot(
            r"Application of scaling equation.",
            style="xtraction",
            num=self.name + " Q (V) fit",
            x_label=self.voltage.to_label(),
            y_label=self.quantity.to_label(scale=self.quantity_scale, negative=self.negative),
        )
        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    label = (
                        r"$l_{\mathrm{E,drawn}}=\SI{"
                        + f"{dut.length*1e6:.2f}"
                        + r"}{\micro\meter},\, b_{\mathrm{E,drawn}}=\SI{"
                        + f"{dut.width*1e6:.2f}"
                        + r"}{\micro\meter}$"
                    )
                    data = dut.data[key]

                    voltages_ref = self.get_operating_points(data)
                    quantity_ref = [self.get_quantity(data, voltage) for voltage in voltages_ref]
                    quantity_ref = np.abs(np.asarray(quantity_ref)) * self.quantity_scale

                    plot.add_data_set(voltages_ref, quantity_ref, label=label)

                    try:  # for subclass that has xfunc...ok this is a little dirty ;)
                        x = self.xfunc(dut.length, dut.width)
                    except AttributeError:
                        x = dut.perimeter

                    indexes = [
                        find_nearest_index(x / dut.area, line["x"]) for line in self.data_model
                    ]

                    quantity_model = [
                        line["y_model_real"][index] * dut.area
                        for index, line in zip(indexes, self.data_model)
                    ]
                    quantity_model = np.asarray(quantity_model) * self.quantity_scale
                    voltages_model = [line["voltage"] for line in self.data_model]
                    voltages_model = np.asarray(voltages_model)

                    plot.add_data_set(voltages_model, quantity_model, label=None)

        plot.legend_location = "upper left"

        if self.quantity.specifier == specifiers.CURRENT:
            plot.y_axis_scale = "log"

        return plot

    @plot()
    @print_to_documentation()
    def plot_quantity_separated(self):
        """Plot quantity as a function of operating point meas vs fit for multiple geometries for all analyzed duts"""
        col_width, col_length, col_area, col_corner, col_perimeter = self.get_cols_poa_full()

        plot = Plot(
            r"$" + self.quantity.to_tex() + r"$ separated for reference device",
            style="mix",
            num=self.name + " Q (V) seperated",
            x_label=self.voltage.to_label(),
            y_label=self.quantity.to_label(scale=self.quantity_scale, negative=self.negative),
        )
        for key in self.dut_ref.data.keys():
            if self.validate_key(key):
                data = self.dut_ref.data[key]
                voltages = self.get_operating_points(data)
                quantity_meas = [self.get_quantity(data, voltage) for voltage in voltages]
                plot.add_data_set(
                    voltages,
                    np.abs(data[col_area] * self.quantity_scale),
                    label=r"$"
                    + self.quantity.to_tex(subscript="A", superscript="''")
                    + r"A_{\mathrm{E0}}$",
                )
                plot.add_data_set(
                    voltages,
                    np.abs(data[col_perimeter] * self.quantity_scale),
                    label=r"$"
                    + self.quantity.to_tex(subscript="P", superscript="'")
                    + r"P_{\mathrm{E0}}$",
                )
                plot.add_data_set(
                    voltages,
                    np.abs((data[col_perimeter] + data[col_area])) * self.quantity_scale,
                    label=r"$"
                    + self.quantity.to_tex(subscript="A", superscript="''")
                    + r"A_{\mathrm{E0}}+"
                    + self.quantity.to_tex(subscript="P", superscript="'")
                    + r"P_{\mathrm{E0}}$",
                )
                plot.add_data_set(
                    voltages,
                    np.abs(data[col_length] * self.quantity_scale),
                    label=r"$"
                    + self.quantity.to_tex(subscript="l", superscript="'")
                    + r"l_{\mathrm{E0}}$",
                )
                plot.add_data_set(
                    voltages,
                    np.abs(data[col_width] * self.quantity_scale),
                    label=r"$"
                    + self.quantity.to_tex(subscript="b", superscript="'")
                    + r"b_{\mathrm{E0}}$",
                )
                plot.add_data_set(
                    voltages,
                    np.abs(data[col_corner] * self.quantity_scale),
                    label=r"$" + self.quantity.to_tex(subscript="c", superscript="") + r"$ ",
                )
                plot.add_data_set(
                    voltages,
                    np.abs(np.asarray(quantity_meas) * self.quantity_scale),
                    label=r"$" + self.quantity.to_tex(subscript="", superscript="") + r"$ ",
                )

        plot.legend_location = "upper left"

        if self.quantity.specifier == specifiers.CURRENT:
            plot.y_axis_scale = "log"
        return plot

    @plot()
    @print_to_documentation()
    def plot_quantity_density_separated(self):
        """Plot quantity as a function of operating point meas vs fit for multiple geometries for all analyzed duts"""

        plot = Plot(
            r"$"
            + self.quantity.to_tex()
            + r"$ density along width/length separated for reference device.",
            style="mix",
            num=self.name + " Q (V) density seperated",
            x_label=self.voltage.to_label(),
            y_label=r"$"
            + self.quantity.to_tex(subscript=r"l(b)", superscript="'")
            + r"/"
            + self.quantity.get_tex_unit(scale=self.quantity_scale, add=r"\per\micro\meter")
            + r"$",
        )
        for key in self.dut_ref.data.keys():
            if self.validate_key(key):
                data = self.dut_ref.data[key]
                voltages = self.get_operating_points(data)
                quantitiy_per_length = data["q_per_length"] * self.quantity_scale / 1e6  # per um
                quantitiy_per_width = data["q_per_width"] * self.quantity_scale / 1e6  # per um
                plot.add_data_set(
                    voltages,
                    quantitiy_per_length,
                    label=r"$" + self.quantity.to_tex(subscript="l", superscript="'") + r"$",
                )
                plot.add_data_set(
                    voltages,
                    quantitiy_per_width,
                    label=r"$" + self.quantity.to_tex(subscript="b", superscript="'") + r"$",
                )

        plot.legend_location = "upper left"
        return plot
