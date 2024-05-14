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


import click

from firmitas import __vers__, readconf
from firmitas.base.maintool import gonotify, probedir


@click.command(name="firmitas")
@click.option(
    "-c",
    "--conffile",
    "conffile",
    type=click.Path(exists=True),
    help="Read configuration from the specified Python file",
    default=None,
)
@click.version_option(version=__vers__, prog_name="firmitas")
def main(conffile=None):
    if conffile:
        confdict = {}
        with open(conffile) as confobjc:
            exec(compile(confobjc.read(), conffile, "exec"), confdict)  # noqa : S102
        readconf(confdict)
    probedir()
    gonotify()
