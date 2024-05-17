""" Methods for finding points and regions in vectors.
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
from scipy.interpolate import UnivariateSpline

from DMT.extraction.find_nearest import find_nearest_index


def get_poly_region(x_vals, y_vals, x_range, degree, r_ov_ymax, sort=False):
    """Enlarge the x_range as long as the linear fit for this range is still "good enough"

    Parameters
    ----------
    x_vals, y_vals : array
    x_range : (float, float)
        Range inside x_vals, in this region the region will be searched
    degree : int
        Degree of polynomial fit. If a constant region is searched use 0, for a linear use 1.
    r_ov_ymax : float
        Maximum for the relative conditional number for the polyfit iteration.
    sort : {False, True}, optional
        If true, x_vals and y_vals are sorted before smoothing spline.
    Returns
    --------
    poly_final : ndarray
        Final polynomial coefficients for the fit
    (x_lower, x_upper) : tuple
        Lower and upper borders of the polynomial region
    """

    if x_range[0] == x_range[1]:
        # same values -> whole x vector
        x_low = x_vals[0]
        x_upp = x_vals[-1]
    else:
        x_low = min(x_range)
        x_upp = max(x_range)

    # In case x_low and/or x_upp are not in x_vals -> find nearest
    ind_x1 = find_nearest_index(x_low, x_vals)
    ind_x2 = find_nearest_index(x_upp, x_vals)

    # add one because numpy counts from i_l to i_u-1
    x_vals = x_vals[ind_x1 : ind_x2 + 1]
    y_vals = y_vals[ind_x1 : ind_x2 + 1]
    # max y in given range used to normalize R
    y_max = max(y_vals)

    # smoothing spline. Sort before if wanted.
    if sort:
        ind_sort = np.argsort(x_vals)
        x_vals = x_vals[ind_sort]
        y_vals = y_vals[ind_sort]
    # cubic (k=3) smoothing spline
    u_spline = UnivariateSpline(x_vals, y_vals, k=3)

    # "zero" of u_spline
    ind_x_zero = np.argmin(abs(u_spline.derivative(degree + 1)(x_vals)))
    # for constant 1st derivative must be zero, for linear second

    # starting values for the linear region
    # around the local minium +-1 (if possible)
    if ind_x_zero > 0:
        ind_x_rl = ind_x_zero - 1
    else:
        ind_x_rl = ind_x_zero

    if ind_x_zero < len(x_vals) - 1:
        ind_x_ru = ind_x_zero + 1
    else:
        ind_x_ru = ind_x_zero

    # Lower and Upper index of the region are equal
    # It was not possible to enlarge the local minium
    if ind_x_rl == ind_x_ru:
        raise OSError("Inside the given range only one value was found!")

    enlarge_low = True
    enlarge_up = True
    while enlarge_low or enlarge_up:
        if ind_x_rl > 0:
            [_poly, res1, _rank, _s, _covariance_matrix] = np.polyfit(
                x_vals[ind_x_rl - 1 : ind_x_ru + 1],
                y_vals[ind_x_rl - 1 : ind_x_ru + 1],
                degree,
                full=True,
            )
            if abs(res1 / y_max) <= r_ov_ymax:
                # relative condition number is smaller than given condition -> enlarge
                ind_x_rl = ind_x_rl - 1
            else:
                # stop enlarging here
                enlarge_low = False
        else:
            # reached index 0
            enlarge_low = False
        if ind_x_ru < len(x_vals) - 1:
            [_poly, res2, _rank, _s, _covariance_matrix] = np.polyfit(
                x_vals[ind_x_rl : ind_x_ru + 2], y_vals[ind_x_rl : ind_x_ru + 2], degree, full=True
            )
            if abs(res2 / y_max) <= r_ov_ymax:
                # relative condition number is smaller than given condition -> enlarge
                ind_x_ru = ind_x_ru + 1
            else:
                # stop enlarging here
                enlarge_up = False
        else:
            # reached end of range
            enlarge_up = False

    [poly_final, _res, _rank, _s, _covariance_matrix] = np.polyfit(
        x_vals[ind_x_rl : ind_x_ru + 1], y_vals[ind_x_rl : ind_x_ru + 1], degree, full=True
    )

    return [poly_final, (x_vals[ind_x_rl], x_vals[ind_x_ru])]
