""" Xtraction is a improved list of xsteps.

By using this one can change between gui and script and also exchange the order of steps including boundaries of extraction area and parameters

Offers:

* List of steps, which all work on the same DutViews for reference and extraction
* Modelcard management using a global and local modelcards and push_modelcard/pull_modelcard.
* Saving and loading of whole extractions
* Access point for :class:`~DMT.extraction.xtraction_gui.XtractionGui`

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
from typing import Literal, Union
import datetime
import copy
import warnings
from typing import List
from pathlib import Path
from qtpy.QtCore import QObject, Signal
import _pickle as cpickle
from DMT.core import DutLib, MCard, Technology
from DMT.extraction import XStep


class Xtraction(QObject):
    """Xtraction objects are a container for XStep objects and can be used to define a model parameter extraction flow.
    Xtraction objects can be displayed in the DMT.extraction.gui and provide routines for plotting and documenting a
    parameter extraction.

    Parameters
    ----------
    mcard                   : :class:`~DMT.core.mcard.MCard`
        This MCard needs to hold all parameters (incl. boundaries) of the model and is used for simulations or model equation calculations.
    save_dir                : str
        Path to folder where all databases are saved.
    dut_ref :               :class:`~DMT.core.dut_view.DutView`
        This device needs to hold relevant reference data in one or more DataFrames.
    dut_ext                 : :class:`~DMT.core.dut_view.DutCircuit`
        The extraction Dut, whose model parameters shall be extracted; needed for model circuit simulations.

    Attributes
    ----------
    mcard                   : :class:`~DMT.core.mcard.MCard`
        This MCard needs to hold all parameters (incl. boundaries) of the model and is used for simulations or model equation calculations.
    dirs                    : dict{key: str}
        Path to folders where all databases are saved.
    lib :               :class:`~DMT.core.dut_lib.DutLib`
        This library holds all devices that are relevant for the extraction. This lib is passed to all xsteps.
    available_xsteps          : list[:class:`~DMT.extraction.x_step.XStep`]
        List of xsteps for this extraction.
    curr_xstep              : :class:`~DMT.extraction.x_step.XStep`
        Current active xstep. All methods work with this xstep.

    autosave_pushed_modelcards : {"no","yes","code", "code_compressed"}, optional
        If "yes", saves each pushed modelcard with the timestamp as filename in the xtraction folder.
        If "code", it turns on code saving in the modelcards to save. If "code_compressed", the code is compressed to save.

    """

    stepChanged = Signal()
    mcardChanged = Signal()

    def __init__(
        self,
        name: str,
        mcard: MCard,
        save_dir: Union[str, Path],
        lib: DutLib,
        autosave_pushed_modelcards: Literal["no", "yes", "code", "code_compressed"] = "no",
        technology: Technology = None,
    ):
        QObject.__init__(self)
        self.name = name.replace(" ", "_")

        self.lib = lib
        self.mcard = copy.deepcopy(mcard)  # global modelcard

        if isinstance(save_dir, str):
            save_dir = Path(save_dir).resolve()
        else:
            save_dir = save_dir.resolve()

        self.dirs = {
            "save_dir": save_dir,
            "sim_dir": save_dir / "sim",
            "circuit_database_dir": save_dir / "sim_db",
            "mcard_dir": save_dir / "modelcards",
            "lib_dir": self.lib.save_dir,
        }
        for _key, directory in self.dirs.items():
            directory.mkdir(parents=True, exist_ok=True)

        self._technology = technology

        # controls flow
        self.available_xsteps: List[XStep] = []
        self.curr_xstep = None  # pointer to the currently loaded xstep

        # for defining global plots
        self.global_plots = []

        autosave_options = ["yes", "code", "code_compressed", "no"]
        if autosave_pushed_modelcards in autosave_options:
            self.autosave_pushed_modelcards = autosave_pushed_modelcards
        else:
            raise IOError(
                'DMT->Xtraction: Autosave_pushed_modelcards has to be one of the following:\n"'
                + '", "'.join(autosave_options)
                + '"\nGiven was: '
                + str(autosave_pushed_modelcards)
            )

    # bug catcher => leave here only as long as Pandas problems with non unique cols persists...
    def check_dims(self):
        for key in self.lib.dut_ref.data.keys():
            for col in self.lib.dut_ref.data[key].columns:
                shape = self.lib.dut_ref.data[key][col].shape
                if len(shape) > 1:
                    if shape[1] == 2:
                        raise IOError

    def __re_init__(self):
        """Workaround for saving and loading QSignals."""
        QObject.__init__(self)

    @property
    def global_plot_methods(self):
        methods = []
        # for step in self.available_xsteps:
        #     for method in step.global_plot_methods:
        #         methods.append(method)

        return methods

    @property
    def technology(self):
        """Technology of this xtraction.

        Returns
        -------
        :class:`~DMT.core.technology.Technology`
            Directly the set technology
        """
        return self._technology

    @technology.setter
    def technology(self, tech_new):
        """Set a technology for this extraction that holds necessary technology-specific scaling and extraction routines.

        Additionally sets this new tech to all available xsteps in this xtraction

        Parameters
        ----------
        tech_new : :class:`~DMT.core.technology.Technology`
        """
        for step in self.available_xsteps:
            step.technology = tech_new
        self._technology = tech_new

    def adjust_xstep(self, xstep: XStep):
        """Sets the duts from xtraction to the given step

        Parameters
        ----------
        xstep : list[:class:`~DMT.extraction.x_step.XStep`]
        """
        # Implementation moved inside xstep to allow overwriting
        warnings.warn(
            "DMT.xtraction.adjust_xstep: Implementation moved inside xstep to allow overwriting.",
            category=DeprecationWarning,
        )

        xstep.lib = self.lib
        xstep.technology = self.technology

        xstep.circuit_sim_dir = self.dirs["sim_dir"]
        xstep.circuit_database_dir = self.dirs["circuit_database_dir"]

        xstep.__re_init__()

    def add_xstep(self, xstep: XStep):
        """Adds a step to the extraction flow.

        Parameters
        ----------
        xstep : list[:class:`~DMT.extraction.x_step.XStep`]
        """
        # self.check_dims()
        if xstep.name in [step.name for step in self.available_xsteps]:
            raise IOError(
                "The names of the XSteps must be unique! The name '"
                + xstep.name
                + "' was already taken."
            )

        # Implementation moved inside xstep to allow overwriting
        xstep.add_to_xtraction(self)

        xstep.init()
        self.available_xsteps.append(xstep)
        if self.curr_xstep is None:
            self.curr_xstep = self.available_xsteps[0]
        # self.check_dims()

    def activate_xstep(self, step_name):
        """Sets self.curr_xstep to the step with the name step_name.

        Parameters
        ----------
        step_name : str
            Name of the step to set.

        """
        if isinstance(step_name, XStep):
            step_name = step_name.name

        for step in self.available_xsteps:
            if step.name == step_name:
                self.curr_xstep = step
                self.stepChanged.emit()
                return

        raise IOError("The XStep with the name " + step_name + " was not found!")

    def next_xstep(self):
        """Places the next xstep on curr_xstep."""
        # find current:
        i_step = (
            len(self.available_xsteps) - 1
        )  # in case aviable_xsteps is empty nothing is activated
        for i_step, step in enumerate(self.available_xsteps):
            if step.name == self.curr_xstep.name:
                break

        if i_step != len(self.available_xsteps) - 1:
            self.activate_xstep(self.available_xsteps[i_step + 1].name)

    def step(self, step, bounds):
        """perform an extraction of XStep step using bounds. Before, pull global Mcard, then push local Mcard."""
        self.activate_xstep(step)
        self.pull_global_mcard()
        step.x_bounds = [bounds]
        step.extract()
        self.push_local_mcard()

    def previous_xstep(self):
        """Places the previous xstep on curr_xstep."""
        # find current:
        i_step = 0  # in case aviable_xsteps is empty nothing is activated
        for i_step, step in enumerate(self.available_xsteps):
            if step.name == self.curr_xstep.name:
                break

        if i_step != 0:
            self.activate_xstep(self.available_xsteps[i_step - 1].name)

    def pull_global_mcard(self, initial_guess=False, mcard=None):
        """Set all parameters that exist in both self.mcard and self.curren_xstep.mcard to self.current_xstep.mcard"""
        if mcard is None:
            mcard = self.mcard

        for para in mcard:
            if para.name in self.curr_xstep.mcard.name:
                self.curr_xstep.mcard.set(para)

        # now also the initial guesses from the step are overwritten... set them again
        if initial_guess:
            self.curr_xstep.set_initial_guess(self.curr_xstep.data_reference)

        self.curr_xstep.mcardChanged.emit()

    def push_local_mcard(self, mcard=None):
        """Set the parameters in my mcard according to the paramaters_to_push attribute of the current_xstep. And saves it to the local mcard folder with the time as name."""
        if mcard is None:
            mcard = self.curr_xstep.mcard

        for para in self.curr_xstep.paras_to_push:
            para = mcard.get(para)  # get the value from the mcard. For safety.
            if para.name in self.mcard.name:
                self.mcard.set(para)
            else:
                self.mcard.add(para)

        if self.autosave_pushed_modelcards == "yes":
            self.mcard.dump_json(
                self.dirs["mcard_dir"]
                / (datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"),
                save_va_code=False,
                compress_va_code=False,
            )
        elif self.autosave_pushed_modelcards == "code":
            self.mcard.dump_json(
                self.dirs["mcard_dir"]
                / (datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"),
                save_va_code=True,
                compress_va_code=False,
            )
        elif self.autosave_pushed_modelcards == "code_compressed":
            self.mcard.dump_json(
                self.dirs["mcard_dir"]
                / (datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".json"),
                save_va_code=True,
                compress_va_code=True,
            )

        self.mcardChanged.emit()

    def save(self):
        """Saves the current extraction status in the given directory. The extraction status includes the steps, the modelcard and the current duts."""
        for dir_name, dir_path in self.dirs.items():
            dir_path = Path(dir_path)
            dir_path.mkdir(parents=True, exist_ok=True)
            self.dirs[dir_name] = dir_path

        self.lib.save()
        # save the mcard as separete file to allow loading with other extractions
        self.mcard.dump_json(self.dirs["save_dir"] / "mcard.json")
        with (self.dirs["save_dir"] / "extraction.p").open(mode="wb") as handle:
            cpickle.dump(self, handle)

    def __getstate__(self):
        """Return state values to be pickled. Implemented according `to <https://www.ibm.com/developerworks/library/l-pypers/index.html>`_ .
        Notes
        -----
        ..todo:
            iterate through all properties and throw away the HDFStore objects.
        """
        d = copy.copy(self.__dict__)

        list_to_del = ["lib", "stepChanged", "mcardChanged", "objectNameChanged", "destroyed"]

        for to_del in list_to_del:
            if to_del in d:
                del d[to_del]
        return d

    @staticmethod
    def load(path_extraction):
        """Static class method. Loads a DutView object from a pickle file with full path save_dir.

        Parameters
        ----------
        path_extraction  :  str
            Path to the pickled Xtraction object that shall be loaded.

        Returns
        -------
        :class:`~DMT.extraction.xtraction.Xtraction`
            Loaded object from the pickle file.
        """
        # pylint: disable=unused-variable

        with open(path_extraction, "rb") as handle:
            extraction = cpickle.load(handle)

        for key, path in extraction.dirs:  # path conversion
            extraction.dirs[key] = Path(path)

        extraction.lib = DutLib.load(extraction.dirs["lib_dir"] / "dut_lib.p")

        extraction.__re_init__()
        for step in extraction.available_xsteps:
            step.add_to_xtraction(extraction)

        return extraction

    def extract(self):
        """Ask the current xstep to optimize itself."""
        try:
            self.curr_xstep.extract()
        except Exception as err:
            print("An error occurred: " + str(err.__class__.__name__) + ":" + str(err.args))

    def stop(self):
        self.curr_xstep.stopped = True

    def set_technology(self, technology):
        """Set a technology for this extraction that holds necessary technology-specific scaling and extraction routines.

        Just use the setter propery. This method is deprecated!
        """
        self.technology = technology

    def iter_steps(self, pull=True, push=True, initial_guess=False):
        """Get an step iterator

        use with::

            for i_step, step in xtraction.iter_steps(pull=True, push=False, initial_guess=[0, 4])
                step.extract()

        Parameters
        ----------
        pull : bool or list, optional
            Is done before the current step is returned from the iterator.
            In case list is given, it must be a list of numbers in which pull is used.
        push : bool or list, optional
            Is done before the next step is returned from the iterator.
            In case list is given, it must be a list of numbers in which push is used.
        initial_guess : bool or list, optional
            Is done before the current step is returned from the iterator.
            In case list is given, it must be a list of numbers in which initial guess is used.

        Returns
        -------
        iterator : :class:`~DMT.core.xtraction.IterXtraction`
        """
        return IterXtraction(self, pull, push, initial_guess)


class IterXtraction(object):
    """Xtraction steps iterator

    use with::

        for i_step, step in xtraction.iter_steps(pull=True, push=False, initial_guess=[0, 4])
            step.extract()

    Parameters
    ----------
    pull : bool or list, optional
        Is done before the current step is returned from the iterator.
            In case list is given, it must be a list of numbers in which pull is used.
        push : bool or list, optional
            Is done before the next step is returned from the iterator.
            In case list is given, it must be a list of numbers in which push is used.
        initial_guess : bool or list, optional
            Is done before the current step is returned from the iterator.
            In case list is given, it must be a list of numbers in which initial guess is used.
    """

    def __init__(self, xtraction, pull, push, initial_guess):
        self.index = 0  # start at 0
        self.xtraction = xtraction  # reference to xtraction

        if isinstance(pull, list):
            self.pull = pull
        elif isinstance(pull, bool):
            if pull:
                # per default the first step is not in the pull list
                self.pull = range(1, len(self) + 1)  # always a list
            else:
                self.pull = []
        else:
            raise TypeError()

        if isinstance(push, list):
            self.push = push
        elif isinstance(push, bool):
            if push:
                self.push = range(0, len(self) + 1)  # always a list
            else:
                self.push = []
        else:
            raise TypeError()

        if isinstance(initial_guess, list):
            self.initial_guess = initial_guess
        elif isinstance(initial_guess, bool):
            if initial_guess:
                self.initial_guess = range(0, len(self) + 1)  # always a list
            else:
                self.initial_guess = []
        else:
            raise TypeError()

    def __len__(self):
        """Convenience to so len(iterator) can be used.."""
        return len(self.xtraction.available_xsteps)

    def __iter__(self):
        """Here self is returned -> this class itself is an iterator."""
        return self

    def __next__(self):
        """This routine is magic and sets the iteration behaviour.

        We want to replace:

        ```
            for _step in xtraction.available_xsteps:
                xtraction.pull_global_mcard()  # start of loop
                xtraction.curr_xstep.extract() # user action
                xtraction.push_local_mcard()  # end of loop
                xtraction.next_xstep() # manual looping
        ```

        with

        ```
            for i_step, step in xtraction.iter_steps(pull=True, push=True, initial_guess=True)
                step.extract() # user action
        ```

        """
        # first we need to consider the end of the original loop -> after user actions
        # this is the push command in the original loop.
        # push ?
        if self.index in self.push:
            # if index in push list
            # and not in the first iteration (per default). This would be before any actions done by the user.
            self.xtraction.push_local_mcard()

        if self.index == len(self):
            # end reached
            raise StopIteration

        # get and activate the step
        step = self.xtraction.available_xsteps[self.index]
        self.xtraction.activate_xstep(step.name)
        # afterwards the actions before a user defined actions are done.
        # pull ?
        if self.index in self.pull:
            # if index in pull list
            self.xtraction.pull_global_mcard()

        # initial guess ?
        if self.index in self.initial_guess:
            # if index in initial guess list
            step.set_initial_guess(step.data_reference)

        self.index += 1  # increase index to keep the correct reference
        return self.index - 1, step
