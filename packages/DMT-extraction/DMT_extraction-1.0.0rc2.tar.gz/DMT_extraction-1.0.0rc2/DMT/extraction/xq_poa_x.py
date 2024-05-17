""" Extracts PoA parameters for a given quantity.

* quantity_a  -> area related quantitiy
* quantity_x  -> x related quantity (see docstring below)
* quantity_corner  -> corner related quantity

Author: Markus Müller | Markus.Mueller3@tu-dresden.de
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
from scipy import interpolate
import numpy as np
import warnings
import copy
from DMT.core import McParameter, McParameterCollection, Plot, specifiers, sub_specifiers
from DMT.extraction import plot, print_to_documentation, find_nearest_index
from DMT.extraction import XQPoaBilinearFull

# pylint: disable=redefined-outer-name


class XQPoX(XQPoaBilinearFull):
    """XQPoX is a subclass of XQPoaBilinearFull and implements the separation of any quantity vs. an area and another area/peri quantity X, e.g. A_BCx.

    | XPoa can perform a separation of the emitter window area vs. any quantity X that can be written as a function of (dut.length, dut.width).
    | (1) quantity(op) = quantity_a(op) * area + quantity_x * X + quantity_corner
    | at different operating points, depending on the parameter that are passed to this object.

    Parameters
    ----------
    same as XQPoaBilinearFull, but:
    pfunc : callable(dut.length, dut.width, mcard)
        A callable function that returns some quantity P as a function of (dut.length, dut.width).
    ptex  : string
        String that will be used for plotting the quantity P returned by pfunc.
    afunc : callable(dut.length, dut.width, mcard)
        A callable function that returns some quantity A as a function of (dut.length, dut.width).
    atex  : string
        String that will be used for plotting the quantity A returned by pfunc.
    """

    def __init__(self, pfunc, ptex, *args, afunc=None, atex=None, **kwargs):
        # init the super class...to_optimize will deactivate dl and db
        self.pfunc = pfunc
        self.ptex = ptex
        self.afunc = afunc
        self.atex = atex
        if self.atex is None:
            self.atex = r"A_{\mathrm{E0}}"

        super().__init__(*args, scale_along="both", **kwargs)  # no dl and dE
        self.negative = False

        self.model_function_info = {"independent_vars": ("l_E0", "b_E0", "x", "area")}

    def set_initial_guess_line(self, composition, line):
        """For this simple linear extraction the starting guess need not be very clever. Just assume that quantity_p=0."""
        val_a1 = None
        val_a2 = None
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            try:
                [val_a2, val_a1] = np.polyfit(
                    line["x"], line["y"], 1
                )  # a1 y abschnitt => area , a2 steigung => x
            except np.RankWarning:
                try:
                    val_a1 = (np.max(line["y"]) - np.min(line["y"])) / (
                        np.max(line["x"]) - np.min(line["x"])
                    )  # steigung
                    val_a2 = line["y"][0] - val_a2 * line["x"][0]  # yabschnitt
                except RuntimeWarning:
                    val_a1 = 0
                    val_a2 = line["y"][0]

        para_a1 = McParameter("quantity_per_area", value=np.abs(val_a1))
        para_a1.min = 0
        para_a1.max = np.abs(val_a1) * 2
        composition.set(para_a1)

        para_a2 = McParameter("quantity_per_x", value=np.abs(val_a2))
        para_a2.min = 0
        para_a2.max = np.abs(val_a2) * 2
        composition.set(para_a2)
        # para_a2 = McParameter("quantity_per_x", value=np.abs(0))
        # para_a2.min = 0
        # para_a2.max = np.abs(val_a1) * 2
        # composition.set(para_a2)

        try:
            para_c = McParameter("quantity_corner", value=np.abs(val_a1) * line["area"][0] * 0.5)
            para_c.min = 0
            para_c.max = np.abs(val_a1) * line["area"][0]
            composition.set(para_c)
        except KeyError:
            pass

    def fit(self, line, paras_model):
        """Set the y-values, using one quantity_a for each line and one quantity_p for all lines."""
        line["y"] = self.model_function(
            b_E0=line["b_E0"],
            l_E0=line["l_E0"],
            x=line["x_"],
            area=line["area"],
            quantity_per_area=paras_model["quantity_per_area"].value,
            quantity_per_x=paras_model["quantity_per_x"].value,
        ) / (line["area"])
        return line

    def init_data_reference(self):
        """Same as XQPoaBilinearFull, but we add the XFuncs value, too."""
        super().init_data_reference()
        for line in self.data_reference:
            line["x_"] = self.pfunc(
                line["l_E0"],
                line["b_E0"],
                dlE=self.mcard["dlE"].value,
                dbE=self.mcard["dbE"].value,
                gamma_l=self.mcard["gamma_l"].value,
                gamma_b=self.mcard["gamma_b"].value,
                recr=self.mcard["recr"].value,
            )
            if self.afunc is None:
                length = line["l_E0"]
                width = line["b_E0"]
                area = length * width
                line["area"] = area
            else:
                line["area"] = self.afunc(
                    line["l_E0"],
                    line["b_E0"],
                    dlE=self.mcard["dlE"].value,
                    dbE=self.mcard["dbE"].value,
                    gamma_l=self.mcard["gamma_l"].value,
                    gamma_b=self.mcard["gamma_b"].value,
                    recr=self.mcard["recr"].value,
                )
            line["x"] = line["x_"] / (line["area"])
            area0 = line["l_E0"] * line["b_E0"]
            line["y"] = line["y"] * area0 / line["area"]
            line["y_ref"] = line["y_ref"] * area0 / line["area"]

    def write_back_results(self):
        """Write back the results obtained by this QStep into dut_ref."""
        for dut in self.relevant_duts:
            # identify dataframe to write the results
            key_dut = None
            for key in dut.data.keys():
                if self.validate_key(key) and self.key == dut.split_key(key)[-1]:
                    if key_dut is None:
                        key_dut = key
                        break
                    else:
                        raise IOError(
                            "DMT -> XPoa: Found a second dataframe to write back results. Found were: "
                            + key_dut
                            + " and "
                            + key
                        )

            # if key_dut is None:
            #     raise IOError('DMT -> XPoa: Did not find dataframe to write back results. I was looking for ' + self.key)
            else:
                continue  # no key for this DUT

            # gather the results
            voltages_data = [line["voltage"] for line in self.data_model]
            quantity_area, quantity_x = (
                np.zeros(np.size(self.data_model)),
                np.zeros(np.size(self.data_model)),
            )

            # get dl0 and db0
            dlE = self.mcard["dlE"].value
            dbE = self.mcard["dbE"].value
            params = self.mcard.to_kwargs()
            recr = self.mcard["recr"].value

            for i, composition in enumerate(self.paras_to_optimize_per_line):
                # true also with corner rounding:
                if self.afunc is None:
                    area = dut.length * dut.width
                else:
                    area = self.afunc(
                        dut.length,
                        dut.width,
                        dlE=self.mcard["dlE"].value,
                        dbE=self.mcard["dbE"].value,
                        gamma_l=self.mcard["gamma_l"].value,
                        gamma_b=self.mcard["gamma_b"].value,
                        recr=self.mcard["recr"].value,
                    )
                x = self.pfunc(
                    dut.length,
                    dut.width,
                    dlE=self.mcard["dlE"].value,
                    dbE=self.mcard["dbE"].value,
                    gamma_l=self.mcard["gamma_l"].value,
                    gamma_b=self.mcard["gamma_b"].value,
                    recr=self.mcard["recr"].value,
                )

                composition_kwargs = composition.to_kwargs()
                if self.corner_rounding:
                    composition_kwargs["recr"] = recr

                try:
                    quantity_area[i] = area * composition["quantity_per_area"].value
                except KeyError:
                    quantity_area[i] = 0

                try:
                    quantity_x[i] = x * composition["quantity_per_x"].value
                except KeyError:
                    quantity_x[i] = 0

            indexes = [find_nearest_index(area, line["area"]) for line in self.data_model]
            quantity_model = [
                line["y"][index] * area for index, line in zip(indexes, self.data_model)
            ]
            quantity_model = np.asarray(quantity_model)

            # interpolate
            voltages_df = self.get_operating_points(dut.data[key_dut])
            try:
                f_quantity_area = interpolate.interp1d(
                    voltages_data, quantity_area, kind=3, fill_value="extrapolate"
                )
                f_quantity_x = interpolate.interp1d(
                    voltages_data, quantity_x, kind=3, fill_value="extrapolate"
                )
            except ValueError:  # voltages needs to be monotonically increasing.
                voltages = np.asarray(voltages_data)
                i_sort = np.argsort(voltages)
                f_quantity_area = interpolate.interp1d(
                    voltages[i_sort],
                    np.asarray(quantity_area)[i_sort],
                    kind=3,
                    fill_value="extrapolate",
                )
                f_quantity_x = interpolate.interp1d(
                    voltages[i_sort],
                    np.asarray(quantity_x)[i_sort],
                    kind=3,
                    fill_value="extrapolate",
                )

            sign = 1
            if self.negative:
                sign = -1

            quantity_area = sign * f_quantity_area(voltages_df)
            quantity_x = sign * f_quantity_x(voltages_df)

            # copy to local dataframe
            col_width, col_length, col_area, col_corner, col_perimeter = self.get_cols_poa_full()
            df = copy.deepcopy(dut.data[key_dut])
            df[col_area] = quantity_area
            df[col_corner] = 0
            df[col_perimeter] = quantity_x
            dut.add_data(df, key=key_dut, force=True)
            if dut == self.lib.dut_ref:
                self.df_separated = df

    # Just plotting from here on ###############
    @plot()
    @print_to_documentation()
    def plot_quantity_separated(self):
        """Plot quantity as a function of operating point meas vs fit for multiple geometries for all analyzed duts"""
        # pylint: disable=unused-variable
        col_width, col_length, col_area, col_corner, col_perimeter = self.get_cols_poa_full()

        plot = Plot(
            r"$" + self.quantity.to_tex() + r"$ separated for reference device",
            style="mix",
            num=self.name + " Q (V) seperated",
            x_label=self.voltage.to_label(),
            y_label=self.quantity.to_label(scale=self.quantity_scale, negative=self.negative),
        )
        try:
            data = self.df_separated
        except AttributeError:
            return None
        voltages = self.get_operating_points(data)
        quantity_meas = [self.get_quantity(data, voltage) for voltage in voltages]

        plot.add_data_set(
            voltages,
            np.abs(data[col_area] * self.quantity_scale),
            label=r"$" + self.quantity.to_tex(subscript="A", superscript="''") + self.atex + r"$",
        )
        plot.add_data_set(
            voltages,
            np.abs(data[col_perimeter] * self.quantity_scale),
            label=r"$" + self.quantity.to_tex(subscript="P", superscript="''") + self.ptex + r"$",
        )
        plot.add_data_set(
            voltages,
            np.abs((data[col_perimeter] + data[col_area])) * self.quantity_scale,
            label=r"$" + self.quantity.to_tex(subscript="", superscript="") + r"$ model",
        )
        plot.add_data_set(
            voltages,
            np.abs(np.asarray(quantity_meas) * self.quantity_scale),
            label=r"$" + self.quantity.to_tex(subscript="", superscript="") + r"$ meas.",
        )

        plot.legend_location = "upper left"

        if self.quantity.specifier == specifiers.CURRENT:
            plot.y_axis_scale = "log"
        return plot

    def plot_quantity_density_separated(self):
        return None

    def plot_quantity_bE_c_high(self):
        return None

    def plot_quantity_bE_b_mid(self):
        return None

    def plot_quantity_bE_a_low(self):
        return None

    def plot_quantity_lE_c_high(self):
        return None

    def plot_quantity_lE_b_mid(self):
        return None

    def plot_quantity_lE_a_low(self):
        return None

    @plot()
    @print_to_documentation()
    def plot_quantity_AEdrawn_a_low(self):
        return self.get_plot_along_area(op=0.2, num=self.name + " Q (A_E,drawn) 0.2V")

    @plot()
    @print_to_documentation()
    def plot_quantity_AEdrawn_b_mid(self):
        return self.get_plot_along_area(op=0.3, num=self.name + " Q (A_E,drawn) 0.3V")

    @plot()
    @print_to_documentation()
    def plot_quantity_AEdrawn_c_high(self):
        return self.get_plot_along_area(op=0.5, num=self.name + " Q (A_E,drawn) 0.5V")

    def get_plot_along_area(self, op=None, num=None):
        """Return an array of the quantity along length or width, at width or length with an delta at an operating point and a fit line"""
        # init the plot
        plot = Plot(
            "$"
            + self.quantity.to_tex()
            + r"\left("
            + self.atex
            + r"@"
            + self.voltage.to_tex()
            + r"=\SI{"
            + str(op)
            + r"}{\volt}\right)$",
            x_label=r"$" + self.atex + r"$",
            y_label=self.quantity.to_label(scale=self.quantity_scale, negative=self.negative),
            style="xtraction",
            num=num,
        )

        # loop over all dimensions, in the end we can sort...
        quantity = []
        area = []
        x = []
        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    data = dut.data[key]
                    # this way the order makes sense
                    quantity.append(self.get_quantity(data, op))
                    if self.afunc is None:
                        area.append(dut.area)
                    else:
                        area.append(
                            self.afunc(
                                dut.length,
                                dut.width,
                                dlE=self.mcard["dlE"].value,
                                dbE=self.mcard["dbE"].value,
                                gamma_l=self.mcard["gamma_l"].value,
                                gamma_b=self.mcard["gamma_b"].value,
                            )
                        )
                    x.append(
                        self.pfunc(
                            dut.length,
                            dut.width,
                            dlE=self.mcard["dlE"].value,
                            dbE=self.mcard["dbE"].value,
                            gamma_l=self.mcard["gamma_l"].value,
                            gamma_b=self.mcard["gamma_b"].value,
                        )
                    )

        quantity = np.abs(quantity)

        # now see what we want to scale along
        quantities_at = []
        x_axes = []
        at = np.unique(x)

        for at_ in at:
            indices = [
                i for i in range(len(x)) if x[i] == at_
            ]  # indices where we want to take the quantity
            quantities_at.append(np.asarray([quantity[i] for i in indices]))
            x_axes.append(np.asarray([area[i] for i in indices]))

        # sort and find fit line
        fit_lines = []
        for i, (x_axis, quantity_at) in enumerate(zip(x_axes, quantities_at)):
            i_sort = np.argsort(x_axis)
            x_axis = x_axis[i_sort]
            quantity_at = quantity_at[i_sort]
            x_axes[i] = x_axis
            quantities_at[i] = quantity_at
            if len(x_axis) > 2:  # also find a fitline
                fit_line = np.poly1d(np.polyfit(x_axis, quantity_at, 1))
                fit_lines.append(fit_line([0] + x_axis.tolist()))
            else:
                fit_lines.append(None)

        for x_axis, quantity_at, fit_line, at_ in zip(x_axes, quantities_at, fit_lines, at):
            # prepare labels (dirty: if "P" in ptex, assume length, else area)
            if "P" in self.ptex:
                label = r"={0:1.2f}\si{{\micro\meter}}$"
                label = label.format(at_ * 1e6)
            else:
                label = r"={0:1.2f}\si{{\square\micro\meter}}$"
                label = label.format(at_ * 1e12)
            # add the measured data
            plot.add_data_set(
                x_axis * 1e12,
                quantity_at * self.quantity_scale,
                label=r"$" + self.ptex + label,
            )
            # only need fit line if more than one data point...
            if fit_line is not None:
                plot.add_data_set(
                    [0] + (x_axis * 1e12).tolist(), fit_line * self.quantity_scale, label=None
                )
            else:
                # add dummy so that labels are nice
                plot.add_data_set(
                    [-1] * len(quantity_at), quantity_at * self.quantity_scale, label=None
                )

        plot.legend_location = "upper left"
        plot.x_limits = (0, None)
        plot.y_limits = (0, None)
        return plot

    def scaling_plot(self, mcard=None):
        return None

    @plot()
    @print_to_documentation()
    def main_plot(self, mcard=None):
        """Overwrite main plot."""
        main_plot = super().main_plot(mcard=mcard, calc_all=False)
        main_plot.x_limits = (0, None)
        main_plot.y_limits = (0, None)
        atex = self.atex
        if not "P" in self.ptex:  # P is a perimeter
            main_plot.x_label = r"$" + self.ptex + r"/" + atex + r"$"
            main_plot.x_scale = 1
        else:
            main_plot.x_label = (
                r"$" + self.ptex + r"/" + atex + r"\left(\si{\per\micro\meter}\right)$"
            )
            main_plot.x_scale = 1e-6
        main_plot.y_label = (
            r"$"
            + self.quantity.to_tex()
            + r"/"
            + atex
            + r"\left("
            + self.quantity.get_tex_unit(scale=self.quantity_scale, add=r"\per\square\micro\meter")
            + r"\right)$"
        )
        if self.negative:
            main_plot.y_label = (
                r"$-"
                + self.quantity.to_tex()
                + r"/"
                + atex
                + r"\left("
                + self.quantity.get_tex_unit(
                    scale=self.quantity_scale, add=r"\per\square\micro\meter"
                )
                + r"\right)$"
            )

        main_plot.legend_location = "upper left"
        return main_plot

    def get_tex(self):
        atex = self.atex
        subs = "''"
        if "P" in self.ptex:
            subs = "'"
        return (
            r"\frac{ "
            + self.quantity.to_tex()
            + r" }{ "
            + atex
            + r" } "
            + r"= "
            + self.quantity.to_tex(subscript="A", superscript="''")
            + r" "
            + r"+ \frac{ "
            + self.ptex
            + r" }{ "
            + atex
            + r" } "
            + self.quantity.to_tex(subscript="P", superscript=subs)
        )

    def get_description(self):
        from pylatex import Alignat, NoEscape
        from DMT.external.pylatex import Tex

        subs = "''"
        if "P" in self.ptex:
            subs = "'"
        doc = Tex()
        doc.append(
            NoEscape(
                r"This extraction step performs the geometry separation of $"
                + self.quantity.to_tex()
                + r"$."
            )
        )
        doc.append(NoEscape(r"\enspace In the following P refers to $" + self.ptex + r"$."))
        doc.append(NoEscape(r"and A refers to $" + self.atex + r"$."))
        doc.append(
            NoEscape(r"\enspace This extraction step performs a PoA separation according to")
        )
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            agn.append(self.get_tex())
        doc.append(
            NoEscape(
                r"where $"
                + self.quantity.to_tex(subscript="A", superscript="''")
                + r"$ is the "
                + self.quantity.get_descriptor()
                + r" per A, "
            )
        )
        doc.append(
            NoEscape(
                r"$"
                + self.quantity.to_tex(subscript="P", superscript=subs)
                + r"$ is the "
                + self.quantity.get_descriptor()
                + r" per P, "
            )
        )
        doc.append(
            NoEscape(
                r"The scaling equation is fitted globally (2D fit) for all measured device geometries in this extraction step."
            )
        )
        doc.append("\r")
        return doc

    def get_cols_poa_full(self):
        col_width = self.quantity + sub_specifiers.WIDTH
        col_length = self.quantity + sub_specifiers.LENGTH
        col_area = self.quantity + sub_specifiers.AREA
        col_corner = self.quantity + sub_specifiers.CORNER
        col_perimeter = self.quantity + sub_specifiers.PERIMETER
        return (col_width, col_length, col_area, col_corner, col_perimeter)

    def quantity_poa(
        self,
        l_E0,
        b_E0,
        x,
        area,
        *,
        quantity_per_area=None,
        quantity_per_x=None,
        **_kwargs,
    ):
        return area * quantity_per_area + x * quantity_per_x  # + quantity_corner

    # EQUIVALENT CIRCUIT ELEMENTS THAT SPLIT INTO AREA AND PERIMETER COMPONENT -> area componenent scales with area, perimeter with effective perimeter
    # EQUIVALENT CIRCUIT ELEMENTS THAT SPLIT INTO ONE COMPONENT                 -> area componenent scales with effective area
    @classmethod
    def get_perimeter(cls, length=None, width=None, **kwargs):
        return 2 * length + 2 * width

    @classmethod
    def get_area(cls, length=None, width=None, **kwargs):
        return length * width

    @classmethod
    def get_effective_perimeter(
        cls,
        length=None,
        width=None,
        dlE=None,
        dbE=None,
        gamma_l=None,
        gamma_b=None,
        xfunc=None,
        **kwargs,
    ):
        x = xfunc(length, width, dbE, dlE, gamma_l, gamma_b)
        return x

    @classmethod
    def get_effective_area(
        cls, length, width, dlE, dbE, gamma_l=None, gamma_b=None, gamma_c=None, **kwargs
    ):
        return 0  # not implemented, but need to return something....wont matter since no para that scales with effective area is there for this XQPoaStep class
