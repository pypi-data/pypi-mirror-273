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
import numpy as np
import copy
from DMT.core import specifiers, sub_specifiers, DataFrame, constants
from DMT.psp.mc_psp import McPsp


def find_dtj(model, t_dev=None, p=None, *, RTH=None, **kwargs):
    """
    Find the junction temperature increase for each element of p due to self heating by solving the PSP temperature network using the Newton algorithm.

    model : VerilogAE.Model()
    """
    d_tj = np.zeros_like(p)
    if RTH is None or RTH == 0:  # should do the same
        return d_tj
    else:
        for i, (p_i, d_tj_i) in enumerate(zip(p, d_tj)):
            while True:
                f_dtj = (
                    p_i
                    * model.functions["RTH_T"].eval(
                        voltages={}, temperature=t_dev + d_tj_i, RTH=RTH, **kwargs
                    )
                    - d_tj_i
                )

                # small deviation to numerically find derivative
                df_dtj = p_i * model.functions["RTH_T"].eval(
                    temperature=t_dev + d_tj_i + 1e-3,
                    RTH=RTH,
                    pterm=p_i,
                    voltages={},
                    **kwargs,
                ) - (d_tj_i + 1e-3)

                df_dtj = (df_dtj - f_dtj) / 1e-3  # (f(x+h)-f(x))/h
                f_df = f_dtj / df_dtj
                d_tj_i = d_tj_i - 1 * f_df
                # if t_dev - d_tj_i < 0:
                # print('DMT -> find_dtj: Convergence Problems')
                # d_tj_i = d_tj_i/3

                if np.abs(f_df) < 1e-3:
                    d_tj[i] = d_tj_i  # pylint: disable=unsupported-assignment-operation
                    break

    # limit temperature
    TMIN = -100
    TMAX = 326.85
    d_tj = np.clip(d_tj, TMIN - t_dev + 273.15, TMAX - t_dev + 273.15)

    # if(Tdev < `TMIN + 273.15) begin
    #     Tdev = `TMIN + 273.15;
    # end else begin
    #     if (Tdev > `TMAX + 273.15) begin
    #         Tdev = `TMAX + 273.15;
    #     end
    # end

    return d_tj


def deemb_to_internal_DC(df: DataFrame, mc: McPsp, t_dev: float, model):
    """Deembeds the internal transistor but only DC. Use this to get the correct voltages for the internal currents

    Parameters
    ----------
    df : DMT.DataFrame()
        Measured DC currents of a MOSFET
    mc : DMT.MCard()
        A PSP Modelcard that will be used to determine the voltage drops towards the transistor.
    t_dev : float
        Ambient measurement temperature
    model : verilogae module

    Returns
    -------
    df_deemb : DMT.DataFrame()
        The df with the internal voltages and currents
    """
    df_deemb = copy.deepcopy(df)
    mc_kwargs = mc.to_kwargs()  # cast modelcard to kwargs for later use
    mc_kwargs = {k.upper(): v for k, v in mc_kwargs.items()}

    # definition of columns
    col_vb = specifiers.VOLTAGE + "B"

    col_vbp = specifiers.VOLTAGE + "BP"
    col_vbs = specifiers.VOLTAGE + "BS"
    col_vbd = specifiers.VOLTAGE + "BD"

    col_vg = specifiers.VOLTAGE + "G"
    col_vd = specifiers.VOLTAGE + "D"
    col_vs = specifiers.VOLTAGE + "S"

    col_id = specifiers.CURRENT + "D"
    col_is = specifiers.CURRENT + "S"
    col_ig = specifiers.CURRENT + "G"
    col_ib = specifiers.CURRENT + "B"

    try:
        i_d = df_deemb[col_id].to_numpy().real
        v_d = df_deemb[col_vd].to_numpy().real
    except KeyError:
        i_d = np.zeros(len(df_deemb.index))
        v_d = np.zeros(len(df_deemb.index))

    try:
        v_g = df_deemb[col_vg].to_numpy().real
        i_g = df_deemb[col_ig].to_numpy().real
    except KeyError:
        i_g = np.zeros(len(df_deemb.index))
        v_g = np.zeros(len(df_deemb.index))

    try:
        v_s = df_deemb[col_vs].to_numpy().real
        i_s = df_deemb[col_is].to_numpy().real
    except KeyError:
        v_s = np.zeros(len(df_deemb.index))
        i_s = np.zeros(len(df_deemb.index))

    try:
        v_b = df_deemb[col_vb].to_numpy().real
        i_b = df_deemb[col_ib].to_numpy().real
    except KeyError:
        v_b = np.zeros(len(df_deemb.index))
        i_b = np.zeros(len(df_deemb.index))

    # first correct temperature !!
    p = i_d * (v_d - v_s)
    t_dev += find_dtj(model, t_dev=t_dev, p=p, **mc_kwargs).real

    df_deemb[specifiers.TEMPERATURE] = t_dev

    # internal nodes of the PSP model
    # electrical GP; Connection: G - RG - GP
    # electrical SI; Connection: S - RSE - SI
    # electrical DI; Connection: D - RDE - D
    # electrical BI; Connection: B - RWELL - BI

    # electrical BP; Connection: BP - RBULK - BI
    # electrical BS; Connection: BS - RJUNS - BI
    # electrical BD; Connection: BD - RJUND - BI

    # DC deembedding
    voltages = {
        "br_DT": t_dev - mc_kwargs["DTA"] - mc_kwargs["TR"] - constants.P_CELSIUS0,
    }
    r_g = model.functions["RG_i"].eval(temperature=t_dev, voltages=voltages, **mc_kwargs)
    r_se = model.functions["RSE_i"].eval(temperature=t_dev, voltages=voltages, **mc_kwargs)
    r_de = model.functions["RDE_i"].eval(temperature=t_dev, voltages=voltages, **mc_kwargs)
    r_well = model.functions["RWELL_i"].eval(temperature=t_dev, voltages=voltages, **mc_kwargs)

    r_bulk = model.functions["RBULK_i"].eval(temperature=t_dev, voltages=voltages, **mc_kwargs)
    r_juns = model.functions["RJUNS_i"].eval(temperature=t_dev, voltages=voltages, **mc_kwargs)
    r_jund = model.functions["RJUND_i"].eval(temperature=t_dev, voltages=voltages, **mc_kwargs)

    df_deemb[col_vg] = v_g - r_g * i_g
    df_deemb[col_vs] = v_s + r_se * i_s
    df_deemb[col_vd] = v_d - r_de * i_d
    df_deemb[col_vb] = v_b + r_well * i_b

    # how to split the current?
    # for now assume major current going into main transistor and not into junctions :/
    df_deemb[col_vbp] = df_deemb[col_vb] + r_bulk * i_b
    df_deemb[col_vbs] = df_deemb[col_vb] - r_juns * 0
    df_deemb[col_vbd] = df_deemb[col_vb] - r_jund * 0

    # remove voltages
    df_deemb = df_deemb.drop_all_voltages()

    return df_deemb
