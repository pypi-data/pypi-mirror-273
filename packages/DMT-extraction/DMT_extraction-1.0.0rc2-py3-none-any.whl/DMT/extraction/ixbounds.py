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
import math
import numpy as np


class Bounds(object):
    """Base class for all Bounds classes used by XStep to select a sub-region of the reference data for fitting."""

    def __init__(self):
        self._low = None
        self._high = None
        self.widget = None

    @property
    def low(self):
        """Getter for the lower bounds of the boundaries."""
        return self._low

    @low.setter
    def low(self, low_new):
        """Setter for the lower bounds of the boundaries."""
        if (self._high is None) or (low_new <= self._high) or np.isnan(self._high).any():
            self._low = low_new

    @property
    def high(self):
        """Getter for the upper (high) bounds of the boundaries."""
        return self._high

    @high.setter
    def high(self, high_new):
        """Setter for the upper (high) bounds of the boundaries."""
        if (self._low is None) or (high_new >= self._low) or np.isnan(self._low).any():
            self._high = high_new

    def __str__(self):
        """Method that converts the Bounds object information to a string."""
        return f"(Min:{self._low:.3e}; Max:{self._high:.3e})"

    def __format__(self, wanted_format):
        """Formatting method that converts the Bounds object information as a string using the "format" method."""
        if (
            ("d" in wanted_format)
            or ("e" in wanted_format)
            or ("f" in wanted_format)
            or ("g" in wanted_format)
        ):
            return f"({self.low:{wanted_format}}, {self.high:{wanted_format}})"

        if "s" in wanted_format:
            return f"(Min:{self._low:.3g}; Max:{self._high:.3g})"

        raise IOError(f"The format {wanted_format} is unknown for Bounds!")


class XBounds(Bounds):
    """Implements X-axis boundaries based on the base class Bounds."""

    def __init__(self, xdata):
        super().__init__()
        self.update(xdata)

    def update(self, xdata):
        """Overwrite the current lower and upper boundaries.

        Parameters
        ----------
        xdata : array, np.array
            The x-axis values that shall lie within the boundaries self.low, self.high.
        """
        self.low = np.real(np.nanmin(xdata))
        self.high = np.real(np.nanmax(xdata))

        if math.isnan(self.low) and math.isnan(self.high):
            self.low = 0
            self.high = 0
        elif math.isnan(self.low):
            self.low = self.high * 0.9
        elif math.isnan(self.high):
            self.high = self.low * 1.1


class YBounds(Bounds):
    """Implements Y-axis boundaries based on the base class Bounds."""

    def __init__(self, ydata):
        super().__init__()
        self.update(ydata)

    def update(self, ydata):
        """Overwrite the current lower and upper boundaries.

        Parameters
        ----------
        ydata : array, np.array
            The y-axis values that shall lie within the boundaries.
        """
        self.low = np.nanmin(ydata)
        self.high = np.nanmax(ydata)

        if math.isnan(self.low) and math.isnan(self.high):
            self.low = 0
            self.high = 0
        elif math.isnan(self.low):
            self.low = self.high * 0.9
        elif math.isnan(self.high):
            self.high = self.low * 1.1


class XYBounds(Bounds):
    """Implements two dimensional XY-axis boundaries based on the base class Bounds.
    Basically this is a rectangular area.
    """

    def __init__(self, xdata=None, ydata=None, new_bounds=None):
        super().__init__()
        self.update(xdata, ydata)

    def update(self, xdata, ydata):
        """Overwrite the current lower and upper X and Y boundaries.

        Parameters
        ----------
        xdata : array, np.array
            The x-axis values that shall lie within the boundaries.
        ydata : array, np.array
            The y-axis values that shall lie within the boundaries.
        """
        self.low = (np.nanmin(xdata), np.nanmin(ydata))
        self.high = (np.nanmax(xdata), np.nanmax(ydata))

    def __str__(self):
        return f"(Min:({self._low[0]:.3g}, {self._low[1]:.3g}); Max:({self._high[0]:.3g}, {self._high[1]:.3g}))"

    def __format__(self, wanted_format):
        if (
            ("d" in wanted_format)
            or ("e" in wanted_format)
            or ("f" in wanted_format)
            or ("g" in wanted_format)
        ):
            return f"(({self._low[0]:{wanted_format}}, {self._low[1]:{wanted_format}}), ({self._high[0]:{wanted_format}}, {self._high[1]:{wanted_format}}))"

        if "s" in wanted_format:
            return f"(Min:({self._low[0]:.3g}, {self._low[1]:.3g}); Max:({self._high[0]:.3g}, {self._high[1]:.3g}))"

        raise IOError(f"The format {wanted_format} is unknown for Bounds!")
