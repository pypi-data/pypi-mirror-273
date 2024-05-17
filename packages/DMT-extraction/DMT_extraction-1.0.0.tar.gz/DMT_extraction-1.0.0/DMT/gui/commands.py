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
import copy
import logging
from qtpy.QtWidgets import QUndoCommand


# These classes are an implementation of the Command design pattern, using the Qt Framework (QUndoStack+QUndoCommand)
class SetOptimizationParaNormalization(QUndoCommand):
    """Set wheather or not the parameters of the model shall be normalized during the optimization."""

    def __init__(self, step, box):
        super().__init__()
        self.step = step
        self.box = box
        self.normalize = box.isChecked()

    def redo(self):
        logging.info(
            "SetOptimizationParaNormalization: changed normalize value of step %s to %s.",
            self.step.name,
            self.normalize,
        )
        self.step.normalize = self.normalize
        self.box.setChecked(self.step.normalize)

    def undo(self):
        logging.info(
            "SetOptimizationParaNormalization: changed normalize value of step %s to %s.",
            self.step.name,
            not self.normalize,
        )
        self.step.normalize = not self.normalize
        self.box.setChecked(self.step.normalize)


class SetOptimizationMethod(QUndoCommand):
    """Change the optimization method of step to new_fit_method."""

    def __init__(self, step, text_edit, new_fit_method):
        super().__init__()
        self.step = step
        self.old_fit_method = step.fit_method
        self.new_fit_method = new_fit_method
        self.text_edit = text_edit

    def redo(self):
        logging.info(
            "SetOptimizationMethod: changed method of step %s to %s.",
            self.step.name,
            self.new_fit_method,
        )
        self.step.fit_method = self.new_fit_method

    def undo(self):
        logging.info(
            "SetOptimizationMethod: changed method of step %s to %s.",
            self.step.name,
            self.old_fit_method,
        )
        self.step.fit_method = self.old_fit_method
        self.text_edit.setCurrentText(self.old_fit_method)


class SetOptimizationTolerance(QUndoCommand):
    """Change the optimization tolerance of step to new_tol ."""

    def __init__(self, step, editor, new_tol):
        super().__init__()
        self.step = step
        self.editor = editor
        self.old_tol = step.f_tol
        self.new_tol = new_tol

    def redo(self):
        logging.info(
            "SetOptimizationTolerance: changed ftol of step %s to %s.", self.step.name, self.new_tol
        )
        self.editor.setText(str(self.new_tol))
        self.step.f_tol = self.new_tol

    def undo(self):
        logging.info(
            "SetOptimizationTolerance: changed ftol of step %s to %s.", self.step.name, self.old_tol
        )
        self.editor.setText(str(self.old_tol))
        self.step.f_tol = self.old_tol


class SetMcard(QUndoCommand):
    """Set a steps new mcard"""

    def __init__(self, step, new_mcard):
        super().__init__()
        self.step = step
        self.old_mcard = copy.deepcopy(step.mcard)
        self.new_mcard = copy.deepcopy(new_mcard)

    def redo(self):
        self.step.mcard = self.new_mcard
        self.step.mcardChanged.emit()

    def undo(self):
        self.step.mcard = self.old_mcard
        self.step.mcardChanged.emit()


class SetPara(QUndoCommand):
    """Change one Parameter of an xstep"""

    def __init__(self, step, new_para):
        super().__init__()
        self.step = step
        self.new_para = copy.deepcopy(new_para)
        self.old_para = copy.deepcopy(step.mcard.get(new_para))

    def redo(self):
        logging.info(
            "SetPara: changed para %s [min, value, max] from [%s, %s, %s] to [%s, %s, %s].",
            self.new_para.name,
            self.old_para.min,
            self.old_para.value,
            self.old_para.max,
            self.new_para.min,
            self.new_para.value,
            self.new_para.max,
        )
        self.step.mcard.set(self.new_para)
        self.step.paras_to_optimize = self.step.mcard.get(self.step.paras_to_optimize)
        self.step.mcardChanged.emit()

    def undo(self):
        logging.info(
            "SetPara: changed para %s [min, value, max] from [%s, %s, %s] to [%s, %s, %s].",
            self.new_para.name,
            self.new_para.min,
            self.new_para.value,
            self.new_para.max,
            self.old_para.min,
            self.old_para.value,
            self.old_para.max,
        )
        self.step.mcard.set(self.old_para)
        self.step.mcardChanged.emit()


class PullCommand(QUndoCommand):
    """Change the optimization tolerance of step to new_tol ."""

    def __init__(self, xtraction):
        super().__init__()
        self.xtraction = xtraction
        self.old_local_mcard = copy.deepcopy(xtraction.curr_xstep.mcard)

    def redo(self):
        logging.info("PullCommand: pulled the global mcard to the current xstep.")
        self.xtraction.pull_global_mcard()

    def undo(self):
        logging.info("PullCommand: reset the the current xstep mcard to the last one.")
        self.xtraction.pull_global_mcard(mcard=self.old_local_mcard)


class PushCommand(QUndoCommand):
    """Change the optimization tolerance of step to new_tol ."""

    def __init__(self, xtraction):
        super().__init__()
        self.xtraction = xtraction
        self.old_global_mcard = copy.deepcopy(
            xtraction.mcard
        )  # todo: only push the actually required ones

    def redo(self):
        logging.info("PushCommand: pushed the global mcard to the current xstep.")
        self.xtraction.push_local_mcard()

    def undo(self):
        logging.info("PushCommand: reset the global mcard to the last one.")
        self.xtraction.push_local_mcard(mcard=self.old_global_mcard)


class SetOptimizationNmax(QUndoCommand):
    """Change the step's optimization maximum number of steps  to nmax."""

    def __init__(self, step, editor, nmax):
        super().__init__()
        self.step = step
        self.editor = editor
        self.old_nmax = copy.copy(step.n_step_max)
        self.new_nmax = nmax

    def redo(self):
        self.step.n_step_max = self.new_nmax

    def undo(self):
        self.editor.setValue(self.old_nmax)
        self.editor.repaint()
        self.step.n_step_max = self.old_nmax


class SetParaActive(QUndoCommand):
    """Set one parameter of an xstep inactive or active, depending on the state of box."""

    def __init__(self, step, para, box):
        super().__init__()
        self.step = step
        self.para = para
        self.box = box
        self.box_checked = self.box.isChecked()

    def redo(self):
        if self.box_checked:
            self.step.set_para_active(self.para)
        else:
            self.step.set_para_inactive(self.para)

        self.box.setChecked(self.box_checked)
        logging.info("SetParaActive: set para %s to active= %s.", self.para.name, self.box_checked)

    def undo(self):
        self.box_checked = not self.box_checked
        self.redo()
        self.box_checked = not self.box_checked


class SetParaPush(QUndoCommand):
    """Set one parameter of an xstep inactive or active, depending on the state of box."""

    def __init__(self, step, para, box):
        super().__init__()
        self.step = step
        self.para = para
        self.box = box
        self.box_checked = self.box.isChecked()

    def redo(self):
        if self.box_checked:
            self.step.set_para_to_push(self.para)
        else:
            self.step.remove_para_to_push(self.para)

        self.box.setChecked(self.box_checked)
        logging.info("SetParaPush: set para %s to push= %s.", self.para.name, self.box_checked)

    def undo(self):
        self.box_checked = not self.box_checked
        self.redo()
        self.box_checked = not self.box_checked


class StartExtraction(QUndoCommand):
    """Start an XStep's extraction routine, encapsulated in the a subclass instance QThread with the name worker_thread."""

    def __init__(self, extraction):
        super().__init__()
        self.extraction = extraction
        try:
            self.mcard_initial = copy.deepcopy(self.extraction.curr_xstep.mcard)
            self.paras_to_optimize_per_line_initial = copy.deepcopy(
                self.extraction.curr_xstep.paras_to_optimize_per_line
            )
        except AttributeError:
            self.mcard_initial = copy.deepcopy(
                self.extraction.mcard
            )  # to make it work with the single XStep GUI

    def redo(self):
        logging.info("StartExtractionCommand: started extraction.")
        self.extraction.extract()
        # self.worker_thread.start.emit()

    def undo(self):
        logging.info("StartExtractionCommand: reverted extraction.")
        try:
            self.extraction.curr_xstep.mcard = copy.deepcopy(self.mcard_initial)
            self.extraction.curr_xstep.paras_to_optimize_per_line = copy.deepcopy(
                self.paras_to_optimize_per_line_initial
            )
            self.extraction.curr_xstep.mcardChanged.emit()
        except AttributeError:  # why this?
            self.extraction.mcard = copy.deepcopy(self.mcard_initial)
            self.extraction.mcardChanged.emit()


class StopOptimizationCommand(QUndoCommand):
    """Start an XStep's extraction routine, encapsulated in the a subclass instance QThread with the name worker_thread."""

    def __init__(self, extraction):
        super().__init__()
        self.extraction = extraction

    def redo(self):
        logging.info("StopOptimizationCommand: stopped extraction.")
        self.extraction.stop()


class ReplotCommand(QUndoCommand):
    """Inform an xstep that he shall recalculate himself. Then update all plots."""

    def __init__(self, step):
        super().__init__()
        self.step = step

    def redo(self):
        self.replot()

    def undo(self):
        self.replot()

    def replot(self):
        self.step.finished.emit()


class UpdateBounds(QUndoCommand):
    """Tell the XStep object step to update its bounds according to user input in editor."""

    def __init__(self, step, editor, new_bounds):
        super().__init__()
        self.step = step
        self.editor = editor
        self.old_bounds = copy.deepcopy(step.x_bounds)
        self.new_bounds = copy.deepcopy(new_bounds)

    def redo(self):
        message = [
            r"(" + str(bounds.low) + "," + str(bounds.high) + r")," for bounds in self.new_bounds
        ]
        logging.info("SetPara: changed step %s bounds to %s.", self.step.name, message)
        self.editor.set_bounds(self.new_bounds)
        # self.step.x_bounds = self.new_bounds

    def undo(self):
        message = [
            r"(" + str(bounds.low) + "," + str(bounds.high) + r")," for bounds in self.old_bounds
        ]
        logging.info("SetPara: changed step %s bounds to %s.", self.step.name, message)
        # self.step.x_bounds = self.old_bounds # is done in xplot.BoundsWidget.set_bounds
        self.editor.set_bounds(self.old_bounds)
