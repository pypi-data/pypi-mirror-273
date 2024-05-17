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
import abc
import numpy as np


class IYNorm(object):
    """This abstract class defines an interface for different y_values normalization strategies to be used by XStep objects.

    Parameters
    ----------
    y_values : np.array()
        This array shall contain the y_values to be normalized.

    Methods
    -------
    normalize()
        Return an array that contains normalized y_values according to different Sub-class implementations.
    """

    def __init__(self, y_values):
        pass

    @abc.abstractmethod
    def normalize(self, values):
        """This abstract method must be overwritten by subclasses.

        Parameters
        ----------
        values : np.ndarray()
            The y-array that shall be normalized.

        Returns
        -------
        values : np.ndarray()
            The normalized data.
        """
        pass


class IYNormNone(IYNorm):
    """This subclass performs no normalization at all."""

    def normalize(self, values):
        return values


class IYNormDefault(IYNorm):
    """This subclass normalizes the y_values so that they lie between 0 and 1."""

    def __init__(self, y_values):
        super().__init__(y_values)
        self.max = np.max(y_values)
        self.min = np.min(y_values)
        self.delta = self.max - self.min

    def normalize(self, values):
        return (values - self.min) / self.delta


class IYNormFactor(IYNorm):
    """This subclass normalizes the y_values using a constant factor that is multiplied to the data.
    The factor is equal to the minimum of the init values.
    """

    def __init__(self, y_values):
        super().__init__(y_values)
        self.factor = np.min(y_values)

    def normalize(self, values):
        return values * self.factor


class IYNormLog(IYNorm):
    """This subclass normalizes the y_values using np.log10.
    If somehow a nan value occurs, it is set to 1e9."""

    def normalize(self, values):
        if np.any(values == 0):
            raise IOError(
                "IYNormLog received values that contain zeroes (Mathematically impossible). Likely, the init_data_reference method of your XStep has put zeros into the data_reference."
            )
        new_values = np.log10(np.abs(values))
        i_nan = np.where(np.isnan(new_values))
        new_values[i_nan] = 1e9
        return new_values


class IYNormLog_1(IYNorm):
    """This subclass normalizes the y_values using np.log10(1+values).
    If somehow a nan value occurs, it is set to 1e9."""

    def normalize(self, values):
        # new_values = np.ndarray(len(values))
        new_values = np.empty_like(values)
        np.log10(values + 1, out=new_values)

        i_nan = np.where(np.isnan(new_values))
        new_values[i_nan] = 1e9
        # for i, val in enumerate(values):
        #     val_new = np.log10( 1 + val )
        #     new_values[i] = val_new

        return new_values


class IYNormLogOneRange(IYNorm):
    """This subclass normalizes the y_values using np.log10(values'), where values' corresponds to
    the values normalized between 0 and 1.
    If somehow a nan value occurs, it is set to 1e9."""

    def __init__(self, y_values):
        super().__init__(y_values)
        self.max = np.max(y_values)
        self.min = np.min(y_values)
        self.delta = self.max - self.min

    def normalize(self, values):
        new_values = np.empty_like(values)

        np.log10((values - self.min) / self.delta + 1, out=new_values)
        new_values /= np.log10(2)

        i_nan = np.where(np.isnan(new_values))
        new_values[i_nan] = 1e9
        return new_values
