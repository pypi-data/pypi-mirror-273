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
import copy

try:
    from semver.version import Version as VersionInfo
except ImportError:
    from semver import VersionInfo
from DMT.core.mc_parameter import McParameter
from DMT.core.mcard import MCard
from DMT.core.dut_view import DutView
from DMT.core.constants import P_CELSIUS0
from DMT.psp.psp_default_circuits import get_circuit

SEMVER_MCPSP_CURRENT = VersionInfo(major=1, minor=0)

default_possible_groups = {
    "JUN_SIM": "Circuit simulator specific parameters for JUNCAP2",
    "JUN_SB_CAP": "Capacitance Parameters for the source-bulk junction",
    "JUN_SB_CUR": "Ideal-current Parameters for the source-bulk junction",
    "JUN_SB_SRH": "Shockley-Read-Hall Parameters for the source-bulk junction",
    "JUN_SB_TAT": "Trap-assisted Tunneling Parameters for the source-bulk junction",
    "JUN_SB_BBT": "Band-to-band Tunneling Parameters for the source-bulk junction",
    "JUN_SB_AVAL": "Avalanche and Breakdown Parameters for the source-bulk junction",
    "JUN_SB_EXP": "Express Parameters for the source-bulk junction",
    "JUN_DB_CAP": "Capacitance Parameters for the drain-bulk junction",
    "JUN_DB_CUR": "Ideal-current Parameters for the drain-bulk junction",
    "JUN_DB_SRH": "Shockley-Read-Hall Parameters for the drain-bulk junction",
    "JUN_DB_TAT": "Trap-assisted Tunneling Parameters for the drain-bulk junction",
    "JUN_DB_BBT": "Band-to-band Tunneling Parameters for the drain-bulk junction",
    "JUN_DB_AVAL": "Avalanche and Breakdown Parameters for the drain-bulk junction",
    "JUN_DB_EXP": "Express Parameters for the drain-bulk junction",
    "INST_GB": "Instance parameters for global and binning model",
    "INST_L": "Instance parameters for local model",
    "INST_LGB": "Instance parameters for local, global and binning model",
    "SIM_LGB": "Circuit simulator specific parameters",
    "SWITCH_LGB": "Switch parameters",
    "process_L": "Process parameters for local model",
    "interface_L": "Interface states parameters for local model",
    "DIBL_L": "DIBL parameters for local model",
    "STS-SCT_L": "Subthreshold slope parameters of short channel transistor for local model",
    "mobility_L": "Mobility parameters for local model",
    "R_intrinsic_L": "Intrinsic series-resistance parameters for local model",
    "vel_sat_L": "Velocity saturation parameters for local model",
    "vol_sat_L": "Saturation voltage parameters for local model",
    "L_cm_L": "Channel length modulation parameters for local model",
    "impact_ion_L": "Impact ionization parameters for local model",
    "IG_L": "Gate current parameters for local model",
    "GIDL_L": "Gate induced drain/source leakage parameters for local model",
    "charge_L": "Charge model parameters for local model",
    "noise_L": "Noise parameters for local model",
    "edge_L": "Edge transistor parameters for local model",
    "R_par_L": "Parasitic resistance parameters for local model",
    "nqs_L": "NQS parameters for local model",
    "SH_L": "Self-heating Parameters for local model",
    "process_G": "Process parameters for global model",
    "interface_G": "Interface states parameters for global model",
    "DIBL_G": "DIBL parameters for global model",
    "STS-SCT_G": "Subthreshold slope parameters of short channel transistor for global model",
    "mobility_G": "Mobility parameters for global model",
    "R_intrinsic_G": "Intrinsic series-resistance parameters for global model",
    "vel_sat_G": "Velocity saturation parameters for global model",
    "vol_sat_G": "Saturation voltage parameters for global model",
    "L_cm_G": "Channel length modulation parameters for global model",
    "impact_ion_G": "Impact ionization parameters for global model",
    "IG_G": "Gate current parameters for global model",
    "GIDL_G": "Gate induced drain/source leakage parameters for global model",
    "charge_G": "Charge model parameters for global model",
    "noise_G": "Noise parameters for global model",
    "edge_G": "Edge transistor parameters for global model",
    "well_prox_G": "Well proximity effect parameters for global model",
    "process_B": "Process parameters for binning model",
    "interface_B": "Interface states parameters for binning model",
    "DIBL_B": "DIBL parameters for binning model",
    "STS-SCT_B": "Subthreshold slope parameters of short channel transistor for binning model",
    "mobility_B": "Mobility parameters for binning model",
    "R_intrinsic_B": "Intrinsic series-resistance parameters for binning model",
    "vel_sat_B": "Velocity saturation parameters for binning model",
    "vol_sat_B": "Saturation voltage parameters for binning model",
    "L_cm_B": "Channel length modulation parameters for binning model",
    "impact_ion_B": "Impact ionization parameters for binning model",
    "IG_B": "Gate current parameters for binning model",
    "GIDL_B": "Gate induced drain/source leakage parameters for binning model",
    "charge_B": "Charge model parameters for binning model",
    "noise_B": "Noise parameters for binning model",
    "edge_B": "Edge transistor parameters for binning model",
    "well_prox_B": "Well proximity effect parameters for binning model",
    "LABEL_B": "Parameters for binning-set labeling",
    "R_par_GB": "Parasitic resistance parameters for global and binning model",
    "stress_GB": "Stress model parameters for global and  binning model",
    "well_prox_GB": "Well proximity effect parameters for global and binning model",
    "SH_GB": "Self-heating Parameters for global and binning model",
    "nqs_GB": "NQS parameters for global and binning model",
}


class McPsp(MCard):
    """Holds all model parameters of the PSP model.


    Parameters
    ----------
    va_file : str, optional
        Path to a PSP Verilog-AMS file
    load_model_from_path : str, optional
        Initialise the modelcard with the parameter from the given file path.
    version : float, optional
        Version of the model card.

    """

    def __init__(
        self,
        load_model_from_path=None,
        version=1.0,
        default_circuit="common_source",
        __McPsp__=SEMVER_MCPSP_CURRENT,
        parameter_entry_level="full",
        **kwargs,
    ):
        if "nodes_list" in kwargs:
            nodes_list = kwargs.pop("nodes_list")
        else:
            # given in the va code
            nodes_list = ("d", "g", "s", "b", "dt")

        if "default_subckt_name" in kwargs:
            default_subckt_name = kwargs.pop("default_subckt_name")
        else:
            default_subckt_name = "Q_PSP"

        if "default_module_name" in kwargs:  # given in the va code
            default_module_name = kwargs.pop("default_module_name")
        else:
            default_module_name = "PSP103VA"

        if "possible_groups" not in kwargs:
            kwargs["possible_groups"] = default_possible_groups

        super().__init__(
            nodes_list,
            default_subckt_name,
            default_module_name,
            version,
            **kwargs,
        )
        if not isinstance(__McPsp__, VersionInfo):
            try:
                __McPsp__ = VersionInfo.parse(__McPsp__)
            except TypeError:
                __McPsp__ = VersionInfo.parse(f"{__McPsp__:1.1f}.0")

        if __McPsp__ != SEMVER_MCPSP_CURRENT:
            raise IOError("DMT->McPsp: The given version of __McPsp__ is unknown!")

        self.__McPsp__ = __McPsp__
        self.default_circuit = default_circuit
        self.parameter_entry_level = parameter_entry_level

        if parameter_entry_level == "local":
            self.remove(self._get_list_non_local_parameters())
        elif parameter_entry_level == "global":
            self.remove(self._get_list_non_global_parameters())
        elif parameter_entry_level == "binning":
            self.remove(self._get_list_non_binning_parameters())
        elif parameter_entry_level == "instance":
            self.remove(self._get_list_non_instance_parameters())

        if self._va_codes is None:
            raise IOError(
                "The PSP model parameters are not implemented in DMT-FET. You must supply a valid Verilog-A file!"
            )

        if load_model_from_path is not None:
            super().load_model_parameters(load_model_from_path, force=False)
            try:
                type_McPara = super().get("type")
                # set the parameter _type with obtained value
                try:
                    self.set_values({"_type": type_McPara.value}, force=False)
                except KeyError:
                    self.add(McParameter("_type", value=type_McPara.value, unit=None, group="M_P"))
            except KeyError:
                # 'type' parameter is missing in the loaded model card, add 'type' with default value for VA simulation
                self.add(McParameter("type", value=1, unit=None, group="M_P"))

    def info_json(self, **kwargs):
        """Returns a dict with serializeable content for the json file to create. Add the info about the concrete subclass to create here!"""
        info_dict = super().info_json(**kwargs)
        if hasattr(self, "__McPsp__"):
            info_dict["__McPsp__"] = str(self.__McPsp__)
        else:
            info_dict["__McPsp__"] = str(SEMVER_MCPSP_CURRENT)
        info_dict["default_circuit"] = self.default_circuit
        info_dict["parameter_entry_level"] = self.parameter_entry_level
        return info_dict

    def get_circuit(self):
        """The psp model has some default circuits."""
        return get_circuit(self.default_circuit, self)

    def _get_list_non_local_parameters(self):
        non_locals = []
        for para in self:
            if para.group.startswith("JUN"):
                continue
            if "L" in para.group.split("_")[-1]:
                continue
            non_locals.append(para.name)

        return non_locals

    def _get_list_non_global_parameters(self):
        non_globals = []
        for para in self:
            if para.group.startswith("JUN"):
                continue
            if "G" in para.group.split("_")[-1]:
                continue
            non_globals.append(para.name)

        return non_globals

    def _get_list_non_binning_parameters(self):
        non_binning = []
        for para in self:
            if para.group.startswith("JUN"):
                continue
            if "B" in para.group.split("_")[-1]:
                continue
            non_binning.append(para.name)

        return non_binning

    def _get_list_non_instance_parameters(self):
        non_instance = []
        for para in self:
            if para.group.startswith("INST"):
                continue
            non_instance.append(para.name)

        return non_instance

    def get_local_modelcard(
        self, dut: DutView = None, calculate: bool = False, verbose: bool = False
    ):
        """Returns a modelcard with only the parameters valid for the local model.

        Parameters
        ----------
        calculate : bool
            If False, no value is changed except SWGEO is set to 0!
            If True, The values are tried to calculate using the Verilog-A equations. This is sensitive to the code and must have the retrieve flag at all necessary equations.
        verbose: bool
            If True, all missing functions will be reported.
        """
        mc_local = copy.deepcopy(self)
        if calculate:
            mc_local = dut.technology.scale_modelcard(
                mcard=mc_local,
                lE0=dut.length,
                bE0=dut.width,
                nfinger=dut.nfinger,
                config=dut.contact_config,
            )

        if calculate:
            model = mc_local.get_verilogae_model()

            kwargs = self.to_kwargs()
            kwargs = {k.upper(): v for k, v in kwargs.items()}
            to_set = {}

            mc_local.remove(self._get_list_non_local_parameters())
            for para in mc_local:
                try:
                    name_func = next(
                        func for func in model.functions if para.name.upper() + "_i" == func
                    )
                    to_set[para.name] = model.functions[name_func].eval(
                        temperature=kwargs["TR"]
                        + P_CELSIUS0,  # temperature = reference, so no scaling
                        voltages={},  # should NOT need any voltages
                        **kwargs,
                    )
                except StopIteration:
                    if verbose:
                        print(f"No scaling calculation for {para.name} found!")

            mc_local.set_values(to_set)
        else:
            mc_local.remove(self._get_list_non_local_parameters())

        mc_local.set_values({"swgeo": 0}, force=True)
        mc_local.parameter_entry_level = "local"

        return mc_local

    def get_global_modelcard(self):
        """Retruns a modelcard with only the parameters valid for the global model. No value is changed except SWGEO is set to 1!"""
        mc_global = copy.deepcopy(self)
        mc_global.remove(self._get_list_non_global_parameters())
        mc_global.set_values({"swgeo": 1}, force=True)
        mc_global.parameter_entry_level = "global"

        return mc_global

    def get_binning_modelcard(self):
        """Retruns a modelcard with only the parameters valid for the binning model. No value is changed except SWGEO is set to 2!"""
        mc_binning = copy.deepcopy(self)
        mc_binning.remove(self._get_list_non_binning_parameters())
        mc_binning.set_values({"swgeo": 2}, force=True)
        mc_binning.parameter_entry_level = "binning"

        return mc_binning

    def get_instance_modelcard(self):
        """Retruns a modelcard with only the parameters valid for the binning model. No value is changed except SWGEO is set to 2!"""
        mc_binning = copy.deepcopy(self)
        mc_binning.remove(self._get_list_non_instance_parameters())
        mc_binning.set_values({"swgeo": 0}, force=True)
        mc_binning.parameter_entry_level = "instance"

        return mc_binning
