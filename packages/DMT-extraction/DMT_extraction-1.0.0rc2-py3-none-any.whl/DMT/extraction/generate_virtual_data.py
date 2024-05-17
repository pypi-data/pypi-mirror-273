""" Functions to generate virtual measurement data.
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
from DMT.core import SimCon, Sweep, specifiers, DutType
from DMT.core.sweep_def import (
    SweepDefLinear,
    SweepDefList,
    SweepDefLog,
    SweepDefSync,
    SweepDefConst,
)


def generate_virtual_data(
    dut, sweeps, force=True, t_max=10000, n_core=4, rename=True, remove_simulations=True
):
    """Simulates a DuT for the specified sweeps and generates new keys in the DuT that represent the
    corresponding simulated data in its database.

    Parameters
    ----------
    dut : :class:`~:class:`~DMT.core.dut_view.DutView``
        DuT for which the simulated data shall be generated.
    sweeps : [:class:`~DMT.core.sweep.Sweep`]
        List of sweeps that shall be simulated. The sweeps must have a meaningful unique names as DMT's hashing function is
        not used here.
    rename : True, Bool
        If True, the sweep hases are removed from the keys in the database, which corresponds to typical measurements
        taken in a lab.

    Returns
    -------
    run_sims : boolean
        True, if any simulation was started. False if all simulations were read from hard disk.
    """
    if not isinstance(sweeps, list):
        sweeps = [sweeps]

    if rename:
        # check if renamed data is in dut.data
        sweeps_to_sim = []
        keys_dut = list(dut.data.keys())

        for sweep in sweeps:
            # get simulation data and delete from dut
            key_meas = dut.join_key(sweep.get_temperature(), sweep.name)
            if key_meas not in keys_dut:
                sweeps_to_sim.append(sweep)

        sweeps = sweeps_to_sim

    # create a simulation controller and simulate
    sim_con = SimCon(t_max=t_max, n_core=n_core)
    sim_con.append_simulation(dut=dut, sweep=sweeps)
    _all_sim_success, run_sims = sim_con.run_and_read(
        force=force, parallel_read=False, remove_simulations=remove_simulations
    )

    # remove the hashes from the sweep keys
    if rename:
        keys_dut = list(dut.data.keys())
        for sweep in sweeps:
            # get simulation data and delete from dut
            key_sweep = dut.get_sweep_key(sweep)
            key_meas = dut.join_key(sweep.get_temperature(), sweep.name)
            for key in keys_dut:
                if key_sweep in key:
                    data = dut.data[key]
                    dut.remove_data(key)
                    dut.add_data(data, key=key_meas, force=True)

    return run_sims


def get_output_def(qs_analysis=False, additional_outputs=None):
    """Generalized :class:`~DMT.core.sweep.Sweep` outputdef creation for the DEVICE TCAD simulator.
    TODO: Maybe add to DMT.Device instead of here.

    Parameters
    ----------
    qs_analysis : bool, False
        If True, add the required outputs for quasi-static simulation.
    additional_output : [], None
        If not None, add this list of additional outputs to the outputdef.
    """
    output_def = [specifiers.CURRENT + "B", specifiers.CURRENT + "C", specifiers.CURRENT + "E"]
    if qs_analysis:
        output_def += [
            "QU",
            "Q_Y11E",
            "Q_Y12E",
            "Q_Y21E",
            "Q_Y22E",
        ]
    if additional_outputs is not None:
        output_def += additional_outputs
    return output_def


def get_sweep_fgummel(vbe=None, vbc=None, freq=None, temperature=300, name="fgummel_vbc", **kwargs):
    """Generate a forward Gummel sweep for bipolar devices.

    Parameters
    ----------
    vbe : np.ndarray, optional
        List of vbe values to be simulated. Defaults to a linear sweep from 0 to 1.2 V in 0.01 Volt steps.
    vbc : np.ndarray, optional
        The single value or list of vbc values for which the vbe sweep is simulated.
        Defaults to a list with [-3.0, -2.5, -2.0, -1.5, -1.0, -0.7, -0.5, -0.2, 0, 0.2, 0.5, 0.7].
    temperature : float, 300, optional
        The temperature at which the simulations shall be undertaken.
    name : str, "fgummel_vbc", optional
        Should be a unique and useful name for the generated sweep.

    Returns
    -------
    swp : :class:`~DMT.core.sweep.Sweep`
        A DMT Sweep object that can be simulated with TCAD and circuit simulators.
    """
    if vbe is None:
        vbe = np.linspace(0.0, 1.2, num=121)
    if vbc is None:
        vbc = np.array([-3.0, -2.5, -2.0, -1.5, -1.0, -0.7, -0.5, -0.2, 0, 0.2, 0.5, 0.7])

    swp = _get_sweep(
        v10=vbe, v12=vbc, ac=False, temp=temperature, dut_type=DutType.bjt, mode="list"
    )
    swp.outputdef = get_output_def(**kwargs)
    swp.name = name
    return swp


def get_sweep_ac_vbc(vbe=None, vbc=None, freq=None, temperature=300, name="freq_vbc", **kwargs):
    """Generate a forward Gummel sweep with inner Vbe sweep outer Vbc sweep and
    additional small-signal AC analysis at a specific frequency for bipolar devices.

    Parameters
    ----------
    vbe : np.ndarray, optional
        List of vbe values to be simulated. Defaults to a linear sweep from 0.0 to 1.2 V in 0.01 Volt steps.
    vbc : np.ndarray, optional
        The single value or list of vbc values for which the vbe sweep is simulated.
        Defaults to a list with [-3.0, -2.5, -2.0, -1.5, -1.0, -0.7, -0.5, -0.2, 0, 0.2, 0.5, 0.7].
    freq : float
        The frequency in Hertz at which the AC analysis shall be conducted.
    temperature : float, 300, optional
        The temperature at which the simulations shall be undertaken.
    name : str, "freq_vbc", optional
        Should be a unique and useful name for the generated sweep.

    Returns
    -------
    swp : :class:`~DMT.core.sweep.Sweep`
        A DMT Sweep object that can be simulated with TCAD and circuit simulators.
    """
    if vbe is None:
        vbe = np.linspace(0.0, 1.2, num=121)
    if vbc is None:
        vbc = np.array([-3.0, -2.5, -2.0, -1.5, -1.0, -0.7, -0.5, -0.2, 0, 0.2, 0.5, 0.7])
    if freq is None:
        freq = 1e3

    swp = _get_sweep(
        v10=vbe, v12=vbc, ac=True, freq=freq, temp=temperature, dut_type=DutType.bjt, mode="list"
    )
    swp.outputdef = get_output_def(**kwargs)
    swp.name = name
    return swp


def get_sweep_foutput_vb(
    vbe=None, vce=None, temperature=300, name="foutput_vb", freq=None, **kwargs
):
    """Get a forced base voltage forward output sweep.

    Parameters
    ----------
    vce : np.ndarray, optional
        List of vbe values for which the vce sweep shall be simulated.
        Defaults to a linear sweep from 0.0 to 3.0 V in 0.05 Volt steps.
    vbe : np.ndarray, optional
        The single value or list of vbe values for which the vce sweep is simulated.
        Defaults to a list from -1 to 1.2V in 0.01V.
    temperature : float,300, optional
        The temperature at which the simulations shall be undertaken.
    name : str, "foutput_vb", optional
        Should be a unique and useful name for the generated sweep.

    Returns
    -------
    swp : :class:`~DMT.core.sweep.Sweep`
        A DMT Sweep object that can be simulated with TCAD and circuit simulators.
    """
    if vbe is None:
        vbe = np.linspace(-1.0, 1.2, num=221)
    if vce is None:
        vce = np.linspace(0.0, 3.0, num=16)

    swp = _get_sweep(
        v10=vbe, v20=vce, ac=True, freq=freq, temp=temperature, dut_type=DutType.bjt, mode="list"
    )
    swp.outputdef = get_output_def(**kwargs)
    swp.name = name
    return swp


def get_sweep_ac_vb(vbe=None, vce=None, freq=None, temperature=300, name="freq_vb_", **kwargs):
    """Generate a forward Gummel sweep with inner Vbe sweep outer Vce sweep and
    additional small-signal AC analysis at a specific frequency for bipolar devices.

    Parameters
    ----------
    vbe : np.ndarray, optional
        List of vbe values to be simulated. Defaults to a linear sweep from 0.0 to 1.2 V in 0.1 Volt steps.
    vce : np.ndarray, optional
        The single value or list of vce values for which the vbe sweep is simulated.
        Defaults to a list from 0.0V to 3.0V in 16 equally spaced steps.
    freq : float
        The frequency in Hertz at which the AC analysis shall be conducted.
    temperature : float, 300, optional
        The temperature at which the simulations shall be undertaken.
    name : str, \"freq\_vb\_\", optional
        Should be a unique and useful name for the generated sweep.

    Returns
    -------
    swp : :class:`~DMT.core.sweep.Sweep`
        A DMT Sweep object that can be simulated with TCAD and circuit simulators.
    """
    if vbe is None:
        vbe = np.linspace(-1.0, 1.2, num=221)
    if vce is None:
        vce = np.linspace(0.0, 3.0, num=16)

    swp = _get_sweep(
        v10=vbe, v20=vce, ac=True, freq=freq, temp=temperature, dut_type=DutType.bjt, mode="list"
    )
    swp.outputdef = get_output_def(**kwargs)
    swp.name = name
    return swp


def get_sweep_ac_vc(vbe=None, vce=None, freq=None, temperature=300, name="freq_vc", **kwargs):
    """Generate an output  sweep with inner Vce sweep outer Vbe sweep and
    additional small-signal AC analysis at a specific frequency for bipolar devices.

    Parameters
    ----------
    vbe : np.ndarray, optional
        List of vbe values to be simulated. Defaults to a linear sweep from 0.0 to 1.2 V in 0.1 Volt steps.
    vce : np.ndarray, optional
        The single value or list of vce values for which the vbe sweep is simulated.
        Defaults to a list from -2.0V to 3.0V in 501 equally spaced steps.
    freq : float
        The frequency in Hertz at which the AC analysis shall be conducted.
    temperature : float, 300, optional
        The temperature at which the simulations shall be undertaken.
    name : str, "freq_vc", optional
        Should be a unique and useful name for the generated sweep.

    Returns
    -------
    swp : :class:`~DMT.core.sweep.Sweep`
        A DMT Sweep object that can be simulated with TCAD and circuit simulators.
    """
    if vbe is None:
        vbe = np.linspace(0.0, 1.2, num=13)
    if vce is None:
        vce = np.linspace(-2.0, 3.0, num=501)

    swp = _get_sweep(
        v10=vbe, v20=vce, ac=True, freq=freq, temp=temperature, dut_type=DutType.bjt, mode="list"
    )
    swp.outputdef = get_output_def(**kwargs)
    swp.name = name
    return swp


def get_sweep_foutput_ib(ib=None, vce=None, temperature=300, name="foutput_ib", **kwargs):
    """Generate a forced Ib sweep with inner Vce sweep and inner Ib sweep.

    Parameters
    ----------
    ib : np.ndarray, optional
        List of ib values to be simulated. Defaults to a linear sweep from 2 to 20 uA in 10 equally spaced steps.
    vce : np.ndarray, optional
        The single value or list of vce values for which the vbe sweep is simulated.
        Defaults to a list from 0.0V to 2.0V in 101 equally spaced steps.
    temperature : float, 300, optional
        The temperature at which the simulations shall be undertaken.
    name : str, "foutput_ib", optional
        Should be a unique and useful name for the generated sweep.

    Returns
    -------
    swp : :class:`~DMT.core.sweep.Sweep`
        A DMT Sweep object that can be simulated with TCAD and circuit simulators.
    """
    if ib is None:
        ib = np.linspace(2e-6, 20e-6, num=10)
    if vce is None:
        vce = np.linspace(0.0, 2.0, num=101)

    swp = _get_sweep(i1=ib, v20=vce, ac=False, temp=temperature, dut_type=DutType.bjt, mode="list")
    swp.outputdef = get_output_def(**kwargs)
    swp.name = name
    return swp


def get_sweep_bjt(
    name=None,
    vbe=None,
    vbc=None,
    vce=None,
    vse=0,
    ib=None,
    ie=None,
    ac=True,
    temp=300,
    freq=1e3,
    mode="lin",
):
    """Wrapper for the method get_sweep, suitable for BJT type devices. See the documentation of the get_sweep method for
    details.
    """
    return _get_sweep(
        name=name,
        v10=vbe,
        v12=vbc,
        v20=vce,
        v30=vse,
        i1=ib,
        i0=ie,
        ac=ac,
        temp=temp,
        freq=freq,
        dut_type=DutType.bjt,
        mode=mode,
    )


def get_sweep_mos(
    name=None,
    vgs=None,
    vgd=None,
    vds=None,
    vbs=0,
    ig=None,
    isource=None,
    ac=True,
    temp=300,
    freq=1e3,
    mode="lin",
):
    """Wrapper for the method get_sweep suitable for MOS type devices. See the documentation of the get_sweep method for
    details.
    """
    return _get_sweep(
        name=name,
        v10=vgs,
        v12=vgd,
        v20=vds,
        v30=vbs,
        i1=ig,
        i0=isource,
        ac=ac,
        temp=temp,
        freq=freq,
        mode=mode,
        dut_type=DutType.mos,
    )


def _get_sweep(
    name=None,
    v10=None,
    v12=None,
    v20=None,
    v30=0,
    i1=None,
    i0=None,
    ac=True,
    temp=300,
    freq=1e3,
    dut_type=None,
    mode="lin",
):
    """Return a a DMT.Sweep Definition suitable for three port device simulation.
    The contacts of a three port device considered by this routine are named port_1, port_2, port_3 and ground(0).
    Note that only TWO of the port voltages v10, v12, v20 and/or port currents i1, i0 and i2 (not yet implemented)
    can be defined, since two voltages or one voltage and one current unambiguously define all bias
    that can be forced for a two port.

    The voltage v30 is special and defaults to zero (Emitter-Substrate short or Bulk-Source) short.
    If v30 is specified, it is added as the outermost voltage sweep.
    The voltage v30 is always interpreted as a list and never as a linear sweep.

    Parameters
    ----------
    v10, v12, v20, v30, i1, i0 : float64, np.array(), list, None
        The sweep definition for the current or voltage at or between the respective port pin(s) 1, 2 and 0:
        (1) A constant value indicates a CONSTANT voltage/current.
        (2) A List and keyword "mode"="lin": Indicates a linear sweep for the voltage/current from the value of the
        [0]th array element to [1]th array element in [2]th array value equally spaced steps.
        (3) List and keyword "mode"="list": Value is swept according to the values specified in the list
        If the keyword mode =="lin", only one contact voltage or current can be swept!
    ac   : bool, optional, default=True
        If True: return a sweep that contains an AC simulation definition for the specified frequency "freq".
    temp : float,[float], optional, default=300
        Temperature of the simulation in Kelvin. If a list of floats is given, the temperature is swept as the outermost sweep.
    freq : float64,[float], 1e3
        The frequency for AC simulations at every DC operating point in Hertz.
        If single value: Simulation only at this frequency.
        If three element list: Log sweep from 10^freq[0] to 10^freq[1] in freq[2] logarithmically spaced steps.
    dut_type : :class:`~DMT.core.dut_type.DutTypeInt` or :class:`~DMT.core.dut_type.DutTypeFlag`
        Indicates if the sweep is targeted at a MOSFET or BJT type device.
    mode : str, "lin" or "list"
        Parameter that controls how the primary sweep variable shall be interpreted.

    returns
    -------
    sweep : :class:`~DMT.core.sweep.Sweep`
        DMT sweep definition
    """
    if dut_type is None:
        raise IOError("The kwarg dut_type must be specified explicitly.")

    if not mode in ["list", "lin"]:
        raise IOError("The kwarg 'mode' must be set to either 'lin' or 'list'.")

    if v10 is not None and v12 is not None and v20 is not None:
        raise IOError(
            "You specified three voltages, but two voltages already define all potentials at the two-port device contacts. Replace on of the voltages with None."
        )

    # cast all inputs to lists
    if v10 is not None:
        try:
            _a = len(v10)
            v10 = np.asarray(v10)
        except TypeError:
            v10 = np.array([v10])
    else:
        v10 = np.array([])

    if v12 is not None:
        try:
            _a = len(v12)
            v12 = np.asarray(v12)
        except TypeError:
            v12 = np.array([v12])
    else:
        v12 = np.array([])

    if v20 is not None:
        try:
            _a = len(v20)
            v20 = np.asarray(v20)
        except TypeError:
            v20 = np.array([v20])
    else:
        v20 = np.array([])

    if v30 is not None:
        try:
            _a = len(v30)
            v30 = np.asarray(v30)
        except TypeError:
            v30 = np.array([v30])
    else:
        v30 = np.array([])

    if i1 is not None:
        try:
            _a = len(i1)
            i1 = np.asarray(i1)
        except TypeError:
            i1 = np.array([i1])
    else:
        i1 = np.array([])

    if i0 is not None:
        try:
            _a = len(i0)
            i0 = np.asarray(i0)
        except TypeError:
            i0 = np.array([i0])
    else:
        i0 = np.array([])

    # interpret lists according to kwargs "mode"
    if mode == "lin":
        if len(v10) > 1:
            v10 = np.linspace(v10[0], v10[1], int(v10[2]))
        if len(v12) > 1:
            v12 = np.linspace(v12[0], v12[1], int(v12[2]))
        if len(v20) > 1:
            v20 = np.linspace(v20[0], v20[1], int(v20[2]))
        # if len(v30) > 1: #v30 is always interpreted as LIST
        #     v30 = np.linspace(v30[0], v30[1], int(v30[2]))
        if len(i0) > 1:
            i0 = np.linspace(i0[0], i0[1], int(i0[2]))
        if len(i1) > 1:
            i1 = np.linspace(i1[0], i1[1], int(i1[2]))
    elif mode == "list":
        pass

    if dut_type is DutType.mos:
        spec_voltage_0 = specifiers.VOLTAGE + "S"
        spec_current_0 = specifiers.CURRENT + "S"
        spec_voltage_1 = specifiers.VOLTAGE + "G"
        spec_current_1 = specifiers.CURRENT + "G"
        spec_voltage_2 = specifiers.VOLTAGE + "D"
        spec_current_2 = specifiers.CURRENT + "D"
        spec_voltage_3 = specifiers.VOLTAGE + "B"
        spec_current_3 = specifiers.CURRENT + "B"
    elif dut_type is DutType.bjt:
        spec_voltage_0 = specifiers.VOLTAGE + "E"
        spec_current_0 = specifiers.CURRENT + "E"
        spec_voltage_1 = specifiers.VOLTAGE + "B"
        spec_current_1 = specifiers.CURRENT + "B"
        spec_voltage_2 = specifiers.VOLTAGE + "C"
        spec_current_2 = specifiers.CURRENT + "C"
        spec_voltage_3 = specifiers.VOLTAGE + "S"
        spec_current_3 = specifiers.CURRENT + "S"

    if not v10.size == 0 and not v12.size == 0:
        if len(v10) > len(v12):
            if len(v12) == 1:
                swp_name = "v10_sweep_at_v12_{0:2.2f}".format(v12[0]).replace(".", "p")
            else:
                swp_name = "v10_sweep_at_v12"
            sweepdef = [
                SweepDefSync(
                    spec_voltage_2, spec_voltage_1, spec_voltage_1 + spec_voltage_2, sweep_order=3
                ),
                SweepDefList(
                    spec_voltage_1,
                    sweep_order=3,
                    value_def=v10,
                ),
                SweepDefList(
                    spec_voltage_1 + spec_voltage_2,
                    sweep_order=2,
                    value_def=v12,
                ),
                SweepDefConst(
                    spec_voltage_0,
                    sweep_order=1,
                    value_def=[0],
                ),
            ]
        else:
            if len(v10) == 1:
                swp_name = "v12_sweep_at_v10_{0:2.2f}".format(v10[0]).replace(".", "p")
            else:
                swp_name = "v12_sweep_at_v10"
            v12_rev = v12
            v12_rev[0] = -v12_rev[0]
            v12_rev[1] = -v12_rev[1]
            sweepdef = [
                SweepDefList(
                    spec_voltage_2,
                    sweep_order=3,
                    value_def=v12_rev,
                ),
                SweepDefList(
                    spec_voltage_0,
                    sweep_order=2,
                    value_def=-v10,
                ),
                SweepDefConst(
                    spec_voltage_1,
                    sweep_order=1,
                    value_def=[0],
                ),
            ]
    elif not v10.size == 0 and not v20.size == 0:
        if len(v10) > len(v20):
            if len(v20) == 1:
                swp_name = "v10_sweep_at_v20_{0:2.2f}".format(v20[0]).replace(".", "p")
            else:
                swp_name = "v10_sweep_at_v20"
            sweepdef = [
                SweepDefList(
                    spec_voltage_1,
                    sweep_order=3,
                    value_def=v10,
                ),
                SweepDefList(
                    spec_voltage_2,
                    sweep_order=2,
                    value_def=v20,
                ),
                SweepDefConst(
                    spec_voltage_0,
                    sweep_order=1,
                    value_def=0,
                ),
            ]
        else:
            if len(v10) == 1:
                swp_name = "v20_sweep_at_v10_{0:2.2f}".format(v10[0]).replace(".", "p")
            else:
                swp_name = "v20_sweep_at_v10"
            sweepdef = [
                SweepDefList(
                    spec_voltage_2,
                    sweep_order=3,
                    value_def=v20,
                ),
                SweepDefList(
                    spec_voltage_1,
                    sweep_order=2,
                    value_def=v10,
                ),
                SweepDefConst(
                    spec_voltage_0,
                    sweep_order=1,
                    value_def=[0],
                ),
            ]
    elif not v20.size == 0 and not i1.size == 0:
        if len(v20) > len(i1):
            if len(i1) == 1:
                swp_name = "v20_sweep_at_i1_{0:2.2f}mA".format(i1[0] * 1e3).replace(".", "p")
            else:
                swp_name = "v20_sweep_at_i1"
            sweepdef = [
                SweepDefList(
                    spec_voltage_2,
                    sweep_order=3,
                    value_def=v20,
                ),
                SweepDefList(
                    spec_current_1,
                    sweep_order=2,
                    value_def=i1,
                ),
                SweepDefConst(
                    spec_voltage_0,
                    sweep_order=1,
                    value_def=[0],
                ),
            ]
    elif not v12.size == 0 and not i0.size == 0:
        if len(v12) > len(i0):
            if len(i0) == 1:
                swp_name = "v12_sweep_at_i0_{0:2.2f}mA".format(i0[0] * 1e3).replace(".", "p")
            else:
                swp_name = "v12_sweep_at_i0"
            v21 = [-v12[0], -v12[1], v12[2]]
            sweepdef = [
                SweepDefList(
                    spec_voltage_2,
                    sweep_order=3,
                    value_def=v21,
                ),
                SweepDefList(
                    spec_current_0,
                    sweep_order=2,
                    value_def=i0,
                ),
                SweepDefConst(
                    spec_voltage_1,
                    sweep_order=1,
                    value_def=[0],
                ),
            ]
    else:
        raise NotImplementedError

    if len(v30) == 1:
        if v30[0] == 0:
            pass  # V30 should default to zero in the netlists
        else:  # we add the substrate or bulk voltage explicitly as the outermost constant sweep
            sweep_order_voltage_3 = max([swd.sweep_order for swd in sweepdef]) + 1
            sweepdef.append(
                SweepDefConst(
                    spec_voltage_3,
                    sweep_order=sweep_order_voltage_3,
                    value_def=v30,
                )
            )
    elif len(v30) > 1:
        sweep_order_voltage_3 = max([swd.sweep_order for swd in sweepdef]) + 1
        sweepdef.append(
            SweepDefList(
                spec_voltage_3,
                sweep_order=sweep_order_voltage_3,
                value_def=v30,
            )
        )

    if ac and freq is not None:
        sweep_order_ac = max([swd.sweep_order for swd in sweepdef]) + 1
        if isinstance(freq, float):
            freq = [freq]
        if len(freq) == 1:
            sweepdef.append(
                {
                    "var_name": specifiers.FREQUENCY,
                    "sweep_order": sweep_order_ac,
                    "sweep_type": "CON",
                    "value_def": freq,
                },
            )
        else:
            sweepdef.append(
                {
                    "var_name": specifiers.FREQUENCY,
                    "sweep_order": sweep_order_ac,
                    "sweep_type": "LOG",
                    "value_def": freq,
                },
            )

    if isinstance(temp, list):
        othervar = {}
        for i, _swd in enumerate(sweepdef):
            sweepdef[i]["sweep_order"] = sweepdef[i]["sweep_order"] + 1

        sweepdef.append(
            {
                "sweep_order": 1,
                "sweep_type": "LIN",
                "value_def": temp,
                "var_name": specifiers.TEMPERATURE,
            },
        )
    else:
        othervar = {"TEMP": temp}

    # Replace the generic two-port pin names with ones that correspond to either a MOSFET or BJT in common emitter/source
    # configuration.
    if name is None:
        if dut_type == DutType.mos:
            swp_name = swp_name.replace("v10", "vgs")
            swp_name = swp_name.replace("v12", "vgd")
            swp_name = swp_name.replace("v21", "vdg")
            swp_name = swp_name.replace("v20", "vds")
            swp_name = swp_name.replace("i1", "ig")
            swp_name = swp_name.replace("i2", "id")
            swp_name = swp_name.replace("i0", "ie")
        elif dut_type == DutType.bjt:
            swp_name = swp_name.replace("v10", "vbe")
            swp_name = swp_name.replace("v12", "vbc")
            swp_name = swp_name.replace("v21", "vcb")
            swp_name = swp_name.replace("v20", "vce")
            swp_name = swp_name.replace("i1", "ib")
            swp_name = swp_name.replace("i2", "ic")
            swp_name = swp_name.replace("i0", "ie")
    else:
        swp_name = name

    sweep = Sweep(swp_name, sweepdef=sweepdef, outputdef=[], othervar=othervar)
    return sweep
