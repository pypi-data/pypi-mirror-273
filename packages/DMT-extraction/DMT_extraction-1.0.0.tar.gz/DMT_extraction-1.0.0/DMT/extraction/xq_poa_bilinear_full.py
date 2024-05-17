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

from scipy import interpolate
import numpy as np
import warnings
import copy

from DMT.core import unit_registry, constants
from DMT.core import DutType, McParameter, Plot, specifiers, sub_specifiers
from DMT.extraction import XStep, plot, Model, print_to_documentation
from DMT.extraction import find_nearest_index, IYNormLog

# pylint: disable=redefined-outer-name


class XQPoaBilinearFull(XStep):
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
    mcard          : DMT.core.McParameterCollection
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
    config         : str
        Configuration of the device. (Optional)
    corner_rounding : Boolean, False
        If True, use bilinear corner rounding equation.
    exclude : tuple, None
        A tuple whose first entry is the minimum length that is considered for scaling and the second entry the minimum width.
    """

    def __init__(
        self,
        name,
        mcard,
        lib,
        op_definition,
        quantity,
        quantity_scale,
        sweep_voltage,
        dut_type=DutType.npn,
        scale_along="width",
        scale_at=None,
        legend_off=True,
        config=None,
        exclude=None,
        corner_rounding=False,
        use_exact_key=True,
        nfinger=None,
        **kwargs,
    ):
        self.config = config
        self.exclude = exclude
        temp = op_definition["TEMP"]
        if not isinstance(temp, (float, int)) and len(temp) > 1:
            raise IOError(
                "DMT -> XPoa -> The POA separation can be only done for one temperature in one XQStep."
            )

        if nfinger is None:
            if config == "CBEBC":
                nfinger = 1
            elif config == "CBEBEBC":
                nfinger = 2
            else:
                nfinger = 1  # Unsupported contact config

        # self.name_dlE = '_dlE_' + quantity.to_raw_string() + '_' + '{0:.2f}'.format(op_definition['TEMP'])
        # self.name_dbE = '_dbE_' + quantity.to_raw_string() + '_' + '{0:.2f}'.format(op_definition['TEMP'])

        # try:
        #     possible_parameters = kwargs.pop('possible_parameters')
        # except KeyError:
        #     possible_parameters = [self.name_dlE, self.name_dbE]

        if not use_exact_key:
            raise IOError(
                "DMT -> XPoa: Poa step needs exact key in order to write back the results correctly."
            )

        self.quantity_scale = quantity_scale
        for speci, vals in op_definition.items():
            if str(speci) == str(sweep_voltage):
                if None in vals:
                    raise IOError(
                        name
                        + ': "None" is not allowed in the op_definition for the specifier defined by the "sweep_voltage" argument. Specify a concrete value.'
                    )
                try:
                    self.low = np.min(vals[0])
                    self.upp = np.max(vals[1])
                    self.mid = np.mean(vals[:2])
                    break
                except IndexError:
                    raise IOError(
                        name
                        + ": You need to pass an upper and lower boundary for the sweep voltage in the op_definition.\n Currently the op_definition is :"
                        + speci
                        + ":"
                        + str(vals)
                        + " and the sweep voltage ist "
                        + sweep_voltage
                        + "."
                    )

        else:
            raise IOError(
                'The specifier from the "sweep_voltage" keyword argument ( '
                + str(sweep_voltage)
                + " ) to "
                + name
                + " must also be part of the op_definition dictionary."
            )

        self.corner_rounding = corner_rounding
        if self.corner_rounding:
            self.model_function = self.quantity_poa_recr
        else:
            self.model_function = self.quantity_poa

        self.model_function_info = {"independent_vars": ("l_E0", "b_E0")}

        # init the super class
        super().__init__(
            name,
            mcard,
            lib,
            op_definition,
            model=Model("dummy", 1, [], []),  # don't really need a model here
            legend_off=legend_off,
            use_exact_key=use_exact_key,
            specifier_paras={
                "quantity": None,
                "sweep_voltage": None,
            },
            sweep_voltage=sweep_voltage,
            quantity=quantity,
            **kwargs,
        )

        self.voltage = self.specifier_paras["sweep_voltage"]
        self.quantity = self.specifier_paras["quantity"]
        self.dut_type = dut_type
        self.scale_along = scale_along
        self.negative = False
        self.nfinger = nfinger

        if scale_at is None:
            if scale_along == "width":
                self.scale_at = getattr(
                    lib.dut_ref, "length"
                )  # if scaling is along width, fix length
            elif scale_along == "length":
                self.scale_at = getattr(
                    lib.dut_ref, "width"
                )  # if scaling is along length, fix width
            else:
                self.scale_at = None
        else:
            self.scale_at = scale_at

        if "relevant_duts" in kwargs.keys():  # user supplied relevant devices
            self.relevant_duts = kwargs["relevant_duts"]
        else:
            self.relevant_duts = [dut for dut in self.lib if self.filter_function(dut)]

        if quantity.specifier == specifiers.CURRENT or quantity.specifier == specifiers.CAPACITANCE:
            self.iynorm = IYNormLog  # logarithmic normalization is advantageous for currents

        self.quantity_poa_info = {"independent_vars": ("l_E0", "b_E0")}

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

        main_plot = super(XQPoaBilinearFull, self).main_plot(
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

    def get_dut_key(self, key, dut):
        """Returns the original DuT key to write back results into a static persistant dataframe"""
        key_parts = dut.split_key(key)  # '_', self.__class__.__name__, self.name, key)
        return dut.join_key(*key_parts[3:])

    def ensure_input_correct(self):
        """Search for all required columns in the data frames. Check whether the scaling specifications make sense."""
        if (
            self.scale_along != "width"
            and self.scale_along != "length"
            and self.scale_along != "both"
        ):
            raise IOError(
                "DMT -> XPoa -> ensure_input_correct: I can only scale along width, length or both!"
            )

        if not len(self.relevant_duts) > 1:  # we need more than one dut for scaling
            raise IOError(
                "DMT -> XPoa -> ensure_input_correct: Input not correct. "
                "The given combination of dut_ref, scale_at and scale_along gave less than one Dut to analyze, which makes no sense."
            )

        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    data = dut.data[key]
                    try:
                        data.ensure_specifier_column(self.quantity, ports=self.lib.dut_ref.ac_ports)
                    except KeyError as err:
                        raise IOError(
                            err.args[0]
                            + "\nThe column was missing in the data frame with the key "
                            + key
                            + "."
                        )

    def filter_function(self, dut):
        """This function returns true for duts that are suitable for scaling along scale_along at a fixed scale_at value."""
        if id(dut) == id(self.lib.dut_ref):
            dummy = 1
        if not dut.dut_type == self.dut_type:
            return False

        if self.config is not None:  # check device configuration
            if not dut.contact_config == self.config:
                return False

        if self.exclude is not None:  # check if this geometry is used for scaling
            if dut.length <= self.exclude[0]:
                return False
            if dut.width <= self.exclude[1]:
                return False

        if hasattr(dut, self.scale_along):
            if self.scale_along == "width":
                dimension_value = getattr(dut, "length")  # if scaling is along width, fix length
            elif self.scale_along == "length":
                dimension_value = getattr(dut, "width")  # if scaling is along length, fix width

            if np.isclose(dimension_value, self.scale_at, rtol=0.05, atol=1e-9):
                return True
            else:
                return False
        else:  # if scale along == "both":
            return True

    def set_initial_guess(self, data_reference):
        """In contrast to XStep set_initial_guess, this method needs to set an initial guess for each line and init the parameter arrays."""
        if "dlE" in self.paras_to_optimize.name:
            para_dlE = self.paras_to_optimize["dlE"]
            if para_dlE.value == 0:
                para_dlE.value = -1e-9

            length_min = min([dut.length for dut in self.relevant_duts])
            para_dlE.min = -length_min
            para_dlE.max = length_min

            self.mcard.set(para_dlE)

        if "dbE" in self.paras_to_optimize.name:
            para_dbE = self.paras_to_optimize["dbE"]
            if para_dbE.value == 0:
                para_dbE.value = -1e-9

            width_min = min([dut.width for dut in self.relevant_duts])
            para_dbE.min = -width_min
            para_dbE.max = width_min
            self.mcard.set(para_dbE)

        for line, composition in zip(self.data_reference, self.paras_to_optimize_per_line):
            self.set_initial_guess_line(composition, line)

        unit = unit_registry.meter
        try:
            self.mcard["dbE"].unit = unit
            self.mcard["dlE"].unit = unit
        except IndexError:
            pass

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

        # assume all quantity of line comes through quantity_area
        val_a = np.mean(line["quantity"] / (line["l_E0"] * line["b_E0"]))
        para_a = McParameter(
            "quantity_per_area", value=np.abs(val_a), minval=0, maxval=np.abs(val_a) * 2
        )
        composition.set(para_a)

        # assume all quantity of line comes through quantity_length
        val_p = np.mean(line["quantity"] / (2 * line["l_E0"]))
        para_l = McParameter(
            "quantity_per_length", value=val_p, minval=0, maxval=np.abs(val_p) * 2
        )  # nice staring value i think
        try:
            composition.set(para_l)
        except KeyError:
            # composition.add(para_l)
            pass

        # assume all quantity of line comes through quantity_width
        val_p = np.mean(line["quantity"] / (2 * line["b_E0"])) / 2
        para_b = McParameter(
            "quantity_per_width", value=val_p, minval=0, maxval=np.abs(val_p) * 2
        )  # nice staring value i think
        try:
            composition.set(para_b)
        except KeyError:
            # composition.add(para_b)
            pass

        # assume all quantity of line comes through quantity_length
        val_p = np.max(line["quantity"])
        para_c = McParameter("quantity_corner", value=val_p, minval=0, maxval=np.abs(val_p))
        try:
            composition.set(para_c)
        except KeyError:
            # composition.add(para_c)
            pass

    def fit(self, line, paras_model):
        """Set the y-values, using one quantity_a for each line and one quantity_p for all lines."""
        if self.corner_rounding:
            paras = [
                "dle",
                "dbe",
                "recr",
                "quantity_per_area",
                "quantity_per_length",
                "quantity_per_width",
                "quantity_corner",
            ]
        else:
            paras = [
                "dle",
                "dbe",
                "quantity_per_area",
                "quantity_per_length",
                "quantity_per_width",
                "quantity_corner",
            ]

        para_values = paras_model.get_values(paras)
        line["y"] = self.model_function(b_E0=line["b_E0"], l_E0=line["l_E0"], **para_values) / (
            line["b_E0"] * line["l_E0"]
        )
        # linye['y'] = (line['y'] - y_ref)
        return line

    def init_data_reference(self):
        """Go through all relevant duts and extract I_B."""
        v_in_all_df, voltages = None, None
        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    data = dut.data[key]
                    voltages = np.round(self.get_operating_points(data), 3)

                    if v_in_all_df is None:
                        v_in_all_df = voltages
                        continue

                    # this creates a list of all voltages common to the measurements, including the current data
                    v_in_all_df = [voltage for voltage in v_in_all_df if voltage in voltages]

        v_in_all_df.sort()

        if voltages is None:
            raise IOError(
                "DMT -> XQPoaBilinearFull: Something went wrong when finding common voltages."
            )

        if len(v_in_all_df) == 1:
            raise IOError(
                "DMT -> XQPoaBilinearFull: only one voltage common to all data. Not suitable for PoA analysis."
            )

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
                print(
                    f"XQPoaBilinearFull: Skipping bias point {voltage} less the 2 geometries were found"
                )
                continue

            quantities_per_area0 = np.asarray(quantities_per_area0)
            l_E0 = np.asarray(l_E0)
            b_E0 = np.asarray(b_E0)
            quantities = np.asarray(quantities)

            line = {
                "y": quantities_per_area0 / self.nfinger,
                "y_ref": quantities_per_area0 / self.nfinger,
                "x": 2 * (l_E0 + b_E0) / (l_E0 * b_E0),
                "quantity": quantities,
                "l_E0": l_E0,
                "b_E0": b_E0,
                "area": l_E0 * b_E0,
                "voltage": voltage,
            }

            self.data_reference.append(line)
            self.labels.append(
                r"$" + self.voltage.to_tex() + r"=\SI{" + str(voltage) + r"}{V}$"
            )  # ensures nice labels in the plot

        # catch negative quantities, e.g. reverse gummel IC
        self.negative = False
        for line in self.data_reference:
            if not self.negative:
                if (line["y"] < 0).all():
                    print("PoA analysis using negative y axis.")
                    self.negative = True
            elif self.negative:
                if (line["y"] > 0).any():
                    raise IOError("mixed negative and positive quantities in PoA not implemented.")

        if self.negative:
            for line in self.data_reference:
                line["y"] = np.abs(line["y"])

    def collect_data(self):
        """This is overwriten here since this step wants to save the new keys, too!"""
        super().collect_data()
        for dut in self.relevant_duts:
            for key in list(dut.data.keys()):
                if (
                    self.validate_key(key) and key[0] == "_"
                ):  # old specifier that indicates not saving this data
                    new_key = "q" + key[1:]  # new specifier so that the data will be saved
                    dut.data[new_key] = dut.data.pop(key)

    # Just plotting from here on ###############
    @plot()
    @print_to_documentation()
    def plot_quantity_scaled_fit(self):
        """Plot quantity as a function of operating point meas vs fit for multiple geometries for all analyzed duts"""
        plot = Plot(
            r"Application of scaling equation.",
            style="xtraction_color",
            num=self.name + " Q (V) fit",
            x_label=self.voltage.to_label(),
            y_label=self.quantity.to_label(scale=self.quantity_scale, negative=self.negative),
        )
        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    label = (
                        r"$\left("
                        + f"{dut.length*1e6:.1f}"
                        + r","
                        + f"{dut.width*1e6:.2f}"
                        + r"\right)$"
                    )
                    data = dut.data[key]

                    voltages_ref = self.get_operating_points(data)
                    quantity_ref = [self.get_quantity(data, voltage) for voltage in voltages_ref]
                    quantity_ref = np.abs(np.asarray(quantity_ref)) * self.quantity_scale

                    try:  # for subclass that has pfunc...ok this is a little dirty ;)
                        x = self.pfunc(
                            dut.length,
                            dut.width,
                            dlE=self.mcard["dlE"].value,
                            dbE=self.mcard["dbE"].value,
                            gamma_l=self.mcard["gamma_l"].value,
                            gamma_b=self.mcard["gamma_b"].value,
                        )
                    except:
                        x = dut.perimeter

                    try:  # for subclass that has afunc...ok this is a little dirty ;)
                        area = self.afunc(
                            dut.length,
                            dut.width,
                            dlE=self.mcard["dlE"].value,
                            dbE=self.mcard["dbE"].value,
                            gamma_l=self.mcard["gamma_l"].value,
                            gamma_b=self.mcard["gamma_b"].value,
                        )
                    except:
                        area = dut.area

                    indexes = [find_nearest_index(x / area, line["x"]) for line in self.data_model]

                    quantity_model = [
                        line["y"][index] * area for index, line in zip(indexes, self.data_model)
                    ]
                    quantity_model = np.asarray(quantity_model) * self.quantity_scale * self.nfinger
                    voltages_model = [line["voltage"] for line in self.data_model]
                    voltages_model = np.asarray(voltages_model)

                    # if self.quantity.specifier == specifiers.CURRENT:
                    #     vt=constants.calc_VT(dut.get_key_temperature(key))
                    #     plot.add_data_set(voltages_ref, quantity_ref/np.exp(voltages_ref/vt)      , label=label)
                    #     plot.add_data_set(voltages_model, quantity_model/np.exp(voltages_model/vt), label=None)
                    # else:
                    plot.add_data_set(voltages_ref, quantity_ref, label=label)
                    plot.add_data_set(voltages_model, quantity_model, label=None)

        plot.legend_location = "upper left"

        if self.quantity.specifier == specifiers.CURRENT:
            plot.y_axis_scale = "log"

        return plot

    @plot()
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
        try:
            data = self.df_separated
        except AttributeError:
            return None
        voltages = self.get_operating_points(data)
        quantity_meas = [self.get_quantity(data, voltage) for voltage in voltages]

        plot.add_data_set(
            voltages,
            np.abs(np.asarray(quantity_meas) * self.quantity_scale),
            label=r"$" + self.quantity.to_tex(subscript="", superscript="") + r"\,\mathrm{meas.}$ ",
            style="sk",
        )
        plot.add_data_set(
            voltages,
            np.abs((data[col_perimeter] + data[col_area])) * self.quantity_scale,
            label=r"$" + self.quantity.to_tex() + r"\mathrm{\,model}$",
            style="-k",
        )

        plot.add_data_set(
            voltages,
            np.abs(data[col_area] * self.quantity_scale),
            label=r"$"
            + self.quantity.to_tex(subscript="A", superscript="''")
            + r"A_{\mathrm{E0}}$",
            style="--r",
        )
        # plot.add_data_set(
        #     voltages,
        #     np.abs(data[col_perimeter] * self.quantity_scale),
        #     label=r"$" + self.quantity.to_tex(subscript="P", superscript="'") + r"P_{\mathrm{E0}}$",
        # )

        plot.add_data_set(
            voltages,
            np.abs(data[col_length] * self.quantity_scale),
            label=r"$" + self.quantity.to_tex(subscript="l", superscript="'") + r"l_{\mathrm{E0}}$",
            style="--<b",
        )
        plot.add_data_set(
            voltages,
            np.abs(data[col_width] * self.quantity_scale),
            label=r"$" + self.quantity.to_tex(subscript="b", superscript="'") + r"b_{\mathrm{E0}}$",
            style="-.m",
        )
        plot.add_data_set(
            voltages,
            np.abs(data[col_corner] * self.quantity_scale),
            label=r"$" + self.quantity.to_tex(subscript="c", superscript="") + r"$ ",
            style="--og",
        )

        plot.legend_location = "upper left"

        if self.quantity.specifier == specifiers.CURRENT:
            plot.y_axis_scale = "log"
        return plot

    # @plot()
    # @print_to_documentation()
    # def plot_quantity_density_separated(self):
    #     """ Plot quantity as a function of operating point meas vs fit for multiple geometries for all analyzed duts
    #     """

    #     plot = Plot(r'$' + self.quantity.to_tex() + r'$ density along width/length separated for reference device.', style='mix', num=self.name + ' Q (V) density seperated'
    #         , x_label=self.voltage.to_label()
    #         , y_label=r'$' + self.quantity.to_tex(subscript=r'l(b)', superscript="'") + r'/' + self.quantity.get_tex_unit(scale=self.quantity_scale, add=r'\per\micro\meter') + r'$'
    #     )
    #     for key in self.dut_ref.data.keys():
    #         if self.validate_key(key):
    #             data     = self.dut_ref.data[key]
    #             voltages = self.get_operating_points(data)
    #             quantitiy_per_length = data['q_per_length'] * self.quantity_scale/1e6 #per um
    #             quantitiy_per_width  = data['q_per_width']  * self.quantity_scale/1e6 #per um
    #             plot.add_data_set(voltages, quantitiy_per_length, label=r'$' + self.quantity.to_tex(subscript='l', superscript="'") + r'$')
    #             plot.add_data_set(voltages, quantitiy_per_width , label=r'$' + self.quantity.to_tex(subscript='b', superscript="'") + r'$')

    #     plot.legend_location = 'upper left'
    #     return plot

    # the letters are there since plots are printed to documentation alphabetically

    @plot()
    def plot_quantity_lEdrawn_a(self):
        return self.get_plot_along_dimension(
            along="length",
            delta=0,
            op=self.low,
            num=self.name + " Q(l_E,drawn) {:1.1f}V".format(self.low),
        )

    @plot()
    def plot_quantity_lEdrawn_b(self):
        return self.get_plot_along_dimension(
            along="length",
            delta=0,
            op=self.mid,
            num=self.name + " Q(l_E,drawn) {:1.1f}V".format(self.mid),
        )

    @plot()
    def plot_quantity_lEdrawn_c(self):
        return self.get_plot_along_dimension(
            along="length",
            delta=0,
            op=self.upp,
            num=self.name + " Q(l_E,drawn) {:1.1f}V".format(self.upp),
        )

    @plot()
    def plot_quantity_bEdrawn_a(self):
        return self.get_plot_along_dimension(
            along="width",
            delta=0,
            op=self.low,
            num=self.name + " Q (b_E,drawn) {:1.1f}V".format(self.low),
        )

    @plot()
    def plot_quantity_bEdrawn_b(self):
        return self.get_plot_along_dimension(
            along="width",
            delta=0,
            op=self.mid,
            num=self.name + " Q (b_E,drawn) {:1.1f}V".format(self.mid),
        )

    @plot()
    def plot_quantity_bEdrawn_c(self):
        return self.get_plot_along_dimension(
            along="width",
            delta=0,
            op=self.upp,
            num=self.name + " Q (b_E,drawn) {:1.1f}V".format(self.upp),
        )

    @plot()
    @print_to_documentation()
    def plot_quantity_bE_c_high(self):
        return self.get_plot_along_dimension(
            along="width",
            delta=self.mcard["dbE"].value,
            op=self.upp,
            num=self.name + " Q (b_E) {:1.1f}V".format(self.upp),
        )

    @plot()
    @print_to_documentation()
    def plot_quantity_bE_b_mid(self):
        return self.get_plot_along_dimension(
            along="width",
            delta=self.mcard["dbE"].value,
            op=self.mid,
            num=self.name + " Q (b_E) {:1.1f}V".format(self.mid),
        )

    @plot()
    @print_to_documentation()
    def plot_quantity_bE_a_low(self):
        return self.get_plot_along_dimension(
            along="width",
            delta=self.mcard["dlE"].value,
            op=self.low,
            num=self.name + " Q (b_E) {:1.1f}V".format(self.low),
        )

    @plot()
    @print_to_documentation()
    def plot_quantity_lE_c_high(self):
        return self.get_plot_along_dimension(
            along="length",
            delta=self.mcard["dlE"].value,
            op=self.upp,
            num=self.name + " Q (l_E) {:1.1f}V".format(self.upp),
        )

    @plot()
    @print_to_documentation()
    def plot_quantity_lE_b_mid(self):
        return self.get_plot_along_dimension(
            along="length",
            delta=self.mcard["dlE"].value,
            op=self.mid,
            num=self.name + " Q (l_E) {:1.1f}V".format(self.mid),
        )

    @plot()
    @print_to_documentation()
    def plot_quantity_lE_a_low(self):
        return self.get_plot_along_dimension(
            along="length",
            delta=self.mcard["dlE"].value,
            op=self.low,
            num=self.name + " Q (l_E) {:1.1f}V".format(self.low),
        )

    def get_plot_along_dimension(self, along=None, delta=None, op=None, num=None):
        """Return an array of the quantity along length or width, at width or length with an delta at an operating point and a fit line"""
        # init the plot
        if along == "width":
            str_ = "b"
        else:
            str_ = "l"

        if delta == 0:
            x_label = r"$" + str_ + r"_{\mathrm{E,drawn}}\left(\si{\micro\meter}\right)$"
            title = (
                "$"
                + self.quantity.to_tex()
                + r"("
                + str_
                + r"_{\mathrm{E,drawn}}                      )@"
                + self.voltage.to_tex()
                + r"=\SI{"
                + str(op)
                + r"}{\volt}$"
            )
        else:
            x_label = (
                # r"$\left( "
                "$"
                + str_
                + r"_{\mathrm{E,drawn}} + \Delta "
                + str_
                # + r" \right)/\si{\micro\meter}$"
                + r" \left(\si{\micro\meter}\right)$"
            )
            title = (
                "$"
                + self.quantity.to_tex()
                + r"("
                + str_
                + r"_{\mathrm{E,drawn}} + \Delta "
                + str_
                + r")@"
                + self.voltage.to_tex()
                + r"=\SI{"
                + str(op)
                + r"}{\volt}$"
            )

        plot = Plot(
            title,
            x_label=x_label,
            y_label=self.quantity.to_label(scale=self.quantity_scale, negative=self.negative),
            y_scale=self.quantity_scale,
            x_scale=1e6,
            style="xtraction",
            num=num,
        )

        # loop over all dimensions, in the end we can sort...
        quantity = []
        lengths = []
        widths = []
        for dut in self.relevant_duts:
            for key in dut.data.keys():
                if self.validate_key(key):
                    data = dut.data[key]
                    # this way the order makes sense
                    quantity.append(self.get_quantity(data, op))
                    lengths.append(dut.length)
                    widths.append(dut.width)

        lengths = np.asarray(lengths).round(decimals=10)  # given in um usually
        widths = np.asarray(widths).round(decimals=10)

        # now see what we want to scale along
        quantities_at = []
        x_axes = []
        if along == "width":
            at = np.unique(lengths)
        elif along == "length":
            at = np.unique(widths)

        for at_ in at:
            if along == "width":
                indices = [
                    i for i in range(len(lengths)) if lengths[i] == at_
                ]  # indices where we want to take the quantity
            else:
                indices = [
                    i for i in range(len(widths)) if widths[i] == at_
                ]  # indices where we want to take the quantity

            quantities_at.append(np.abs(np.asarray([quantity[i] for i in indices])))
            if along == "width":
                x_axes.append(np.asarray([widths[i] for i in indices]))
            else:
                x_axes.append(np.asarray([lengths[i] for i in indices]))

        # account for delta
        for i, x_axis in enumerate(x_axes):
            x_axes[i] = x_axis + delta

        # sort and find fit line
        # pylint: disable = cell-var-from-loop
        fit_lines = []
        for i, (x_axis, quantity_at) in enumerate(zip(x_axes, quantities_at)):
            i_sort = np.argsort(x_axis)
            x_axes[i] = x_axis[i_sort]
            quantities_at[i] = quantity_at[i_sort]
            if len(x_axes[i]) > 1:  # also find a fitline
                p = np.polyfit(x_axes[i], quantities_at[i], 1)
                fit_line = lambda x: p[0] * np.asarray(x) + p[1]
                fit_lines.append(fit_line([0] + x_axes[i].tolist()))
            else:
                fit_lines.append(None)

        # prepare labels
        if along == "width":
            label = r"$l_\mathrm{{E,drawn}}={0:1.2f}\si{{\micro\meter}}$"
        elif along == "length":
            label = r"$b_\mathrm{{E,drawn}}={0:1.2f}\si{{\micro\meter}}$"

        # quantities_at = np.abs(quantities_at, dtype=object)
        for x_axis, quantity_at, fit_line, at_ in zip(x_axes, quantities_at, fit_lines, at):
            # add the measured data
            plot.add_data_set(
                np.asarray(x_axis), np.array(quantity_at), label=label.format(at_ * 1e6)
            )
            # only need fit line if more than one data point...
            if fit_line is not None:
                plot.add_data_set(np.asarray([0] + (x_axis).tolist()), fit_line, label=None)
            else:
                # add dummy so that labels are nice
                plot.add_data_set(np.asarray([-1e-6]), quantity_at, label=None)

        plot.legend_location = "upper left"
        plot.x_limits = (0, None)
        plot.y_limits = (0, None)
        return plot

    @plot()
    @print_to_documentation()
    def scaling_plot(self, mcard=None):
        """Plots Q/A vs P/A with actual lengths and widths"""
        if mcard is None:
            mcard = self.mcard

        scl_plot = Plot(
            r"$"
            + self.quantity.to_tex()
            + r"/A_{\mathrm{E0}}\left( P_{\mathrm{E0}}/A_{\mathrm{E0}} \right) $",
            style="xtraction_color",
            num=self.name + " scaling plot",
            y_label=r"$"
            + self.quantity.to_tex()
            + r"/A_{\mathrm{E0}}\left("
            + self.quantity.get_tex_unit(scale=self.quantity_scale, add=r"\per\square\micro\meter")
            + r"\right)$",
            x_label=r"$P_{\mathrm{E0}}/A_{\mathrm{E0}} \left(\si{\per\micro\meter}\right)$",
        )
        if self.negative:
            scl_plot.y_label = r"$-" + self.quantity.to_tex() + r"/A_{\mathrm{E0}}$"

        if self.main_fig is None:  # Crash otherwise
            self.main_plot()

        for line_reference, line_model, label in zip(
            self.data_reference, self.data_model, self.labels
        ):  # add the reference and model data in an alternating way
            if self.corner_rounding:
                recr = mcard["recr"].value
                l = line_reference["l_E0"] + mcard["dlE"].value
                b = line_reference["b_E0"] + mcard["dbE"].value
                A_E0 = l * b - (4 - np.pi) * recr**2
                P_E0 = 2 * (l - 2 * recr) + +2 * (b - 2 * recr) + 2 * np.pi * recr
                l = line_model["l_E0"] + mcard["dlE"].value
                b = line_model["b_E0"] + mcard["dbE"].value
                A_E0_m = l * b - (4 - np.pi) * recr**2
                P_E0_m = 2 * (l - 2 * recr) + +2 * (b - 2 * recr) + 2 * np.pi * recr

            else:
                l = line_reference["l_E0"] + mcard["dlE"].value
                b = line_reference["b_E0"] + mcard["dbE"].value
                A_E0 = l * b
                P_E0 = 2 * (l + b)
                l = line_model["l_E0"] + mcard["dlE"].value
                b = line_model["b_E0"] + mcard["dbE"].value
                A_E0_m = l * b
                P_E0_m = 2 * (l + b)

            q_ref = line_reference["quantity"]
            q_mod = line_model["quantity"]

            if not self.legend_off:
                scl_plot.add_data_set(
                    P_E0 / A_E0 * self.main_fig.x_scale,
                    np.abs(q_ref) / A_E0 * self.main_fig.y_scale,
                    label="reference " + label,
                )
                scl_plot.add_data_set(
                    P_E0_m / A_E0_m * self.main_fig.x_scale,
                    np.abs(q_mod) / A_E0_m * self.main_fig.y_scale,
                    label="model " + label,
                )
            else:
                scl_plot.add_data_set(
                    P_E0 / A_E0 * self.main_fig.x_scale,
                    np.abs(q_ref) / A_E0 * self.main_fig.y_scale,
                )
                scl_plot.add_data_set(
                    P_E0_m / A_E0_m * self.main_fig.x_scale,
                    np.abs(q_mod) / A_E0_m * self.main_fig.y_scale,
                )

        scl_plot.x_limits = (0, None)
        scl_plot.y_limits = (0, None)
        return scl_plot

    def optimize(self):
        super().optimize()
        self.write_back_results()

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
            quantity_area, quantity_length, quantity_width, quantity_corner = (
                np.zeros(np.size(self.data_model)),
                np.zeros(np.size(self.data_model)),
                np.zeros(np.size(self.data_model)),
                np.zeros(np.size(self.data_model)),
            )

            # get dl0 and db0
            dle = self.mcard["dle"].value
            dbe = self.mcard["dbe"].value
            params = self.mcard.to_kwargs()
            if self.corner_rounding:
                recr = self.mcard["recr"].value
            else:
                recr = 0

            for i, composition in enumerate(self.paras_to_optimize_per_line):
                # true also with corner rounding:
                length = 2 * (dut.length + dle - 2 * recr)
                width = 2 * (dut.width + dbe - 2 * recr)
                area = (dut.length + dle) * (dut.width + dbe) - (4 - np.pi) * recr**2

                composition_kwargs = composition.to_kwargs()
                if self.corner_rounding:
                    composition_kwargs["recr"] = recr

                try:
                    quantity_area[i] = area * composition["quantity_per_area"].value
                except KeyError:
                    quantity_area[i] = 0

                try:
                    quantity_length[i] = length * composition["quantity_per_length"].value
                except KeyError:
                    quantity_length[i] = 0

                try:
                    quantity_width[i] = width * composition["quantity_per_width"].value
                except KeyError:
                    quantity_width[i] = 0

                quantity_corner[i] = (
                    self.model_function(
                        l_E0=dut.length,
                        b_E0=dut.width,
                        dle=dle,
                        dbe=dbe,
                        **composition_kwargs,
                    )
                    - quantity_area[i]
                    - quantity_length[i]
                    - quantity_width[i]
                )

            # modeled quantity directly
            try:  # for subclass that has xfunc...ok this is a little dirty ;)
                x = self.pfunc(
                    dut.length,
                    dut.width,
                    self.mcard["dlE"].value,
                    self.mcard["dbE"].value,
                    self.mcard["gamma_l"].value,
                    self.mcard["gamma_b"].value,
                )
            except AttributeError:
                x = dut.perimeter

            indexes = [find_nearest_index(x / dut.area, line["x"]) for line in self.data_model]
            quantity_model = [
                line["y"][index] * dut.area for index, line in zip(indexes, self.data_model)
            ]
            quantity_model = np.asarray(quantity_model)

            # interpolate
            voltages_df = self.get_operating_points(dut.data[key_dut])
            try:
                f_quantity_area = interpolate.interp1d(
                    voltages_data, quantity_area, kind=3, fill_value="extrapolate"
                )
                f_quantity_length = interpolate.interp1d(
                    voltages_data, quantity_length, kind=3, fill_value="extrapolate"
                )
                f_quantity_width = interpolate.interp1d(
                    voltages_data, quantity_width, kind=3, fill_value="extrapolate"
                )
                f_quantity_corner = interpolate.interp1d(
                    voltages_data, quantity_corner, kind=3, fill_value="extrapolate"
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
                f_quantity_length = interpolate.interp1d(
                    voltages[i_sort],
                    np.asarray(quantity_length)[i_sort],
                    kind=3,
                    fill_value="extrapolate",
                )
                f_quantity_width = interpolate.interp1d(
                    voltages[i_sort],
                    np.asarray(quantity_width)[i_sort],
                    kind=3,
                    fill_value="extrapolate",
                )
                f_quantity_corner = interpolate.interp1d(
                    voltages[i_sort],
                    np.asarray(quantity_corner)[i_sort],
                    kind=3,
                    fill_value="extrapolate",
                )

            sign = 1
            if self.negative:
                sign = -1

            quantity_area = sign * f_quantity_area(voltages_df) * self.nfinger
            quantity_length = sign * f_quantity_length(voltages_df) * self.nfinger
            quantity_width = sign * f_quantity_width(voltages_df) * self.nfinger
            quantity_corner = sign * f_quantity_corner(voltages_df) * self.nfinger

            # copy to local dataframe
            col_width, col_length, col_area, col_corner, col_perimeter = self.get_cols_poa_full()
            df = copy.deepcopy(dut.data[key_dut])
            df[col_width] = quantity_width
            df["q_per_width"] = (
                quantity_width / (dut.width + dbe) * 0.5
            )  # just for plotting the edge densities
            df[col_length] = quantity_length
            df["q_per_length"] = (
                quantity_length / (dut.length + dle) * 0.5
            )  # just for plotting the edge densities
            df[col_area] = quantity_area
            df[col_corner] = quantity_corner
            df[col_perimeter] = quantity_corner + quantity_width + quantity_length
            dut.add_data(df, key=key_dut, force=True)
            if dut == self.lib.dut_ref:
                self.df_separated = df

            # assert np.allclose(quantity_area + quantity_length + quantity_width + quantity_corner, quantity_model, rtol=1e-3)
            # assert np.allclose(df[col_area]  + df[col_perimeter] , quantity_model, rtol=1e-3)

            # # copy to persistent dataframe
            # key_dut     = self.get_dut_key(key_dut, dut)
            # voltages_df = self.get_operating_points(dut.data[key_dut])

            # # new interpolation
            # quantity_area   = sign*f_quantity_area(voltages_df)
            # quantity_length = sign*f_quantity_length(voltages_df)
            # quantity_width  = sign*f_quantity_width(voltages_df)
            # quantity_corner = sign*f_quantity_corner(voltages_df)

            # #this needs to be implemented in the subclass of xpoa
            # df = copy.deepcopy(dut.data[key_dut])
            # df[col_width]     = quantity_width
            # df[col_length]    = quantity_length
            # df[col_area]      = quantity_area
            # df[col_corner]    = quantity_corner
            # df[col_perimeter] = quantity_corner + quantity_width + quantity_length
            # dut.add_data(df, key=key_dut, force=True)

    def get_tex(self):
        if self.corner_rounding:
            return (
                r"\frac{ "
                + self.quantity.to_tex()
                + r" }{ A_{\mathrm{E0}} } "
                + r"= "
                + self.quantity.to_tex(subscript="A", superscript="''")
                + r" "
                + r"+ \frac{ l_{\mathrm{E0}} }{ A_{\mathrm{E0}} } "
                + self.quantity.to_tex(subscript="l", superscript="'")
                + r"+ \frac{ b_{\mathrm{E0}} }{ A_{\mathrm{E0}} } "
                + self.quantity.to_tex(subscript="b", superscript="'")
                + r"+ \frac{ 1 }{ A_{\mathrm{E0}}} "
                + self.quantity.to_tex(subscript="c")
                + r" \\ A_{\mathrm{E0}} = \left( l_{\mathrm{E0}}-2r_{\mathrm{ecr}} \right) \left( b_{\mathrm{E0}} -2r_{\mathrm{ecr}} \right) - \left( 4 - \pi \right) r_{\mathrm{ecr}}^2 \\"
                + r" \\ P_{\mathrm{E0}} = 2 \left( l_{\mathrm{E0}}-2r_{\mathrm{ecr}} + b_{\mathrm{E0}}-2r_{\mathrm{ecr}} \right) \\"
                + r" \\ l_{\mathrm{E0}} = l_{\mathrm{E,drawn}} + \Delta l_{\mathrm{E}} \\"
                + r" \\ b_{\mathrm{E0}} = b_{\mathrm{E,drawn}} + \Delta b_{\mathrm{E}}"
            )
        else:
            return (
                r"\frac{ "
                + self.quantity.to_tex()
                + r" }{ A_{\mathrm{E0}} } "
                + r"= "
                + self.quantity.to_tex(subscript="A", superscript="''")
                + r" "
                + r"+ \frac{ l_{\mathrm{E0}} }{ A_{\mathrm{E0}} } "
                + self.quantity.to_tex(subscript="l", superscript="'")
                + r"+ \frac{ b_{\mathrm{E0}} }{ A_{\mathrm{E0}} } "
                + self.quantity.to_tex(subscript="b", superscript="'")
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
        if self.corner_rounding:
            doc.append(
                NoEscape(
                    r"This extraction step performs the PoA separation of $"
                    + self.quantity.to_tex()
                    + r"$. "
                )
            )
            doc.append(NoEscape(r"For advanced HBT technologies, the classical PoA separation"))
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
            doc.append(NoEscape(r"$A_{\mathrm{E0}}$ is the emitter window area and "))
            doc.append(NoEscape(r"$P_{\mathrm{E0}}$ is the emitter window perimeter, "))
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
                    + self.quantity.to_tex(subscript="l", superscript="'")
                    + r"$ is the "
                    + self.quantity.get_descriptor()
                    + r" per emitter length, "
                )
            )
            doc.append(
                NoEscape(
                    r"$"
                    + self.quantity.to_tex(subscript="b", superscript="'")
                    + r"$ is the "
                    + self.quantity.get_descriptor()
                    + r" per emitter width, "
                )
            )
            doc.append(
                NoEscape(
                    r"$"
                    + self.quantity.to_tex(subscript="c", superscript="")
                    + r"$ is the "
                    + self.quantity.get_descriptor()
                    + r" corner component, "
                )
            )
            doc.append(NoEscape(r"$l_{\mathrm{E0}}^{}$ is the emitter window length, "))
            doc.append(NoEscape(r"$b_{\mathrm{E0}}^{}$ is the emitter window width, "))
            doc.append(
                NoEscape(r"$r_{\mathrm{ecr}}^{}$ is the emitter window corner rounding radius, ")
            )
            doc.append(NoEscape(r"$P_{\mathrm{E0}}$ is the emitter window perimeter and "))
            doc.append(NoEscape(r"$A_{\mathrm{E0}}$ is the emitter window area. "))
            doc.append(
                NoEscape(
                    r"The emitter window width (length) differs from the drawn emitter width (length) by $\Delta l_{\mathrm{E}}$ ($\Delta b_{\mathrm{E}}$) and has rounded corners, approximated as circles. "
                )
            )
            doc.append(
                NoEscape(
                    r"The bilinear scaling equation system is fitted globally for all measured device geometries in this extraction step."
                )
            )
            doc.append("\r")

        else:
            doc.append(
                NoEscape(
                    r"This extraction step performs the PoA separation of $"
                    + self.quantity.to_tex()
                    + r"$. "
                )
            )
            doc.append(NoEscape(r"For advanced HBT technologies, the classical PoA separation"))
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
            doc.append(NoEscape(r"$A_{\mathrm{E0}}$ is the emitter window area and "))
            doc.append(NoEscape(r"$P_{\mathrm{E0}}$ is the emitter window perimeter, "))
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
                    + self.quantity.to_tex(subscript="l", superscript="'")
                    + r"$ is the "
                    + self.quantity.get_descriptor()
                    + r" per emitter length, "
                )
            )
            doc.append(
                NoEscape(
                    r"$"
                    + self.quantity.to_tex(subscript="b", superscript="'")
                    + r"$ is the "
                    + self.quantity.get_descriptor()
                    + r" per emitter width, "
                )
            )
            doc.append(
                NoEscape(
                    r"$"
                    + self.quantity.to_tex(subscript="c", superscript="")
                    + r"$ is the "
                    + self.quantity.get_descriptor()
                    + r" corner component, "
                )
            )
            doc.append(NoEscape(r"$l_{\mathrm{E0}}^{}$ is the emitter window length, "))
            doc.append(NoEscape(r"$b_{\mathrm{E0}}^{}$ is the emitter window width, "))
            doc.append(NoEscape(r"$P_{\mathrm{E0}}$ is the emitter window perimeter and "))
            doc.append(NoEscape(r"$A_{\mathrm{E0}}$ is the emitter window area. "))
            doc.append(
                NoEscape(
                    r"The emitter window width (length) differs from the drawn emitter width (length) by $\Delta l_{\mathrm{E}}$ ($\Delta b_{\mathrm{E}}$). "
                )
            )
            doc.append(
                NoEscape(
                    r"The bilinear scaling equation system is fitted globally for all measured device geometries in this extraction step."
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

    def get_operating_points(self, df):
        try:
            col = self.voltage + sub_specifiers.FORCED
            df.ensure_specifier_column(col, reference_node=self.relevant_duts[0].reference_node)
        except KeyError:
            col = self.voltage
            df.ensure_specifier_column(col, reference_node=self.relevant_duts[0].reference_node)

        return df[col].to_numpy()

    def get_quantity(self, df, v_spot):
        """Extract the base current from a given dataframe at a given voltage v_spot.
        Errors should have been cought in ensure_input_correct.
        """
        col = df.get_col_name(self.quantity)
        quantity = df[str(col)].to_numpy()
        v = self.get_operating_points(df)
        index_v = find_nearest_index(v_spot, v)  # find the base current at the given voltage
        # if ib[index_v] < 0:
        #     return False #catch broken measurement
        # else:
        return quantity[index_v]

    # @model_method(indep_vars=('l_E0','b_E0'))
    def quantity_poa(
        self,
        l_E0=None,
        b_E0=None,
        dle=None,
        dbe=None,
        quantity_per_area=None,
        quantity_per_length=0,
        quantity_per_width=0,
        quantity_corner=0,
    ):
        """full bilinear scaling equation of a quantity

        Parameters
        ----------
        l_E0, b_E0 : float !==DRAWN TODO:RENAME!!!!!!!!!!!!!!!!!
        dlE, dbE : float
        quantity_per_area, quantity_per_width, quantity_per_length, quantity_corner : float

        Returns
        -------
        quantity_poa : np.ndarray
        """
        # return area * quantity_per_area  + perimeter * quantity_per_perimeter
        length = l_E0 + dle
        width = b_E0 + dbe
        area = length * width
        # return area * quantity_per_area  + length * 2*quantity_per_length + width * 2*quantity_per_width + quantity_corner
        return (
            area * quantity_per_area
            + length * 2 * quantity_per_length
            + width * 2 * quantity_per_width
            + 4 * quantity_per_length * quantity_per_width / quantity_per_area
        )

    def quantity_poa_recr(
        self,
        l_E0=None,
        b_E0=None,
        recr=None,
        dle=None,
        dbe=None,
        quantity_per_area=None,
        quantity_per_length=0,
        quantity_per_width=0,
        quantity_corner=0,
    ):
        """full bilinear scaling equation of a quantity with corner rounding

        Parameters
        ----------
        l_E0, b_E0 : float !==DRAWN TODO:RENAME!!!!!!!!!!!!!!!!!
        dlE, dbE : float
        quantity_per_area, quantity_per_width, quantity_per_length, quantity_corner : float
        recr : corner rounding radius

        Returns
        -------
        quantity_poa : np.ndarray
        """
        # return area * quantity_per_area  + perimeter * quantity_per_perimeter
        length = l_E0 + dle
        width = b_E0 + dbe
        area = length * width - (4 - np.pi) * recr * recr
        corner_part = quantity_per_area * (
            np.pi
            * (recr + quantity_per_width / quantity_per_area)
            * (recr + quantity_per_length / quantity_per_area)
            - np.pi * recr * recr
        )
        return (
            area * quantity_per_area
            + (length - 2 * recr) * 2 * quantity_per_length
            + (width - 2 * recr) * 2 * quantity_per_width
            + corner_part
        )

    # @classmethod
    # def get_gammas(cls):
    #     return ['gamma_l', 'gamma_b', 'gamma_c']

    # @classmethod
    # def get_custom_gammas(cls, quantity):
    #     """ This function gets the default gammas from the XPoA step and renames them uniquely
    #     """
    #     quantity_specifier = specifiers.SpecifierStr(quantity.specifier, *quantity.nodes)
    #     name_poa           = str(cls.__qualname__)
    #     quantity_str       = str(quantity_specifier)
    #     postfix            = '_' + quantity_str + '_' + name_poa
    #     gammas             = [gamma + postfix for gamma in cls.get_gammas()]
    #     return gammas

    @classmethod
    def get_effective_area(
        cls, lE0, bE0, dlE, dbE, gamma_l=None, gamma_b=None, gamma_c=None, **_kwargs
    ):
        # return (length + dlE) *(width+dbE) + gamma_l * (length + dlE) * 2 + gamma_b * (width + dbE) * 2 + gamma_c
        # TRADICA formulation
        lE0 = lE0 + dlE
        bE0 = bE0 + dbE
        AE0 = lE0 * bE0
        return AE0 * (1 + 2 * gamma_l * lE0 + 2 * gamma_b * bE0 + 4 * gamma_b * gamma_l)

    @classmethod
    def get_area(cls, lE0, bE0, dlE, dbE):
        # return (length + dlE) *(width+dbE) + gamma_l * (length + dlE) * 2 + gamma_b * (width + dbE) * 2 + gamma_c
        # TRADICA formulation
        lE0 = lE0 + dlE
        bE0 = bE0 + dbE
        AE0 = lE0 * bE0
        return AE0

    @classmethod
    def get_effective_perimeter(
        cls, lE0=None, bE0=None, dlE=None, dbE=None, gamma_l=None, gamma_b=None, gamma_c=None
    ):
        # returns an effective perimeter given a few gamas
        return gamma_l * 2 * (lE0 + dlE) + gamma_b * 2 * (bE0 + dbE) + gamma_c

    @classmethod
    def get_effective_area_tex(cls):
        return (
            r"A_{\mathrm{eff}}",
            r"A_{\mathrm{eff}} = A_{\mathrm{E0}} + \gamma_{\mathrm{l}} 2l_{\mathrm{E0}} + \gamma_{\mathrm{b}} 2b_{\mathrm{E0}} + \gamma_{\mathrm{c}}  ",
        )

    @classmethod
    def get_area_tex(cls):
        return r"A_{\mathrm{E0}}", r"A_{\mathrm{E0}} = l_{\mathrm{E0}} b_{\mathrm{E0}}"

    @classmethod
    def get_effective_perimeter_tex(cls):
        return (
            r"P_{\mathrm{eff}}",
            r"P_{\mathrm{eff}} = \gamma_{\mathrm{l}} 2l_{\mathrm{E0}} + \gamma_{\mathrm{b}} 2b_{\mathrm{E0}} + \gamma_{\mathrm{c}}  ",
        )
