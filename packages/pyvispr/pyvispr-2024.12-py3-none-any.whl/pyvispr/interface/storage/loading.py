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

from pathlib import Path as path_t

import PyQt6.QtWidgets as wdgt
from json_any.task.storage import LoadFromJSON
from pyvispr.flow.visual.whiteboard import whiteboard_t


def LoadWorkflow(
    manager: wdgt.QWidget, whiteboard: whiteboard_t, last_loading: path_t, /
) -> path_t | None:
    """"""
    if last_loading.is_file():
        filename = last_loading
    else:
        filename = wdgt.QFileDialog.getOpenFileName(
            manager,
            "Load Workflow",
            str(last_loading),
            "pyVispr Workflows (*.json.*)",
        )
        if (filename is None) or (len(filename[0]) == 0):
            return None
        filename = path_t(filename[0])

    if whiteboard.graph.nodes.__len__() > 0:
        loading_mode = wdgt.QMessageBox(manager)
        loading_mode.setWindowTitle("Loading Options")
        loading_mode.setText(
            "About to load a workflow while the current workflow is not empty\n"
            "Loading options:"
        )
        merging = loading_mode.addButton(
            "Merge Workflows", wdgt.QMessageBox.ButtonRole.YesRole
        )
        _ = loading_mode.addButton(
            "Replace Workflow", wdgt.QMessageBox.ButtonRole.NoRole
        )
        loading_mode.exec()

        is_update = loading_mode.clickedButton() == merging
    else:
        is_update = False

    try:
        loaded = LoadFromJSON(filename)
    except Exception as exception:
        wdgt.QMessageBox.critical(
            None,
            f"Workflow Loading Error",
            str(exception),
        )
        return None

    whiteboard.SetGraph(graph=loaded, is_update=is_update)

    return filename
