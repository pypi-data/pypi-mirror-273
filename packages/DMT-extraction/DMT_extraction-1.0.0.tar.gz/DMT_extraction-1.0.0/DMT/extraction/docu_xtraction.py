""" Automatic documentation for the xtraction
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
from pathlib import Path
from pint.formatting import siunitx_format_unit
from DMT.config import COMMAND_TEX, DATA_CONFIG
from DMT.core import naming, unit_registry

# keep a soft dependency on PyLatex
try:
    from DMT.external.pylatex import (
        CommandRefRange,
        CommandRef,
        SubFile,
        CommandInput,
        CommandLabel,
        Tex,
    )
    from DMT.external.latex import build_tex
    from DMT.external.os import recursive_copy
    from pylatex.base_classes import Arguments
    from pylatex import Section, Subsection, Figure, Itemize, NoEscape, Tabular, Table
except ImportError:
    pass


class DocuXtraction(object):
    """This class implements routines for generating automated documentation of a Xtraction object.
    Xtraction objects represent a full parameter extraction flow.

    Parameters
    ----------
    extraction : DMT.extraction.extraction.Xtraction
        The Xtraction object for which the documentation shall be generated.
    gui_extraction : DMT.extraction.gui.XtractionGUI
        The GUI in which the Xtraction object is being visualized.
    dir_destination : str, Path-like object
        The destination path for writing the documentation to.
    """

    def __init__(
        self,
        extraction,
        gui_extraction=None,
        dir_destination=None,
        # dir_destination=DATA_CONFIG["directories"]["x_doc_dir"],
    ):
        self.extraction = extraction
        self.gui_extraction = gui_extraction

        if dir_destination is None:
            self.dir_destination = self.extraction.dirs["save_dir"] / "documentation"
        else:
            if isinstance(dir_destination, Path):
                self.dir_destination = dir_destination
            else:
                self.dir_destination = Path(dir_destination)

        self.doc = None
        self.modelcard = None
        self.lib = None
        self.technology = None

        self.additional_tex_files = []

    def copy_template(self, dir_destination=None, dir_source=None):
        """Copies the autodoc template in DMT_extraction/autodoc_template to the destination folder.

        Parameters
        ----------
        dir_destination : str, optional
            Path to the destination directory. Is set to self.dir_destination.
        dir_source : str, optional
            Path to the template. If None, the config directory 'autodoc' is used. Per default this points into the DMT package.
        """
        if dir_destination is not None:
            self.dir_destination = Path(dir_destination)

        if dir_source is None:
            dir_source = DATA_CONFIG["directories"]["autodoc"]

        self.dir_destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        recursive_copy(dir_source, self.dir_destination)

        try:
            # now rename _x_title and _author
            path_deckblatt = self.dir_destination / "content" / "deckblatt.tex"
            string_deckblatt = path_deckblatt.read_text(encoding="utf-8")

            string_deckblatt = string_deckblatt.replace("_author", DATA_CONFIG["user_name"])
            string_deckblatt = string_deckblatt.replace(
                "_x_title", str(self.extraction.technology.name).replace("_", r"\_")
            )
            string_deckblatt = string_deckblatt.replace(
                "_wafer", str(self.extraction.lib.wafer).replace("_", r"\_")
            )
            string_deckblatt = string_deckblatt.replace(
                "_date_TO", str(self.extraction.lib.date_tapeout).replace("_", r"\_")
            )
            string_deckblatt = string_deckblatt.replace(
                "_date_received", str(self.extraction.lib.date_received).replace("_", r"\_")
            )

            path_deckblatt.write_text(string_deckblatt, encoding="utf-8")
        except FileNotFoundError:
            pass  # when a different template is used, "deckblatt.tex" may not exists..

        try:
            # now rename _x_title and _author
            path_header = self.dir_destination / "base" / "header.tex"
            string_header = path_header.read_text(encoding="utf-8")

            string_header = string_header.replace("_author", DATA_CONFIG["user_name"])

            path_header.write_text(string_header, encoding="utf-8")
        except FileNotFoundError:
            pass  # when a different template is used, "deckblatt.tex" may not exists..

    def create_subfiles(self):
        """Creates the different Tex subfiles (https://ctan.org/pkg/subfiles) for the automated Xtraction tex documentation.
        For each XStep object in the Xtraction object:

        * create a subsection
        * print the extraction step description
        * print the plots related to the XStep
        * print the optimized modelcard parameters

        """
        steps = {}
        if self.gui_extraction is not None:
            root_item_xstep_views = self.gui_extraction.xtraction_view.treeView.model().rootItem
            ## for figure in self.plots...
            for child_item in root_item_xstep_views.childItems:
                if hasattr(child_item.step, "document_step") and not child_item.step.document_step:
                    continue  # do not document this steps

                # start a dict
                steps[child_item.step] = {
                    "fig_names": [],
                    "fig_captions": [],
                }

                # make sure all data is up to date
                child_item.step.calc_all(None, child_item.step.mcard, jac=False)

                # create the plots as pgfplots, and add the file_names and figure captions to the lists
                for plot_widget in [child_item.childItems[0].widget.plot] + child_item.childItems[
                    1
                ].widget.plots:
                    print_plot = False
                    if plot_widget.method.__name__ in child_item.step.prints_switched:
                        print_plot = child_item.step.prints_switched[plot_widget.method.__name__]
                    elif (
                        hasattr(plot_widget.method, "print_to_documentation")
                        and plot_widget.method.print_to_documentation
                    ):
                        print_plot = True

                    if print_plot:
                        plot_widget.refresh()
                        steps[child_item.step]["fig_names"].append(
                            plot_widget.plot.save_tikz(
                                self.dir_destination / "figures",
                                legend_location="upper right outer",
                                width="0.6\\textwidth",
                            )
                        )
                        steps[child_item.step]["fig_captions"].append(plot_widget.plot.name)
        else:
            for _index, step in self.extraction.iter_steps(
                pull=False, push=False, initial_guess=False
            ):
                if hasattr(step, "document_step") and not step.document_step:
                    continue  # do not document this steps

                # start a dict
                steps[step] = {
                    "fig_names": [],
                    "fig_captions": [],
                }

                # find all print_to_docu routines
                for attr in dir(step):
                    if hasattr(getattr(step, attr), "print_to_documentation") and getattr(
                        getattr(step, attr), "print_to_documentation"
                    ):
                        plot = getattr(step, attr)()  # get the plot and append to the lists
                        steps[step]["fig_names"].append(
                            plot.save_tikz(self.dir_destination / "figures")
                        )
                        steps[step]["fig_captions"].append(plot.name)

        # get other info for each step
        for x_step, docu_step in steps.items():
            docu_step["name"] = x_step.name
            docu_step["class"] = str(x_step.__class__)
            docu_step["bibtex"] = x_step.get_bibtex_entry()
            docu_step["description"] = x_step.get_description()
            if docu_step["description"] is None:
                docu_step["description"] = Tex()

            if len(x_step.op_definitions) > 1:
                docu_step["description"].append("\r")
                docu_step["description"].append(
                    NoEscape(
                        r"This step is performed on the measurement data defined by the following constraints:"
                    )
                )
                for op_def in x_step.op_definitions:
                    with docu_step["description"].create(Itemize()) as itemize:
                        for op_var, op_var_value in op_def.items():  # filter data
                            specifier = naming.get_specifier_from_string(
                                op_var, nodes=x_step.relevant_duts[0].nodes
                            )  # just be sure...
                            unit = specifier.get_pint_unit()
                            if isinstance(op_var_value, float) or isinstance(op_var_value, int):
                                val_unit = op_var_value * unit
                                itemize.add_item(
                                    NoEscape(f"${specifier.to_tex()}$ = {val_unit.to_compact():Lx}")
                                )

                            elif isinstance(op_var_value, tuple):
                                str_high = ""
                                if op_var_value[1] is not None:
                                    val_unit = op_var_value[1] * unit
                                    str_high = f"${specifier.to_tex()}$ \\textless {val_unit.to_compact():Lx}"

                                if op_var_value[0] is None:
                                    if str_high:
                                        itemize.add_item(NoEscape(str_high))
                                else:
                                    val_unit = op_var_value[0] * unit
                                    if str_high:
                                        itemize.add_item(
                                            NoEscape(
                                                f"{val_unit.to_compact():Lx} \\textless {str_high}"
                                            )
                                        )
                                    else:
                                        itemize.add_item(
                                            NoEscape(
                                                f"${specifier.to_tex()}$ \\textgreater {val_unit.to_compact():Lx}"
                                            )
                                        )

                            else:  # list or numpy array..
                                try:
                                    unit_string = siunitx_format_unit(unit)
                                except TypeError:
                                    unit_string = siunitx_format_unit(
                                        unit._units, unit_registry
                                    )  # new version has other interface
                                itemize.add_item(
                                    NoEscape(
                                        f"${specifier.to_tex()}"
                                        + r"$ = \SIlist{{{0:s}}}{{{1:s}}}".format(
                                            ";".join(f"{val:g}" for val in op_var_value),
                                            unit_string,
                                        )
                                    )
                                )

            paras_string = []
            if len(x_step.paras_to_optimize) > 0:
                self.append_parameter_glossaries(x_step.paras_to_optimize)

                for para in sorted(x_step.paras_to_optimize, key=lambda x: (x.group, x.name)):
                    if para.unit is not None and not para.unit.dimensionless:
                        val_unit = para.value * para.unit
                        val_unit = val_unit.to_compact()

                        max_unit = para.max * para.unit
                        max_unit = f"{max_unit.to(val_unit.units).magnitude:g}"

                        min_unit = para.min * para.unit
                        min_unit = f"{min_unit.to(val_unit.units).magnitude:g}"

                        try:
                            unit = siunitx_format_unit(val_unit.units)
                        except TypeError:
                            unit = siunitx_format_unit(
                                val_unit._units, unit_registry
                            )  # new version has other interface
                        # unit     = unit.replace('degC','celsius') #bug in pint, solved by custom siunitx unit (in default header) : \DeclareSIUnit[number-unit-product = {}] \degC{\degreeCelsius}
                        val_unit = f"{val_unit.magnitude:g}"
                    else:
                        val_unit = f"{para.value:g}"
                        unit = "-"
                        max_unit = f"{para.max:g}"
                        min_unit = f"{para.min:g}"

                    max_unit = max_unit.replace("inf", "{$\\infty$}")
                    min_unit = min_unit.replace("-inf", "{$-\\infty$}")

                    if para.name.startswith("_"):
                        para_name = f"{para:<12s}"
                    else:
                        # para_name = NoEscape(r"\gls{{{0:<12s}}}".format(para).replace('_','\_'))
                        para_name = f"{para:<12s}".replace("_", "\\_")

                    if unit != "-":
                        para_name = para_name + r"/\si{" + unit + "}"

                    paras_string.append(
                        [
                            NoEscape(para_name),
                            NoEscape(val_unit),
                            NoEscape(min_unit),
                            NoEscape(max_unit),
                        ]
                    )

            else:
                paras_string = None  # some steps don't have parameters

            docu_step["optimization_result"] = paras_string

        # create .tex file in documentations' content directory
        # create section for xtraction
        self.doc = SubFile()
        with self.doc.create(Section(self.extraction.name.replace("_", " "))):
            for x_step, docu_step in steps.items():
                with self.doc.create(Subsection(docu_step["name"].replace("_", " "))):
                    # add fig: before figures to use cref tex package for referencing
                    fig_names = [f"fig:{fig_name}" for fig_name in docu_step["fig_names"]]
                    fig_captions = docu_step["fig_captions"]
                    if docu_step["description"] is not None:
                        self.doc.append(docu_step["description"])
                        if not len(fig_names) == 0:
                            self.doc.append(
                                NoEscape(
                                    r"The extraction method described above has been applied to measured data as shown in\enspace"
                                )
                            )
                            if len(fig_names) > 1:
                                self.doc.append(
                                    CommandRefRange(
                                        arguments=Arguments(fig_names[0], fig_names[-1])
                                    )
                                )
                            else:
                                self.doc.append(CommandRef(arguments=Arguments(fig_names[0])))

                        self.doc.append(".")

                    # create figures and put them in FloatBarriers
                    for fig_name, fig_caption in zip(fig_names, fig_captions):
                        self.doc.append(NoEscape(r"\FloatBarrier "))
                        with self.doc.create(Figure(position="ht!")) as _plot:
                            _plot.append(NoEscape(r"\centering"))
                            _plot.append(NoEscape(r"\setlength\figurewidth{\textwidth}"))
                            _plot.append(
                                NoEscape(
                                    r"\tikzsetnextfilename{"
                                    + fig_name[4:-4].replace(" ", "_")
                                    + r"_}"
                                )
                            )
                            _plot.append(
                                CommandInput(
                                    arguments=Arguments(
                                        '"' + "/".join(["figures", fig_name[4:]]) + '"'
                                    )
                                )
                            )  # the :4 removes :fig, since the figures have been saved without that
                            _plot.add_caption(NoEscape(fig_caption))
                            _plot.append(CommandLabel(arguments=Arguments(fig_name)))

                        self.doc.append(NoEscape(r"\FloatBarrier "))

                    # print a small table with the optimization results
                    if docu_step["optimization_result"] is not None:
                        tab_name = f"tab:{x_step.name:s}_params"
                        self.doc.append(
                            "The extracted model parameters with the corresponding optimization boundaries are summarized in "
                        )
                        self.doc.append(CommandRef(arguments=Arguments(tab_name)))
                        self.doc.append(".\r")
                        with self.doc.create(Table(position="ht!")) as tab:
                            tab.append(NoEscape(r"\centering"))
                            with tab.create(
                                Tabular(r"l S S S", booktabs=True, width=4)
                            ) as data_table:  # pylatex does not count s S columns from siunitx
                                data_table.add_row(
                                    [
                                        "parameter",
                                        NoEscape("{value}"),
                                        NoEscape("{minimum}"),
                                        NoEscape("{maximum}"),
                                    ]
                                )
                                data_table.add_hline()

                                for para_string in docu_step["optimization_result"]:
                                    try:
                                        data_table.add_row(para_string)
                                    except:
                                        raise IOError(
                                            "DMT -> create_xdoc: step "
                                            + print(x_step.__class__)
                                            + " error while writing table. Number of cells did not match table width."
                                        )

                            tab.add_caption(
                                f"Resulting parameters of the extraction step {x_step.name:s}."
                            )
                            tab.append(CommandLabel(arguments=Arguments(tab_name)))

                        self.doc.append(NoEscape(r"\FloatBarrier"))

        # after the steps, add them to the main file:
        path_documentation = self.dir_destination / "documentation.tex"
        string_main = path_documentation.read_text(encoding="utf-8")

        # now add additional information and place them in the main file:

        # place SubFile of Extraction in the main documentation.tex file
        subfile_string = f'\\subfile{{"documentation_{self.extraction.name:s}"}}\n'
        if not subfile_string in string_main:
            string_main = string_main.replace("%_NEXT", subfile_string + "    %_NEXT")

        # print the library. Always overwrite the existing one. This one needs to be replaced in the main file.
        self.lib = SubFile()
        self.lib.append(self.extraction.lib.toTex())  # add Tex as into SubFile

        subfile_string = r'\subfile{"lib"}'
        if not subfile_string in string_main:
            string_main = string_main.replace("%_LIB", subfile_string)

        # try to print the technology Always overwrite the existing one. This one needs to be replaced in the main file.
        self.technology = SubFile()
        try:
            self.technology.append(
                self.extraction.technology.print_tex(
                    self.extraction.lib.dut_ref, self.extraction.mcard
                )
            )

            # if this was successfull: place subfile for technology in the main file
            subfile_string = r'\subfile{"technology"}'
            if not subfile_string in string_main:
                string_main = string_main.replace("%_TECH", subfile_string)

            # is there a separate tech file (for example a separate TRADICA input file)?
            if (
                hasattr(self.extraction.technology, "docu_inp_file_content")
                and self.extraction.technology.docu_inp_file_content is not None
            ):
                (self.dir_destination / self.extraction.technology.docu_inp_file_name).write_text(
                    self.extraction.technology.docu_inp_file_content, encoding="utf-8"
                )

            # print the modelcard lib
            self.extraction.technology.create_mcard_library(
                self.extraction.lib,
                self.extraction.mcard,
                self.dir_destination / "HICUM.lib",
                # dut_type=DutType.npn
            )

        except AttributeError:  # old technologies may not have a print_tex...
            self.technology = None

        # now write the changed string_main
        path_documentation.write_text(string_main, encoding="utf-8")

        # print the modelcard. Always overwrite the existing one, modelcard is always present in main file.
        self.modelcard = SubFile()
        self.modelcard.append(self.extraction.mcard.print_tex())

        # put all citations into bibtex file
        path_bib = self.dir_destination / "bib.bib"
        string_bib = path_bib.read_text(encoding="utf-8")

        bibtex_entries = list(
            set(
                [
                    docu_step["bibtex"]
                    for x_step, docu_step in steps.items()
                    if docu_step["bibtex"] is not None
                ]
            )
        )
        if self.technology is not None and hasattr(self.extraction.technology, "get_bib_entries"):
            bibtex_entries.append(self.extraction.technology.get_bib_entries())

        for entry in bibtex_entries:
            if not entry in string_bib:
                string_bib = string_bib.replace("_next", entry + "\n_next")

        path_bib.write_text(string_bib, encoding="utf-8")

    def append_parameter_glossaries(self, parameters):
        """Append model parameters to the parameter glossary defined in parameters.tex, if they are not already present

        Parameters
        ----------
        parameters : McParameterCollection, [McParameter]
            A list of McParameter objects or an McParameterCollection which shall be appended to parameters.tex
        """
        path_parameters = self.dir_destination / "base" / "parameters.tex"
        str_parameters = path_parameters.read_text()

        for parameter in parameters:
            if parameter.name.startswith("_"):
                continue

            try:
                desc = parameter.description
            except AttributeError:
                desc = ""
            entry = (
                ""
                + f"\\newglossaryentry{{{parameter.name:s}}}\n"
                + "{\n"
                + f"name={{{parameter.name:s}}},\n"
                + f"description={{{desc:s}}},\n"
                + f"sort={{{parameter.group:s}}}, type=parameterlist\n"
                + "}\n"
            )

            if entry not in str_parameters:
                str_parameters += entry

        path_parameters.write_text(str_parameters)

    def append(self, content, file_name, mark=None, mark_in_file="documentation.tex"):
        """Adds the content to a file  and also start the build chain for self.build.

        Ideally content is a

        Parameters
        ----------
        content : :class:`~DMT.external.pylatex.SubFile` or string
        file_name : str
        mark : str, optional
            If given this string is replaced with file_name in mark_in_file.
        mark_in_file : str
            This file in the destination folder contains the "mark" string, which is replaced with "content".

        """
        if mark is not None:
            path_file = self.dir_destination / mark_in_file
            string_file = path_file.read_text(encoding="utf-8")
            string_file = string_file.replace(mark, file_name)
            path_file.write_text(string_file, encoding="utf-8")

        if not isinstance(content, SubFile):
            temp = content
            content = SubFile()
            content.append(temp)

        self.additional_tex_files.append((file_name, content))

    def generate_tex(self):
        """Write all the tex files but do not build them."""
        self.doc.generate_tex(str(self.dir_destination / ("documentation_" + self.extraction.name)))
        self.modelcard.generate_tex(str(self.dir_destination / "modelcard"))
        self.lib.generate_tex(str(self.dir_destination / "lib"))
        for i_plot, plot in enumerate(self.extraction.lib.plots):
            _name = plot.save_tikz(
                self.dir_destination / "figures",
                file_name=f"lib_plot_{i_plot:d}",
                legend_location="upper right outer",
                width="0.6\\textwidth",
            )

        if self.technology is not None:
            self.technology.generate_tex(str(self.dir_destination / "technology"))

        for file_name, additional_subfile in self.additional_tex_files:
            additional_subfile.generate_tex(str(self.dir_destination / file_name))

    def build(self):
        """Build each of the TEX files into a PDF."""
        compiler = COMMAND_TEX

        try:
            self.doc.generate_pdf(
                self.dir_destination / ("documentation_" + self.extraction.name), compiler=compiler
            )
        except (OSError, IOError):
            print(
                "DMT -> autodoc: failed to generate documentation_" + self.extraction.name + ".pdf"
            )

        try:
            self.modelcard.generate_pdf(self.dir_destination / "modelcard", compiler=compiler)
        except (OSError, IOError):
            print("DMT -> autodoc: failed to generate modelcard.pdf")

        try:
            self.lib.generate_pdf(self.dir_destination / "lib", compiler=compiler)
        except (OSError, IOError):
            print("DMT -> autodoc: failed to generate lib.pdf")

        if self.technology is not None:
            try:
                self.technology.generate_pdf(self.dir_destination / "technology", compiler=compiler)
            except (OSError, IOError):
                print("DMT -> autodoc: failed to generate technology.pdf")

        for file_name, additional_subfile in self.additional_tex_files:
            try:
                additional_subfile.generate_pdf(self.dir_destination / file_name, compiler=compiler)
            except (OSError, IOError):
                print("DMT -> autodoc: failed to generate " + file_name + ".pdf")

        try:
            build_tex(self.dir_destination / "documentation.tex", additional_compiler=compiler)
        except (OSError, IOError):
            print("DMT -> autodoc: failed to generate documentation.pdf")
