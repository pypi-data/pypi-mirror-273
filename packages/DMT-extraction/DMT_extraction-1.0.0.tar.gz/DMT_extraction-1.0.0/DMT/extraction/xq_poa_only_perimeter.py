""" Extracts PoA parameters for a given quantity. Subclass this for a quick and easy PoA separation XStep.

Examples can be found in x_ic_geo.py and other hl2 XSteps that inerhits from this class.

* quantity_a  -> area related quantitiy
* quantity_l  -> length related quantity
* quantity_b  -> width related quantity
* quantity_corner  -> corner related quantity

Author: Markus Müller | Markus.Mueller3@tu-dresden.de
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
from DMT.core import McParameter, McParameterCollection, Plot, specifiers
from DMT.extraction import XQPoaBilinearFull, plot, print_to_documentation


# pylint: disable=redefined-outer-name
class XQPoaOnlyPerimeter(XQPoaBilinearFull):
    """XQPoaOnlyPerimeter is a subclass of XQPoaBilinearFull that applies a simplified scaling equation compared to full bilinear scaling, as described in the docstring of thic class.

    | XQPoaOnlyPerimeter can perform a perimeter vs. area vs. corner separation according to
    | (1) quantity(op) = quantity_a(op) * area + quantity_p * perimeter + quantity_corner
    | at different operating points, depending on the parameter that are passed to this object.
    | With respect to the full bilinear equation system, this assumes that quantity_b == quantity_l.

    Parameters
    ----------
    Same as XQPoaBilinearFull.
    """

    def __init__(self, *args, **kwargs):
        # init the super class...to_optimize will deactivate dl and db
        super().__init__(*args, **kwargs)
        self.paras_quantity = McParameterCollection()
        for para in ["quantity_per_area", "quantity_per_perimeter", "quantity_corner"]:
            self.paras_quantity.add(
                McParameter(para, value=0)
            )  # the value is set to a better value in self.set_initial_guess(), later.

    def set_initial_guess_line(self, composition, line):
        """For this simple linear extraction the starting guess need not be very clever. Just assume that quantity_p=0."""
        val_a = None
        val_p = None
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            try:
                [val_p, val_a] = np.polyfit(line["x"], line["y"], 1)
            except np.RankWarning:
                val_p = (np.max(line["y"]) - np.min(line["y"])) / (
                    np.max(line["x"]) - np.min(line["x"])
                )
                val_a = line["y"][0] - val_p * line["x"][0]

        para_a = McParameter("quantity_per_area", value=np.abs(val_a))
        para_a.min = [0]
        para_a.max = [np.abs(val_a) * 2]
        composition.set(para_a)

        para_p = McParameter(
            "quantity_per_perimeter", value=np.abs(val_p)
        )  # nice staring value i think
        para_p.min = [0]
        para_p.max = [np.abs(val_p) * 2]
        composition.set(para_p)

        para_c = McParameter("quantity_corner", value=1e-20)
        para_c.min = [0]
        para_c.max = [np.abs(val_p)]
        composition.set(para_c)

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

    def plot_quantity_density_separated(self):
        """Plot quantity as a function of operating point meas vs fit for multiple geometries for all analyzed duts"""
        return None

    def get_tex(self):
        return (
            r"\frac{ "
            + self.quantity.to_tex()
            + r" }{ A_{\mathrm{E0}} } "
            + r"= "
            + self.quantity.to_tex(subscript="A", superscript="''")
            + r" "
            + r"+ \frac{ P_{\mathrm{E0}} }{ A_{\mathrm{E0}} } "
            + self.quantity.to_tex(subscript="l", superscript="'")
            + r"+ \frac{ 1 }{ A_{\mathrm{E0}}} "
            + self.quantity.to_tex(subscript="c")
            + r" \\ A_{\mathrm{E0}} = l_{\mathrm{E0}} b_{\mathrm{E0}} \\"
            + r" \\ P_{\mathrm{E0}} = 2 \left( l_{\mathrm{E0}} + b_{\mathrm{E0}} \right) \\"
            + r" \\ l_{\mathrm{E0}} = l_{\mathrm{E,drawn}} + \Delta l_{\mathrm{E}} \\"
            + r" \\ b_{\mathrm{E0}} = b_{\mathrm{E,drawn}} + \Delta b_{\mathrm{E}}"
        )

    def get_description(self):
        from pylatex import Math, Alignat, NoEscape
        from DMT.external.pylatex import Tex

        doc = Tex()
        doc.append(
            NoEscape(
                r"This extraction step performs the PoA separation of $"
                + self.quantity.to_tex()
                + r"$. "
            )
        )
        doc.append(NoEscape(r"For advanced HBT technolgies the classical PoA separation"))
        doc.append(
            Math(
                data=self.quantity.to_tex()
                + r" = "
                + self.quantity.to_tex(subscript="A", superscript="''")
                + r"A_{\mathrm{E0}} + "
                + self.quantity.to_tex(subscript="P", superscript="'")
                + r"P_{\mathrm{E0}}\, ,",
                inline=False,
                escape=False,
            )
        )
        doc.append(
            NoEscape(
                r"where $"
                + self.quantity.to_tex(subscript="A", superscript="''")
                + r"$ is the "
                + self.quantity.get_descriptor()
                + r" per emitter area, "
            )
        )
        doc.append(
            NoEscape(
                r"$"
                + self.quantity.to_tex(subscript="P", superscript="'")
                + r"$ is the "
                + self.quantity.get_descriptor()
                + r" per emitter perimeter, "
            )
        )
        doc.append(NoEscape(r"$A_{\mathrm{E0}}$ is the emitter area and "))
        doc.append(NoEscape(r"$P_{\mathrm{E0}}$ is the emitter perimeter, "))
        doc.append(NoEscape(r"does not generally yield satisfactory results.\\"))
        doc.append(
            NoEscape(
                r"Instead, this extraction step performs a bilinear PoA separation according to"
            )
        )
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            agn.append(self.get_tex())
        doc.append(
            NoEscape(
                r"where $"
                + self.quantity.to_tex(subscript="c", superscript="")
                + r"$ is the "
                + self.quantity.get_descriptor()
                + r"'s corner component, "
            )
        )
        doc.append(NoEscape(r"$l_{\mathrm{E0}}^{}$ is the emitter length, "))
        doc.append(NoEscape(r"$b_{\mathrm{E0}}^{}$ is the emitter width, "))
        doc.append(NoEscape(r"$P_{\mathrm{E0}}$ is the emitter perimeter and "))
        doc.append(NoEscape(r"$A_{\mathrm{E0}}$ is the emitter area. "))
        doc.append(
            NoEscape(
                r"The equation system is fitted globally for all measured device geometries in this extraction step."
            )
        )
        doc.append("\r")
        return doc

    def quantity_poa(
        self, dlE, dbE, l_E0, b_E0, quantity_per_area, quantity_per_perimeter, quantity_corner=0
    ):
        """classical PoA with corner component and dl db"""
        length = l_E0 + dlE
        width = b_E0 + dbE
        area = length * width
        perimeter = 2 * (length + width)
        return area * quantity_per_area + perimeter * quantity_per_perimeter + quantity_corner
