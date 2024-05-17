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
name = "psp"

# some va codes in the package, this way they can be used easily:
from pathlib import Path

path_psp = Path(__file__).resolve().parent

# put here the path to the VA file.
VA_FILES = {
    "juncap200p4": path_psp / "va_code_psp103p4/juncap200.va",
    "psp103p4": path_psp / "va_code_psp103p4/psp103.va",
    "psp103p4t": path_psp / "va_code_psp103p4/psp103t.va",
    "psp103p4nqs": path_psp / "va_code_psp103p4/psp103_nqs.va",
    "juncap200p6": path_psp / "va_code_psp103p6/juncap200.va",
    "psp103p6": path_psp / "va_code_psp103p6/psp103.va",
    "psp103p6t": path_psp / "va_code_psp103p6/psp103t.va",
    "psp103p6nqs": path_psp / "va_code_psp103p6/psp103_nqs.va",
    "juncap200p8": path_psp / "va_code_psp103p8/juncap200.va",
    "psp103p8": path_psp / "va_code_psp103p8/psp103.va",
    "psp103p8t": path_psp / "va_code_psp103p8/psp103t.va",
    "psp103p8nqs": path_psp / "va_code_psp103p8/psp103_nqs.va",
}


class _DefaultVAFiles(object):
    def __init__(self):
        self.juncap200p4 = path_psp / "va_code_psp103p4/juncap200.va"
        self.psp103p4 = path_psp / "va_code_psp103p4/psp103.va"
        self.psp103p4t = path_psp / "va_code_psp103p4/psp103t.va"
        self.psp103p4nqs = path_psp / "va_code_psp103p4/psp103_nqs.va"
        self.juncap200p6 = path_psp / "va_code_psp103p6/juncap200.va"
        self.psp103p6 = path_psp / "va_code_psp103p6/psp103.va"
        self.psp103p6t = path_psp / "va_code_psp103p6/psp103t.va"
        self.psp103p6nqs = path_psp / "va_code_psp103p6/psp103_nqs.va"
        self.juncap200p8 = path_psp / "va_code_psp103p8/juncap200.va"
        self.psp103p8 = path_psp / "va_code_psp103p8/psp103.va"
        self.psp103p8t = path_psp / "va_code_psp103p8/psp103t.va"
        self.psp103p8nqs = path_psp / "va_code_psp103p8/psp103_nqs.va"


default_va_files = _DefaultVAFiles()


# VSM model card
from .mc_psp import McPsp
from .psp_data_processor import find_dtj, deemb_to_internal_DC

from .x_cgg import XCgg
from .x_ccg import XCcg
from .x_ids_vg import XIdsVg
from .x_ids_vd import XIdsVd
from .x_gm import XGm
from .x_gds import XGds
from .x_ib import XIb
from .x_ig import XIg
from .x_y_vt import XYVt
from .x_y_rs import XYRs
from .x_juncap_cap import XJuncapCap
from .x_juncap_current import XJuncapCurrent
