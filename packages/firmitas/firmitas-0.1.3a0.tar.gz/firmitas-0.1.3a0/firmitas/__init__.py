"""
Firmitas
Copyright (C) 2023-2024 Akashdeep Dhar

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.

Any Red Hat trademarks that are incorporated in the source code or
documentation are not subject to the GNU General Public License and may only
be used or replicated with the express permission of Red Hat, Inc.
"""


import os.path
import sys
from importlib import metadata
from logging import getLogger
from logging.config import dictConfig
from pathlib import Path

import yaml

from firmitas.conf import logrdata, standard

__vers__ = metadata.version("firmitas")


def readconf(confobjc):
    standard.gitforge = confobjc.get("gitforge", standard.gitforge)
    standard.repoloca = confobjc.get("repoloca", standard.repoloca)
    standard.reponame = confobjc.get("reponame", standard.reponame)
    standard.username = confobjc.get("username", standard.username)
    standard.password = confobjc.get("password", standard.password)
    standard.daysqant = confobjc.get("daysqant", standard.daysqant)
    standard.maxretry = confobjc.get("maxretry", standard.maxretry)
    standard.certloca = confobjc.get("certloca", standard.certloca)
    standard.hostloca = confobjc.get("hostloca", standard.hostloca)

    dictConfig(standard.logrconf)
    logrdata.logrobjc = getLogger(__name__)

    if standard.gitforge not in ["pagure", "github", "gitlab"]:
        logrdata.logrobjc.error("The specified ticketing repository forge is not yet supported")
        sys.exit(1)

    if not isinstance(standard.daysqant, int):
        logrdata.logrobjc.error(
            "The variable 'daysqant' must have a value of the integer data type only"
        )
        sys.exit(1)
    else:
        if standard.daysqant <= 0:
            logrdata.logrobjc.error(
                "The variable 'daysqant' must have a non-zero positive integer value"
            )
            sys.exit(1)

    if not os.path.exists(standard.certloca):
        logrdata.logrobjc.error(
            "Please set the directory containing X.509 standard TLS certificates properly"
        )
        sys.exit(1)

    if not os.path.exists(standard.hostloca):
        logrdata.logrobjc.error(
            "Please set the directory containing the service hostname map properly"
        )
        sys.exit(1)
    else:
        standard.certdict = yaml.safe_load(Path(standard.hostloca).read_text())
