""" Functions to extract dimenions from given dut name
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
import re


def ex_dimension_width(dut_name):
    """Extract the dimension width of a DuT name (string) for a name like 0p13x10p16.
    The extracted dimension correspond to drawn emitter window WIDTH.

    Parameters
    ----------
    dut_name : str
        The name of the DuT for which the dimension width shall be extracted.

    Returns
    -------
    width : float
        The determined width of the DuT.
    """
    width = re.search(r"(\d+p\d+)x", dut_name)
    if width:
        width = width.group(1)
        width = width.replace("p", ".")
    else:
        raise OSError("filter_dut->Width of DuT cannot be extracted.")
    return round(float(width) * 1e-6, 8)


def ex_dimension_length(dut_name):
    """Extract the dimension length of a DuT name (string) for a name like 0p13x10p16.
    The extracted dimension correspond to drawn emitter window LENGTH.

    Parameters
    ----------
    dut_name : str
        The name of the DuT for which the dimension length shall be extracted.

    Returns
    -------
    length : float
        The determined length of the DuT.
    """
    length = re.search(r"x(\d+p\d+)", dut_name)
    if length:
        length = length.group(1)
        length = length.replace("p", ".")
    else:
        raise OSError("filter_dut->Length of DuT cannot be extracted.")
    return round(float(length) * 1e-6, 8)
