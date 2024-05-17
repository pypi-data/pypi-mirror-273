"""
    Step to allow global fitting of multiple measurements ti simulation data.
    Step is based upon XVerify (see x_verify.py)

    Author: Pascal Kuthe        | PascalKuthe@pm.me
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


import copy
from typing import List, Type

import numpy as np

from DMT.core import (
    specifiers,
    sub_specifiers,
    SpecifierStr,
)
from DMT.extraction import (
    XStep,
    plot,
    find_nearest_index,
    print_to_documentation,
    XVerify,
    IYNormNone,
)
from DMT.extraction.iynorm import IYNorm, IYNormDefault, IYNormLogOneRange
from DMT.extraction.model import memoize

try:
    from DMT.external.pylatex import Tex
    from pylatex import NoEscape
except ImportError:
    pass


class MXVerify(XStep):
    child_steps: List[XVerify]
    fit_along: List[SpecifierStr]
    quantity_fit: List[SpecifierStr]
    iynorms: List[Type[IYNorm]]
    y_data_len: List[int]
    y_normalizers: List[IYNorm]

    """Step class inherits always from XStep.

    Parameters
    ----------
    name            : str
        Name of this specific xcjei object.
    mcard           : :class:`~DMT.core.mcard.MCard` or :class:`~DMT.core.mc_parameter.McParameterCollection`
        This MCard needs to hold all relevant parameters of the model and is used for simulations or model equation calculations.
    lib             : :class:`~DMT.core.dut_lib.DutLib`
        This library of devices needs to hold a relevant reference dut with data in one or more DataFrames.
    op_definition   : {key : float, tuple or list}
    """

    def __init__(
        self,
        name,
        mcard,
        lib,
        op_definition,
        DutCircuitClass,
        relevant_duts=None,
        model_deemb_method=None,
        verify_area_densities=False,
        **kwargs,
    ):
        # init the super class
        super().__init__(
            name,
            mcard,
            lib,
            op_definition,
            DutCircuitClass=DutCircuitClass,
            specifier_paras={
                "fit_along": [],
                "quantity_fit": [],
                "inner_sweep_voltage": specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED,
                "outer_sweep_voltage": specifiers.VOLTAGE + ["B", "C"] + sub_specifiers.FORCED,
            },
            **kwargs,
        )

        self.inner_sweep_voltage = self.specifier_paras["inner_sweep_voltage"]
        self.outer_sweep_voltage = self.specifier_paras["outer_sweep_voltage"]

        self.fit_along = self.specifier_paras["fit_along"]
        self.quantity_fit = self.specifier_paras["quantity_fit"]

        if len(self.fit_along) != len(self.quantity_fit):
            raise IOError(
                "DMT -> MXVerify: There must be an equal amount of quantities to fit and quantaties to fit along."
            )

        # Do not pass full list to children
        del kwargs["quantity_fit"]
        del kwargs["fit_along"]

        self.is_ac = False
        self.model_deemb_method = model_deemb_method
        self.verify_area_densities = verify_area_densities
        self.iynorm = IYNormNone

        # define a set of specifiers that we always wish to have next to inner_sweep_voltage, outer_sweep_voltage and quantity_fit (minimum requirement)
        self.dc_specifiers = []
        self.dc_specifiers.append(
            specifiers.VOLTAGE + ["B", "E"] + sub_specifiers.FORCED
        )  # i did not really find where we need them ?!? In the
        self.dc_specifiers.append(specifiers.VOLTAGE + ["B", "C"] + sub_specifiers.FORCED)
        self.dc_specifiers.append(specifiers.VOLTAGE + ["C", "E"] + sub_specifiers.FORCED)

        self.dc_specifiers.append(specifiers.VOLTAGE + "B")  # only for models :/
        self.dc_specifiers.append(specifiers.VOLTAGE + "E")
        self.dc_specifiers.append(specifiers.VOLTAGE + "C")

        self.dc_specifiers.append(specifiers.CURRENT + "C")
        self.dc_specifiers.append(specifiers.CURRENT + "B")
        self.required_specifiers = [
            self.inner_sweep_voltage,
            self.outer_sweep_voltage,
        ]
        self.ac_specifiers = []
        self.ac_specifiers.append(specifiers.FREQUENCY)
        self.ac_specifiers.append(specifiers.TRANSIT_FREQUENCY)
        self.ac_specifiers.append(specifiers.MAXIMUM_OSCILLATION_FREQUENCY)
        self.ac_specifiers.append(specifiers.MAXIMUM_STABLE_GAIN)
        self.ac_specifiers.append(specifiers.TRANSIT_TIME)
        self.ac_specifiers.append(specifiers.UNILATERAL_GAIN)
        self.ac_specifiers.append(specifiers.SS_PARA_Y + ["B", "B"])
        self.ac_specifiers.append(specifiers.SS_PARA_Y + ["C", "B"])
        self.ac_specifiers.append(specifiers.SS_PARA_Y + ["C", "B"] + sub_specifiers.REAL)
        self.ac_specifiers.append(specifiers.SS_PARA_Y + ["B", "C"])
        self.ac_specifiers.append(specifiers.SS_PARA_Y + ["C", "C"])

        self.iynorms = []
        self.child_steps = []

        for fit_along, quantity_fit in zip(self.fit_along, self.quantity_fit):
            if quantity_fit.specifier == specifiers.CURRENT.specifier:
                self.iynorms.append(IYNormLogOneRange)
            else:
                self.iynorms.append(IYNormDefault)

            if fit_along not in self.required_specifiers:
                self.required_specifiers.append(fit_along)
            if quantity_fit not in self.required_specifiers:
                self.required_specifiers.append(quantity_fit)

            self.child_steps.append(
                XVerify(
                    "{}_SUBFIT_{}".format(name, quantity_fit),
                    mcard,
                    lib,
                    op_definition,
                    DutCircuitClass,
                    quantity_fit=quantity_fit,
                    fit_along=fit_along,
                    **kwargs,
                )
            )

        if relevant_duts is not None:
            self.relevant_duts = relevant_duts
        else:
            self.relevant_duts = [lib.dut_ref]

    def add_to_xtraction(self, xtraction):
        """Sets the duts from xtraction to the given step

        Parameters
        ----------
        xtraction : :class:`~DMT.extraction.XTraction`]
        """
        for child in self.child_steps:
            xtraction.add_xstep(child)

        super().add_to_xtraction(xtraction)

    @plot()
    @print_to_documentation()
    def main_plot(self):
        """Overwrite main plot."""
        return super(MXVerify, self).main_plot(
            "composition",
            x_label="X (composition)",
            y_label="Y (composition)",
        )

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
            self.required_specifiers += self.dc_specifiers
            if self.is_ac:
                self.required_specifiers += self.ac_specifiers

        # unique them (can save some time later...) and sort so the same simulations are found again independent of the different fit_quantity
        self.required_specifiers = sorted(list(set(self.required_specifiers)))

        # now ensure the required specifiers
        super().ensure_input_correct()

    def ensure_input_correct_per_dataframe(self, dataframe, dut=None, key=None, **_kwargs):
        for specifier in self.required_specifiers:
            try:
                dataframe.ensure_specifier_column(specifier, ports=dut.nodes)
            except KeyError as err:
                raise IOError(
                    "The column "
                    + specifier
                    + "could not be calculated. Available columns: "
                    + str(dut.data[key].columns)
                ) from err

    def init_data_reference(self):
        """Find the required data in the user supplied dataframe or database and write them into data_model attribute of XStep object."""

        # sweeps and subfunction_length should be identical so we initialize the data reference with
        # the values of the first child step (first quantity) and just assert that the values are identical for other
        # x and y are just set to zero and copied from the child steps later
        self.data_reference = [
            {
                "x": np.zeros(len(self.child_steps) * len(line["x"])),
                "y": np.zeros(len(self.child_steps) * len(line["x"])),
                "y_no_norm": np.zeros(len(self.child_steps) * len(line["x"])),
                "sweep": copy.deepcopy(line["sweep"]),
                "subfunction_length": len(line["x"]),
                "width": line["width"],
                "length": line["length"],
                "config": line["config"],
            }
            for line in self.child_steps[0].data_reference
        ]

        self.labels = self.child_steps[0].labels

        # The normalizations are initiated and applied here as the entire step is normalized (not just the data_model during optimization)
        self.y_normalizers = []

        # - Append x and y values
        # - Check that other quantateis are identical
        # - Initialize y_normalizers with the full y data of each child
        for i, (child, norm) in enumerate(zip(self.child_steps, self.iynorms)):
            for line_index, (dst, src) in enumerate(zip(self.data_reference, child.data_reference)):
                length = dst["subfunction_length"]

                dst["y"][i * length : (i + 1) * length] = src["y"]
                dst["y_no_norm"][i * length : (i + 1) * length] = src["y"]
                dst["x"][i * length : (i + 1) * length] = src["x"]
                dst["index"] = line_index  # Required for get_bool_array

                assert dst["subfunction_length"] == len(src["y"])  # TODO variable size?

                # TODO properly check that sweeps are identical (they should be but I want the assertion)

                # if dst["sweep"].sweepdef != src["sweep"].sweepdef:
                #     raise IOError("Sweep missmatch (likely a bug):\n{}\n{}".format(src['sweep'].sweepdef ,dst['sweep'].sweepdef))
                #
                # if dst["sweep"].outputdef != src["sweep"].outputdef:
                #     raise IOError("Sweep missmatch (likely a bug):\n{}\n{}".format(src['sweep'].outputdef ,dst['sweep'].outputdef))
                #
                # if dst["sweep"].othervar != src["sweep"].othervar:
                #     raise IOError("Sweep missmatch (likely a bug):\n{}\n{}".format(src['sweep'].othervar ,dst['sweep'].othervar))

            self.y_normalizers.append(
                norm(np.concatenate([line["y"] for line in child.data_reference]))
            )

        # Normalize the y data
        for line in self.data_reference:
            length = line["subfunction_length"]
            for i, norm in enumerate(self.y_normalizers):
                line["y"][i * length : (i + 1) * length] = norm.normalize(
                    line["y"][i * length : (i + 1) * length]
                )

    # Do not sort (only required for bou
    def order_data_reference(self):
        pass

    def sort_line(self, line):
        return line

    def init_data(self):
        self.data_reference = []
        self.data_model = []
        self.labels = []  # ?!?

        self.init_data_reference()
        if not self.data_reference:
            raise DataReferenceEmpty("The data reference of the step " + self.name + " are empty.")

        self.inited_data = True

    def get_bool_array(self, line_ref, bounds=None):
        """Return a boolean array, where True means that the value in line_ref is inside the bounds.

        Parameters
        ----------
        line_ref : {}
            A dictionarray of a line that has at least the keys "x" and "y"
        bounds : DMT.extraction.XBounds, YBounds or XYBounds
            The boundaries that shall be used to determine which values in bool_array are true

        Returns : np.array()
            An array that has "True" where the value in "x" or "y", depending on the type of bounds, is inside the bounds.
        """

        bool_array = np.zeros_like(line_ref["x"], dtype=np.bool)
        subfunction_length = line_ref["subfunction_length"]

        for i, child in enumerate(self.child_steps):
            x = line_ref["x"][i * subfunction_length : (i + 1) * subfunction_length]
            y = line_ref["y_no_norm"][i * subfunction_length : (i + 1) * subfunction_length]
            res = child.get_bool_array({"x": x, "y": y}, child.x_bounds[line_ref["index"]])

            bool_array[i * subfunction_length : (i + 1) * subfunction_length] = res

        print(line_ref["x"])
        print(bool_array)
        print(line_ref["x"][bool_array])

        return bool_array

    def fit(self, line, paras_model, dut=None):
        """
        Implementation is similar to the one in XVerify
        However in this implementation the data for each quantity is concatenated to form the full data
        Furthermore the data is normalized for each quantity individually and the bounds of each subset are applied to the line
        """

        # Read simulation results
        try:
            sweep = line["sweep"]
            key = dut.join_key(dut.get_sweep_key(sweep), "iv")
            data = dut.data[key]
        except KeyError:
            raise IOError(
                "DMT -> XVerify -> " + self.name + ": probably the simulation went wrong."
            )

        # single frequency ? TODO WHY IS THIS NECESSATY
        if specifiers.FREQUENCY in self.op_definition.keys():
            if isinstance(self.op_definition[specifiers.FREQUENCY], (float, int)):
                data = data[
                    np.isclose(data[specifiers.FREQUENCY], self.op_definition[specifiers.FREQUENCY])
                ]

        # read internal HICUM data from simulation results, not always possible..
        try:
            line[specifiers.TEMPERATURE] = data["TK"].to_numpy()
            line[specifiers.TRANSIT_TIME] = data["TF"].to_numpy()
            line["I_CK"] = data["ick"].to_numpy()
            line["V_ciei"] = data["Vciei"].to_numpy()
        except KeyError:
            pass

        # Calculate missing data
        for specifier in self.required_specifiers:
            data.ensure_specifier_column(specifier, ports=dut.nodes)

        subfunction_length = line["subfunction_length"]

        # Initalize with zeros
        line["x"] = np.zeros_like(self.data_reference[line["index"]]["x"])
        line["y"] = np.zeros_like(self.data_reference[line["index"]]["y"])
        line["y_no_norm"] = np.zeros_like(self.data_reference[line["index"]]["y"])

        for i, (quantity_fit, fit_along, norm) in enumerate(
            zip(self.quantity_fit, self.fit_along, self.y_normalizers)
        ):
            # find correct data for quantities where the inner sweep voltage produces unique lines
            if not fit_along.specifier in ["V", "I"]:
                # unique inner voltage
                data[self.inner_sweep_voltage] = data[self.inner_sweep_voltage].round(3)  # cheat
                inner_unique = data[self.inner_sweep_voltage].unique()
                for v_inner in inner_unique:
                    # get correct line :/
                    if v_inner != line[self.inner_sweep_voltage][0]:
                        continue
                    # Assumption: Only done once!
                    data = data[data[self.inner_sweep_voltage] == v_inner]

            # Write data range into line
            x = np.real(data[fit_along].to_numpy())
            y = np.real(data[quantity_fit].to_numpy())

            line["x"][i * subfunction_length : (i + 1) * subfunction_length] = x
            line["y_no_norm"][i * subfunction_length : (i + 1) * subfunction_length] = y
            line["y"][i * subfunction_length : (i + 1) * subfunction_length] = norm.normalize(
                y
            )  # normalize y data

            for specifier in self.required_specifiers:
                line[specifier] = data[specifier].to_numpy()

        # avoid zero
        line["x"] = np.where(line["x"] == 0, 1e-30, line["x"])
        line["y"] = np.where(line["y"] == 0, 1e-30, line["y"])

        return line

    @memoize  # here we memoize calc all, since this is slow with a circuit simulator
    def calc_all(self, *args, **kwargs):
        return super().calc_all(*args, **kwargs)

    def get_tex(self):
        return r"\text{Global optimization of multiple quantities}"

    def set_initial_guess(self, data_reference):
        # Global optimization should only be performed when reasoable values for all parameters are known
        pass

    def get_description(self):
        res = ""
        for quantity_to_fit, fit_along in zip(self.quantity_fit, self.fit_along):
            res += r" ${}\left({}\right)$".format(quantity_to_fit.to_tex(), fit_along.to_tex())

        doc = Tex()
        doc.append(
            NoEscape(
                r"This extraction step compares"
                + res
                + r" at different $"
                + self.outer_sweep_voltage.to_tex()
                + r"$ from measurements vs. full circuit simulations."
            )
        )
        return doc

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
            reference_node=self.relevant_duts[0].reference_node,
            # list_opy      = [self.mcard.va_file],# very slow!
        )
        dut.sim_dir = self.circuit_sim_dir
        return dut
