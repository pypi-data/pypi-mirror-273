# Copyright CNRS/Inria/UniCA
# Contributor(s): Eric Debreuve (since 2017)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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


@dtcl.dataclass(slots=True, repr=False, eq=False)
class runner_wdw_t(wdgt.QMainWindow):
    config: config_t
    node_list: node_list_wgt_t
    whiteboard: whiteboard_t
    load_recent: wdgt.QMenu = dtcl.field(init=False)
    recent_list: node_list_wgt_t = dtcl.field(init=False)
    most_used_list: node_list_wgt_t = dtcl.field(init=False)
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

        tabs = wdgt.QTabWidget()
        tabs.addTab(self.whiteboard, "Workflow")
        tabs.addTab(log_area, "Messages")
        tabs.setStyleSheet("QTabWidget::tab-bar {alignment: center;}")

        layout = wdgt.QGridLayout()
        layout.addWidget(self.node_list.filter_wgt, 1, 1)
        layout.addWidget(self.node_list, 2, 1, 3, 1)
        layout.addWidget(
            wdgt.QLabel('<span style="font-weight:bold; color:blue">Recent</span>'),
            1,
            2,
        )
        layout.addWidget(self.recent_list, 2, 2)
        layout.addWidget(
            wdgt.QLabel('<span style="font-weight:bold; color:blue">Most Used</span>'),
            3,
            2,
        )
        layout.addWidget(self.most_used_list, 4, 2)
        layout.addWidget(tabs, 1, 3, 4, 1)

        central = wdgt.QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        for node_list in (self.node_list, self.recent_list, self.most_used_list):
            # TODO: AddNode if whiteboard visible, dev info if messages visible,
            #     documentation if documentation visible (Tab to be added).
            SCREEN_BACKEND.CreateMessageCanal(node_list, "itemClicked", self.AddNode)

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
        # /!\ Use lambda function below since the graph object can be replaced with another
        # one. Hence, self.whiteboard.graph must be evaluated each time.
        reset_menu = _AddMenu(
            "Reset...",
            (
                (
                    "Now",
                    lambda *_, **__: self.whiteboard.graph.functional.InvalidateAllNodes(),
                ),
            ),
            None,
            self,
        )
        # /!\ Use lambda function below since the graph object can be replaced with another
        # one. Hence, self.whiteboard.graph must be evaluated each time.
        clear_menu = _AddMenu(
            "Clear...",
            (("Now", lambda *_, **__: self.whiteboard.graph.Clear()),),
            None,
            self,
        )
        self._ref_keeper.extend((reset_menu, clear_menu))
        _ = _AddMenu(
            "&Workflow",
            (
                ("About", self.OpenAboutWorkflowDialog),
                None,
                ("&Run", self.Run, {"shortcut": "Ctrl+R"}),
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
                ("Align on Grid", self.AlignOnGrid),
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

    def _LoadRecentEntries(self) -> tuple[str, h.Callable[..., None] | None]:
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

    def AddNode(self, item: wdgt.QListWidgetItem, /) -> None:
        """
        Calling directly on self.whiteboard.graph from the menu will not work if the graph changes.
        """
        name = item.text()
        self.whiteboard.graph.AddNode(name)

        self.config.UpdateRecentNodes(name)
        self.recent_list.source = self.config.recent_nodes
        self.recent_list.Reload()

        self.config.UpdateMostUsedNodes(name)
        self.most_used_list.source = self.config.most_used_nodes
        self.most_used_list.Reload()

    def AlignOnGrid(self) -> None:
        """
        Calling directly on self.whiteboard.graph from the menu will not work if the graph changes.
        """
        self.whiteboard.graph.AlignOnGrid()

    def Run(self) -> None:
        """
        Calling directly on self.whiteboard.graph from the menu will not work if the graph changes.
        """
        self.whiteboard.graph.Run()

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
        wdgt.QMessageBox.about(
            self,
            "About Workflow",
            f"Nodes:{self.whiteboard.graph.nodes.__len__()}/{self.whiteboard.graph.functional.__len__()}\n"
            f"Links:{self.whiteboard.graph.links.__len__()}",
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
