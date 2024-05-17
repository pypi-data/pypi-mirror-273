"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import dataclasses as dtcl
import pprint as pprt
import typing as h
from pathlib import Path as path_t

import PyQt6.QtWidgets as wdgt
from logger_36 import AddGenericHandler
from pyvispr import __version__
from pyvispr.config.type import config_t
from pyvispr.constant.app import APP_NAME
from pyvispr.constant.config import (
    PATH_LAST_LOADING_FOLDER,
    PATH_LAST_SAVING_AS_SCRIPT_FOLDER,
    PATH_LAST_SAVING_FOLDER,
    PATH_SECTION,
)
from pyvispr.flow.visual.whiteboard import whiteboard_t
from pyvispr.interface.storage.loading import LoadWorkflow
from pyvispr.interface.storage.stowing import SaveWorkflow, SaveWorkflowAsScript
from pyvispr.interface.window.widget.list.node import node_list_wgt_t
from pyvispr.interface.window.widget.menu import AddEntryToMenu
from pyvispr.runtime.backend import SCREEN_BACKEND
from pyvispr.runtime.catalog import NODE_CATALOG


@dtcl.dataclass(slots=True, repr=False, eq=False)
class runner_wdw_t(wdgt.QMainWindow):
    config: config_t
    node_list: node_list_wgt_t
    whiteboard: whiteboard_t
    load_recent: wdgt.QMenu = dtcl.field(init=False)
    recent_list: node_list_wgt_t = dtcl.field(init=False)
    most_used_list: node_list_wgt_t = dtcl.field(init=False)
    tabs: wdgt.QTabWidget = dtcl.field(init=False)
    doc_area: wdgt.QTextEdit = dtcl.field(init=False)
    status_bar: wdgt.QStatusBar = dtcl.field(init=False)
    _ref_keeper: list = dtcl.field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """"""
        wdgt.QMainWindow.__init__(self)
        self.setWindowTitle(APP_NAME)
        self._AddMenuBar()
        self.status_bar = self.statusBar()

        self.recent_list = node_list_wgt_t(
            element_name="Recent",
            source=self.config.recent_nodes,
            should_be_sorted=False,
        )
        self.most_used_list = node_list_wgt_t(
            element_name="Most Used",
            source=self.config.most_used_nodes,
            should_be_sorted=False,
        )

        log_area = wdgt.QTextEdit()
        log_area.setReadOnly(True)
        log_area.setLineWrapMode(wdgt.QTextEdit.LineWrapMode.NoWrap)
        AddGenericHandler(log_area.append, supports_html=True)

        self.doc_area = wdgt.QTextEdit()
        self.doc_area.setReadOnly(True)

        self.tabs = wdgt.QTabWidget()
        self.tabs.addTab(self.whiteboard, "Workflow")
        self.tabs.addTab(log_area, "Messages")
        self.tabs.addTab(self.doc_area, "Documentation")
        self.tabs.setStyleSheet("QTabWidget::tab-bar {alignment: center;}")

        layout = wdgt.QGridLayout()
        layout.addWidget(self.node_list.filter_wgt, 0, 0)
        layout.addWidget(self.node_list, 1, 0, 3, 1)
        layout.addWidget(
            wdgt.QLabel('<span style="font-weight:bold; color:blue">Recent</span>'),
            0,
            1,
        )
        layout.addWidget(self.recent_list, 1, 1)
        layout.addWidget(
            wdgt.QLabel('<span style="font-weight:bold; color:blue">Most Used</span>'),
            2,
            1,
        )
        layout.addWidget(self.most_used_list, 3, 1)
        layout.addWidget(self.tabs, 0, 2, 4, 1)

        central = wdgt.QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        for node_list in (self.node_list, self.recent_list, self.most_used_list):
            SCREEN_BACKEND.CreateMessageCanal(
                node_list, "itemClicked", self.AcknowledgeNodeSelected
            )

    @classmethod
    def New(cls) -> runner_wdw_t:
        """"""
        node_list = node_list_wgt_t(element_name="Nodes")
        whiteboard = whiteboard_t()

        return cls(config=config_t(), node_list=node_list, whiteboard=whiteboard)

    @staticmethod
    def Instance() -> runner_wdw_t:
        """"""
        for widget in wdgt.QApplication.topLevelWidgets():
            if isinstance(widget, runner_wdw_t):
                return widget

        raise RuntimeError(f"No runner window currently open.")

    def _AddMenuBar(self) -> None:
        """"""
        menu_bar = self.menuBar()

        _ = _AddMenu(
            "py&Vispr",
            (
                ("About", self.OpenAboutDialog),
                ("Configure", self.OpenConfiguration),
                None,
                ("&Quit", self.Close, {"shortcut": "Ctrl+Q"}),
            ),
            menu_bar,
            self,
        )

        self.load_recent = _AddMenu(
            "Load Recent...",
            self._LoadRecentEntries(),
            None,
            self,
        )
        reset_menu = _AddMenu(
            "Reset...",
            (
                (
                    "Now",
                    self.whiteboard.InvalidateWorkflow,
                ),
            ),
            None,
            self,
        )
        clear_menu = _AddMenu(
            "Clear...",
            (("Now", self.whiteboard.Clear),),
            None,
            self,
        )
        self._ref_keeper.extend((reset_menu, clear_menu))
        _ = _AddMenu(
            "&Workflow",
            (
                ("About", self.OpenAboutWorkflowDialog),
                None,
                ("&Run", self.whiteboard.RunWorkflow, {"shortcut": "Ctrl+R"}),
                None,
                (
                    "&Save",
                    lambda *_, **__: self.LoadOrSaveWorkflow("save"),
                    {"shortcut": "Ctrl+S"},
                ),
                (
                    "L&oad",
                    lambda *_, **__: self.LoadOrSaveWorkflow("load"),
                    {"shortcut": "Ctrl+O"},
                ),
                self.load_recent,
                None,
                (
                    "Save As Script",
                    lambda *_, **__: self.LoadOrSaveWorkflow("save as script"),
                ),
                None,
                reset_menu,
                clear_menu,
            ),
            menu_bar,
            self,
        )

        _ = _AddMenu(
            "&View",
            (
                ("Toggle Grid", self.whiteboard.ToggleGridVisibility),
                ("Align on Grid", self.whiteboard.AlignGraphOnGrid),
            ),
            menu_bar,
            self,
        )

        _ = _AddMenu(
            "&Catalog",
            (("Refresh", self.node_list.Reload),),
            menu_bar,
            self,
        )

    def _LoadRecentEntries(
        self,
    ) -> tuple[tuple[str, h.Callable[..., None] | None], ...]:
        """"""
        recent_s = self.config.recent_flows
        if recent_s.__len__() > 0:
            return tuple(
                (
                    str(_pth),
                    lambda *_, **__: self.LoadOrSaveWorkflow(
                        "load recent", recent=_pth
                    ),
                )
                for _pth in recent_s
            )

        return (("No Recent Workflows", None),)

    def AcknowledgeNodeSelected(self, item: wdgt.QListWidgetItem, /) -> None:
        """"""
        name = item.text()
        which = self.tabs.currentIndex()
        if which == 0:
            self.AddNode(name)
        elif which == 2:
            self.ShowDocumentation(name)

    def ShowDocumentation(self, name: str, /) -> None:
        """"""
        try:
            description = NODE_CATALOG.NodeDescription(name)
        except ValueError:
            description = None

        self.doc_area.clear()
        if description is None:
            self.doc_area.setText(f"Invalid Node: {name}.")
        else:
            description.Activate()
            if (documentation := description.documentation).__len__() == 0:
                documentation = "No documentation."
            self.doc_area.setText(documentation)

    def AddNode(self, name: str, /) -> None:
        """"""
        self.whiteboard.AddNode(name)

        self.config.UpdateRecentNodes(name)
        self.recent_list.source = self.config.recent_nodes
        self.recent_list.Reload()

        self.config.UpdateMostUsedNodes(name)
        self.most_used_list.source = self.config.most_used_nodes
        self.most_used_list.Reload()

    def LoadOrSaveWorkflow(
        self,
        operation: h.Literal[
            "load", "load recent", "save", "save as", "save as script"
        ],
        /,
        *,
        recent: path_t | None = None,
    ) -> None:
        """"""
        if operation == "load":
            filename = LoadWorkflow(
                self, self.whiteboard, self.config.last_loading_folder
            )
            if filename is not None:
                self.config.UpdateRecentFlows(filename)
                self.config[PATH_SECTION][PATH_LAST_LOADING_FOLDER] = filename.parent
                self.load_recent.clear()
                _AddEntries(
                    self.load_recent,
                    self._LoadRecentEntries(),
                    self,
                )
        elif operation == "load recent":
            filename = LoadWorkflow(self, self.whiteboard, recent)
            if filename is not None:
                self.config.UpdateRecentFlows(filename)
                self.config[PATH_SECTION][PATH_LAST_LOADING_FOLDER] = filename.parent
                self.load_recent.clear()
                _AddEntries(
                    self.load_recent,
                    self._LoadRecentEntries(),
                    self,
                )
        elif operation == "save":
            # TODO: Create 2 modes: unsaved and saved. When unsaved, save for the first time,
            #     then switch to saved mode, and save in same file with overwrite from now on,
            #     like any text editor. Save as script does not switch to saved mode.
            # TODO: In accordance with modification above, create a save_as menu first (unsaved
            #     mode), then create a save menu for overwrite and leave the save_as menu.
            # TODO: When closing, if unsaved, ask for confirmation.
            filename = SaveWorkflow(
                self, self.whiteboard.graph, self.config.last_saving_folder
            )
            if filename is not None:
                self.config.UpdateRecentFlows(filename)
                # TODO: Update config w/o using constants, by adding method, or w/ a better way.
                self.config[PATH_SECTION][PATH_LAST_SAVING_FOLDER] = filename.parent
                self.load_recent.clear()
                _AddEntries(
                    self.load_recent,
                    self._LoadRecentEntries(),
                    self,
                )
        elif operation == "save as":
            pass
        elif operation == "save as script":
            filename = SaveWorkflowAsScript(
                self,
                self.whiteboard.graph,
                self.config.last_saving_as_script_folder,
            )
            if filename is not None:
                # TODO: Update config w/o using constants, by adding method, or w/ a better way.
                self.config[PATH_SECTION][
                    PATH_LAST_SAVING_AS_SCRIPT_FOLDER
                ] = filename.parent
        else:
            raise ValueError(f"{operation}: Invalid operation.")

    def OpenAboutDialog(self, _: bool, /) -> None:
        """"""
        config = pprt.pformat(self.config, width=1000)
        wdgt.QMessageBox.about(
            self, "About pyVispr", f"pyVispr {__version__}\n{config}"
        )

    def OpenConfiguration(self, _: bool, /) -> None:
        """"""
        wdgt.QMessageBox.about(
            self,
            "pyVispr Configuration",
            "No configuration options yet\n",
        )

    def OpenAboutWorkflowDialog(self, _: bool, /) -> None:
        """"""
        n_visual_nodes, n_functional_nodes, n_links = self.whiteboard.Statistics()
        wdgt.QMessageBox.about(
            self,
            "About Workflow",
            f"Nodes:V={n_visual_nodes}/F={n_functional_nodes}\n" f"Links:{n_links}",
        )

    def Close(self) -> None:
        """"""
        self.config.Save()
        self.close()


def _AddMenu(
    name: str,
    entries: tuple,
    parent_menu: wdgt.QMenuBar | wdgt.QMenu | None,
    parent_widget: wdgt.QWidget,
    /,
) -> wdgt.QMenu:
    """"""
    if parent_menu is None:
        output = wdgt.QMenu(name)
    else:
        output = parent_menu.addMenu(name)

    _AddEntries(output, entries, parent_widget)

    return output


def _AddEntries(
    menu: wdgt.QMenu,
    entries: tuple,
    parent_widget: wdgt.QWidget,
) -> None:
    """"""
    for entry in entries:
        if entry is None:
            menu.addSeparator()
        elif isinstance(entry, wdgt.QMenu):
            menu.addMenu(entry)
        else:
            if isinstance(entry[-1], dict):
                args = entry[:-1]
                kwargs = entry[-1]
            else:
                args = entry
                kwargs = {}
            AddEntryToMenu(menu, parent_widget, *args, **kwargs)


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
