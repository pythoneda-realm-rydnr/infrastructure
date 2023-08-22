"""
pythoneda/realm/rydnr/infrastructure/cli/change_staging_code_request_delegated_cli.py

This file defines the ChangeStagingCodeRequestDelegatedCli.

Copyright (C) 2023-today rydnr's pythoneda-realm-rydnr/infrastructure

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import argparse
from pythoneda import PrimaryPort
from pythoneda.realm.rydnr.events import ChangeStagingCodeRequestDelegated
import sys

class ChangeStagingCodeRequestDelegatedCli(PrimaryPort):

    """
    A PrimaryPort that makes Rydnr request code to perform the staging of some changes.

    Class name: ChangeStagingCodeRequestDelegatedCli

    Responsibilities:
        - Parse the command-line to retrieve the information needed to request code to stage changes.

    Collaborators:
        - PythonEDA subclasses: They are notified back with the information retrieved from the command line.
        - pythoneda.realm.rydnr.events.change_staging_code_request_delegated.ChangeStagingCodeRequestDelegated
    """

    async def accept(self, app):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: PythonEDA
        """
        parser = argparse.ArgumentParser(description="Delegate request code to stage changes")
        parser.add_argument(
            "command",
            choices=["stage", "commit", "jupyter"],
            nargs="?",
            default=None,
            help="Whether to stage changes",
        )
        parser.add_argument(
            "-r", "--repository-folder", required=False, help="The repository folder"
        )
        args, unknown_args = parser.parse_known_args()

        if args.command == "stage":
            if not args.repository_folder:
                print(f"-r|--repository-folder is mandatory")
                sys.exit(1)
            else:
                event = ChangeStagingCodeRequestDelegated(args.repository_folder)
                ChangeStagingCodeRequestDelegatedCli.logger().debug(f"Sending {event} to {app}")
                await app.accept(event)
