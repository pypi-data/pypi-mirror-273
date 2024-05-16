"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h
from configparser import DEFAULTSECT as DEFAULT_SECTION
from configparser import ConfigParser as config_parser_t
from pathlib import Path as path_t

from pyvispr.config.path import CONFIG_FILE
from pyvispr.constant.config import (
    DEFAULT_CONFIG,
    HISTORY_N_NODES_MOST_USED,
    HISTORY_N_NODES_RECENT,
    HISTORY_NODE_USAGE_SEPARATOR,
    HISTORY_NODES_MOST_USED,
    HISTORY_NODES_RECENT,
    HISTORY_NODES_SEPARATOR,
    HISTORY_SECTION,
    PATH_FLOWS_RECENT,
    PATH_LAST_LOADING_FOLDER,
    PATH_LAST_SAVING_AS_SCRIPT_FOLDER,
    PATH_LAST_SAVING_FOLDER,
    PATH_N_FLOWS_RECENT,
    PATH_SECTION,
    PATH_SEPARATOR,
)


class config_t(dict[str, h.Any]):
    @staticmethod
    def NewConfigParser() -> config_parser_t:
        """"""
        return config_parser_t(delimiters="=", comment_prefixes="#")

    def __init__(self) -> None:
        """"""
        dict.__init__(self)

        ini_config = config_t.NewConfigParser()
        ini_config.read_dict(DEFAULT_CONFIG)
        ini_config.read(CONFIG_FILE)

        self.update(
            {
                _nme: dict(_sct)
                for _nme, _sct in ini_config.items()
                if _nme != DEFAULT_SECTION
            }
        )

        self[HISTORY_SECTION][HISTORY_N_NODES_RECENT] = int(
            self[HISTORY_SECTION][HISTORY_N_NODES_RECENT]
        )
        self[HISTORY_SECTION][HISTORY_NODES_RECENT] = _Split(
            self[HISTORY_SECTION][HISTORY_NODES_RECENT], HISTORY_NODES_SEPARATOR
        )

        self[HISTORY_SECTION][HISTORY_N_NODES_MOST_USED] = int(
            self[HISTORY_SECTION][HISTORY_N_NODES_MOST_USED]
        )
        nodes = self[HISTORY_SECTION][HISTORY_NODES_MOST_USED]
        if nodes is None:
            nodes = {}
        elif HISTORY_NODES_SEPARATOR in nodes:
            nodes = nodes.split(HISTORY_NODES_SEPARATOR)
            nodes = map(lambda _elm: _elm.split(HISTORY_NODE_USAGE_SEPARATOR), nodes)
            nodes = map(lambda _elm: [_elm[0], int(_elm[1])], nodes)
            nodes = dict(nodes)
        elif nodes.__len__() > 0:
            name, usage = nodes.split(HISTORY_NODE_USAGE_SEPARATOR)
            nodes = {name: int(usage)}
        else:
            nodes = {}
        self[HISTORY_SECTION][HISTORY_NODES_MOST_USED] = nodes

        self[PATH_SECTION][PATH_LAST_LOADING_FOLDER] = path_t(
            self[PATH_SECTION][PATH_LAST_LOADING_FOLDER]
        )
        self[PATH_SECTION][PATH_LAST_SAVING_FOLDER] = path_t(
            self[PATH_SECTION][PATH_LAST_SAVING_FOLDER]
        )
        self[PATH_SECTION][PATH_LAST_SAVING_AS_SCRIPT_FOLDER] = path_t(
            self[PATH_SECTION][PATH_LAST_SAVING_AS_SCRIPT_FOLDER]
        )

        self[PATH_SECTION][PATH_N_FLOWS_RECENT] = int(
            self[PATH_SECTION][PATH_N_FLOWS_RECENT]
        )
        paths = _Split(self[PATH_SECTION][PATH_FLOWS_RECENT], PATH_SEPARATOR)
        self[PATH_SECTION][PATH_FLOWS_RECENT] = list(map(path_t, paths))

    @property
    def recent_nodes(self) -> tuple[str, ...]:
        """"""
        return tuple(self[HISTORY_SECTION][HISTORY_NODES_RECENT])

    @property
    def most_used_nodes(self) -> tuple[str, ...]:
        """"""
        nodes = self[HISTORY_SECTION][HISTORY_NODES_MOST_USED].items()
        nodes = sorted(nodes, key=lambda _elm: _elm[1], reverse=True)
        nodes = nodes[: self[HISTORY_SECTION][HISTORY_N_NODES_MOST_USED]]
        nodes = (_elm[0] for _elm in nodes)

        return tuple(nodes)

    def UpdateRecentNodes(self, name: str, /) -> None:
        """"""
        _UpdateRecent_s(
            self[HISTORY_SECTION][HISTORY_NODES_RECENT],
            name,
            self[HISTORY_SECTION][HISTORY_N_NODES_RECENT],
        )

    def UpdateMostUsedNodes(self, name: str, /) -> None:
        """"""
        nodes = self[HISTORY_SECTION][HISTORY_NODES_MOST_USED]
        if name in nodes:
            nodes[name] += 1
        else:
            nodes[name] = 1

    @property
    def recent_flows(self) -> tuple[path_t, ...]:
        """"""
        return tuple(self[PATH_SECTION][PATH_FLOWS_RECENT])

    def UpdateRecentFlows(self, path: path_t, /) -> None:
        """"""
        _UpdateRecent_s(
            self[PATH_SECTION][PATH_FLOWS_RECENT],
            path,
            self[PATH_SECTION][PATH_N_FLOWS_RECENT],
        )

    @property
    def last_loading_folder(self) -> path_t:
        """"""
        return self[PATH_SECTION][PATH_LAST_LOADING_FOLDER]

    @property
    def last_saving_folder(self) -> path_t:
        """"""
        return self[PATH_SECTION][PATH_LAST_SAVING_FOLDER]

    @property
    def last_saving_as_script_folder(self) -> path_t:
        """"""
        return self[PATH_SECTION][PATH_LAST_SAVING_AS_SCRIPT_FOLDER]

    def Save(self) -> None:
        """"""
        formatted = {
            _ky1: {_ky2: _vl2 for _ky2, _vl2 in _vl1.items()}
            for _ky1, _vl1 in self.items()
        }

        formatted[HISTORY_SECTION][HISTORY_NODES_RECENT] = HISTORY_NODES_SEPARATOR.join(
            formatted[HISTORY_SECTION][HISTORY_NODES_RECENT]
        )

        nodes = formatted[HISTORY_SECTION][HISTORY_NODES_MOST_USED].items()
        nodes = map(
            lambda _elm: f"{_elm[0]}{HISTORY_NODE_USAGE_SEPARATOR}{_elm[1]}", nodes
        )
        formatted[HISTORY_SECTION][HISTORY_NODES_MOST_USED] = (
            HISTORY_NODES_SEPARATOR.join(nodes)
        )

        formatted[PATH_SECTION][PATH_FLOWS_RECENT] = PATH_SEPARATOR.join(
            map(str, formatted[PATH_SECTION][PATH_FLOWS_RECENT])
        )

        config = config_t.NewConfigParser()
        config.read_dict(formatted)
        with open(CONFIG_FILE, "w") as accessor:
            config.write(accessor)


def _Split(joined: str | None, separator: str, /) -> list[str]:
    """"""
    if joined is None:
        return []

    if separator in joined:
        return joined.split(separator)

    if joined.__len__() > 0:
        return [joined]

    return []


def _UpdateRecent_s(
    recent_s: list[h.Any], new_element: h.Any, max_length: int, /
) -> None:
    """"""
    if new_element in recent_s:
        recent_s.remove(new_element)
        recent_s.insert(0, new_element)
    elif recent_s.__len__() < max_length:
        recent_s.insert(0, new_element)


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
