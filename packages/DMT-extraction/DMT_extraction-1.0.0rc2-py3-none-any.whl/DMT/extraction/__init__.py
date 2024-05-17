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
name = "extraction"

# utils includes routines that are convenient for coding parameter extraction steps via the DMT.extraction.XStep class.
from .utils import sub_specifier_parameter

# mathematical normalization routines
from .iynorm import IYNormNone, IYNormDefault, IYNormLog, IYNormLog_1, IYNormLogOneRange

# mathematical convenience functions to find nearest elements in array and polynomial approximation
from .find_nearest import find_nearest, find_nearest_index
from .get_poly_region import get_poly_region

# functions for extracting geometry information from device names
from .extract_dimensions import ex_dimension_width, ex_dimension_length

# base class for compact models
from .model import Model

# parameter extraction step implementation classes and routines. Main classes are Xtraction and XStep.
from .ixbounds import Bounds, XBounds, YBounds, XYBounds
from .x_step import XStep, plot, print_to_documentation
from .mx_step import MXStep
from .xtraction import Xtraction
from .docu_xtraction import DocuXtraction
from .xstep_parameter_table import XStepParameterTable

# routines for virtual data generation
from .generate_virtual_data import generate_virtual_data
from .generate_virtual_data import get_sweep_fgummel
from .generate_virtual_data import get_sweep_mos
from .generate_virtual_data import get_sweep_bjt

# Perimeter over Area separation steps implemented as QStep with subclasses XQPoa, XQPoaBilinearFull, XQPoX
from .q_step import QStep
from .xq_poa import XQPoa
from .xq_poa_bilinear_full import XQPoaBilinearFull
from .xq_poa_x import XQPoX
from .xq_poa_bilinear_full_reg import XQPoaBilinearFullReg
from .xq_poa_only_perimeter import XQPoaOnlyPerimeter

# XVerify is a subclass of XStep that runs circuit simulations instead of evaluating analytical equations
from .x_verify import XVerify

# XVerifyMMC can optimize several circuit simulation target characteristics at the same time
from .x_verify_mmc import XVerifyMMC

# Resistance extraction step
from .x_res import XRes

# For jupyter test and playing around
from .x_diode import XDiode
from .model_diode import ModelDiode
