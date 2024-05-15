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
import typing as h
from configparser import ConfigParser as config_parser_t

import PyQt6.QtWidgets as wdgt
from logger_36 import AddGenericHandler
from pyvispr import __version__
from pyvispr.config.path import CONFIG_FILE
from pyvispr.constant.app import APP_NAME
from pyvispr.constant.config import (
    DEFAULT_CONFIG,
    HISTORY_N_NODES_MOST_USED,
    HISTORY_N_NODES_RECENT,
    HISTORY_NODE_USAGE_SEPARATOR,
    HISTORY_NODES_MOST_USED,
    HISTORY_NODES_RECENT,
    HISTORY_NODES_SEPARATOR,
    HISTORY_SECTION,
)
from pyvispr.flow.visual.whiteboard import whiteboard_t
from pyvispr.interface.storage.loading import LoadWorkflow
from pyvispr.interface.storage.stowing import SaveWorkflow, SaveWorkflowAsScript
from pyvispr.interface.window.widget.list.node import node_list_wgt_t
from pyvispr.interface.window.widget.menu import AddEntryToMenu
from pyvispr.runtime.backend import SCREEN_BACKEND


@dtcl.dataclass(slots=True, repr=False, eq=False)
class runner_wdw_t(wdgt.QMainWindow):
    config: dict[str, h.Any]
    node_list: node_list_wgt_t
    whiteboard: whiteboard_t
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
            element_name="Recent", source=self.recent_nodes, should_be_sorted=False
        )
        self.most_used_list = node_list_wgt_t(
            element_name="Most Used",
            source=self.most_used_nodes,
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
            SCREEN_BACKEND.CreateMessageCanal(node_list, "itemClicked", self.AddNode)

    @classmethod
    def New(cls) -> runner_wdw_t:
        """"""
        ini_config = config_parser_t(delimiters="=", comment_prefixes="#")
        ini_config.read_dict(DEFAULT_CONFIG)
        ini_config.read(CONFIG_FILE)

        config: dict[str, h.Any] = {_nme: dict(_sct) for _nme, _sct in ini_config.items()}

        config[HISTORY_SECTION][HISTORY_N_NODES_RECENT] = int(
            config[HISTORY_SECTION][HISTORY_N_NODES_RECENT]
        )
        nodes = config[HISTORY_SECTION][HISTORY_NODES_RECENT]
        if HISTORY_NODES_SEPARATOR in nodes:
            config[HISTORY_SECTION][HISTORY_NODES_RECENT] = nodes.split(
                HISTORY_NODES_SEPARATOR
            )
        elif nodes.__len__() > 0:
            config[HISTORY_SECTION][HISTORY_NODES_RECENT] = [nodes]
        else:
            config[HISTORY_SECTION][HISTORY_NODES_RECENT] = []

        config[HISTORY_SECTION][HISTORY_N_NODES_MOST_USED] = int(
            config[HISTORY_SECTION][HISTORY_N_NODES_MOST_USED]
        )
        nodes = config[HISTORY_SECTION][HISTORY_NODES_MOST_USED]
        if HISTORY_NODES_SEPARATOR in nodes:
            nodes = nodes.split(HISTORY_NODES_SEPARATOR)
            nodes = map(lambda _elm: _elm.split(HISTORY_NODE_USAGE_SEPARATOR), nodes)
            nodes = map(lambda _elm: [_elm[0], int(_elm[1])], nodes)
            config[HISTORY_SECTION][HISTORY_NODES_MOST_USED] = dict(nodes)
        elif nodes.__len__() > 0:
            name, usage = nodes.split(HISTORY_NODE_USAGE_SEPARATOR)
            config[HISTORY_SECTION][HISTORY_NODES_MOST_USED] = {name: int(usage)}
        else:
            config[HISTORY_SECTION][HISTORY_NODES_MOST_USED] = {}

        node_list = node_list_wgt_t(element_name="Nodes")
        whiteboard = whiteboard_t()

        return cls(config=config, node_list=node_list, whiteboard=whiteboard)

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
                ("&Quit", lambda *_, **__: self.Close(), {"shortcut": "Ctrl+Q"}),
            ),
            menu_bar,
            self,
        )

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
        clear_menu = _AddMenu(
            "Clear...",
            (
                (
                    "Now",
                    lambda *_, **__: self.whiteboard.graph.Clear(),
                ),
            ),
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
                ("&Save", lambda *_, **__: SaveWorkflow(self), {"shortcut": "Ctrl+S"}),
                ("L&oad", lambda *_, **__: LoadWorkflow(self), {"shortcut": "Ctrl+O"}),
                None,
                ("Save As Script", lambda *_, **__: SaveWorkflowAsScript(self)),
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
            (("Refresh", lambda *_, **__: self.node_list.Reload()),),
            menu_bar,
            self,
        )

    def AddNode(self, item: wdgt.QListWidgetItem, /) -> None:
        """
        Calling directly on self.whiteboard.graph from the menu will not work if the graph changes.
        """
        name = item.text()
        self.whiteboard.graph.AddNode(name)

        self.UpdateRecentNodes(name)
        self.recent_list.source = self.recent_nodes
        self.recent_list.Reload()

        self.UpdateMostUsedNodes(name)
        self.most_used_list.source = self.most_used_nodes
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

    def OpenAboutDialog(self, _: bool, /) -> None:
        """"""
        wdgt.QMessageBox.about(self, "About pyVispr", f"pyVispr {__version__}")

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

    @property
    def recent_nodes(self) -> tuple[str, ...]:
        """"""
        return tuple(self.config[HISTORY_SECTION][HISTORY_NODES_RECENT])

    @property
    def most_used_nodes(self) -> tuple[str, ...]:
        """"""
        nodes = self.config[HISTORY_SECTION][HISTORY_NODES_MOST_USED].items()
        nodes = sorted(nodes, key=lambda _elm: _elm[1], reverse=True)
        nodes = nodes[: self.config[HISTORY_SECTION][HISTORY_N_NODES_MOST_USED]]
        nodes = (_elm[0] for _elm in nodes)

        return tuple(nodes)

    def UpdateRecentNodes(self, name: str, /) -> None:
        """"""
        if name in (nodes := self.config[HISTORY_SECTION][HISTORY_NODES_RECENT]):
            nodes.remove(name)
            nodes.insert(0, name)
        elif nodes.__len__() < self.config[HISTORY_SECTION][HISTORY_N_NODES_RECENT]:
            nodes.insert(0, name)

    def UpdateMostUsedNodes(self, name: str, /) -> None:
        """"""
        nodes = self.config[HISTORY_SECTION][HISTORY_NODES_MOST_USED]
        if name in nodes:
            nodes[name] += 1
        else:
            nodes[name] = 1

    def Close(self) -> None:
        """"""
        self.config[HISTORY_SECTION][HISTORY_NODES_RECENT] = (
            HISTORY_NODES_SEPARATOR.join(
                self.config[HISTORY_SECTION][HISTORY_NODES_RECENT]
            )
        )

        nodes = self.config[HISTORY_SECTION][HISTORY_NODES_MOST_USED].items()
        nodes = map(
            lambda _elm: f"{_elm[0]}{HISTORY_NODE_USAGE_SEPARATOR}{_elm[1]}", nodes
        )
        self.config[HISTORY_SECTION][HISTORY_NODES_MOST_USED] = (
            HISTORY_NODES_SEPARATOR.join(nodes)
        )

        config = config_parser_t(delimiters="=", comment_prefixes="#")
        config.read_dict(self.config)
        with open(CONFIG_FILE, "w") as accessor:
            config.write(accessor)

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

    for entry in entries:
        if entry is None:
            output.addSeparator()
        elif isinstance(entry, wdgt.QMenu):
            output.addMenu(entry)
        else:
            if isinstance(entry[-1], dict):
                args = entry[:-1]
                kwargs = entry[-1]
            else:
                args = entry
                kwargs = {}
            AddEntryToMenu(output, parent_widget, *args, **kwargs)

    return output
