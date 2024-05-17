""" Functions to find a value and/or index in a array
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


def find_nearest_index(value, array):
    """Find the index of the value in array nearest to value.
    Copied From : https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

    Parameters
    ----------
    value : float, np.array[1]
        The value for which the index in the array is to be determined.
    array : [], np.array()
        The array for which the index of value shall be determined.

    Returns
    -------
    i_value : Index
        The index that corresponds to the closest value to "value" in array.
    """
    # convert to np.array -> also usable in pandas
    array = np.asarray(array)
    try:
        value = np.ndarray.item(value.to_numpy())
    except AttributeError:
        try:
            value = np.ndarray.item(value)
        except TypeError:
            pass

    if value == np.inf:
        i_value = np.argmax(array)
    elif value == -np.inf:
        i_value = np.argmin(array)

    return (np.abs(array - value)).argmin()


def find_nearest(value, array):
    """Find the index of the value in array nearest to value, and also the corresponding value in the array.
    Copied From : https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array

    Parameters
    ----------
    value : float, np.array[1]
        The value for which the index in the array is to be determined.
    array : [], np.array()
        The array for which the index of value shall be determined.

    Returns
    -------
    [value, i_value] : [np.float, Index]
        The index and value in array that are closest to "value".
    """
    if value == np.inf:
        i_value = np.argmax(array)
    elif value == -np.inf:
        i_value = np.argmin(array)

    i_value = find_nearest_index(value, array)
    return [array[i_value], i_value]
