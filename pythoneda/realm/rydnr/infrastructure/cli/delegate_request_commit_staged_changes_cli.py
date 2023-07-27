"""
pythoneda/realm/rydnr/infrastructure/cli/delegate_request_commit_staged_changes_cli.py

This file defines the DelegateRequestCommitStagedChangesCli.

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
from pythoneda.primary_port import PrimaryPort
from pythoneda.realm.rydnr.events.staged_changes_commit_request_delegated import StagedChangesCommitRequestDelegated
import sys

class DelegateCommitStagedChangesRequestCli(PrimaryPort):

    """
    A PrimaryPort that makes Rydnr delegate the request to commit staged changes.

    Class name: DelegateCommitStagedChangesRequestCli

    Responsibilities:
        - Parse the command-line to retrieve the information needed to delegate requests to commit staged changes.

    Collaborators:
        - PythonEDA subclasses: They are notified back with the information retrieved from the command line.
        - pythoneda.realm.rydnr.events.staged_changes_commit_request_delegated.StagedChangesCommitRequestDelegated
    """

    def priority(self) -> int:
        return 100

    async def accept(self, app):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: PythonEDA
        """
        parser = argparse.ArgumentParser(
            description="Delegate request to commit staged changes"
        )
        parser.add_argument(
            "command",
            choices=["stage", "commit"],
            nargs="?",
            default=None,
            help="Whether to stage or commit changes",
        )
        parser.add_argument(
            "-r", "--repository-folder", required=False, help="The repository folder"
        )
        parser.add_argument(
            "-m", "--message", required=False, help="The commit message"
        )
        args, unknown_args = parser.parse_known_args()

        if args.command == "commit":
            if not args.message:
                print(f"-m|--message is mandatory")
                sys.exit(1)
            if not args.repository_folder:
                print(f"-r|--repository-folder is mandatory")
                sys.exit(1)
            if args.message and args.repository_folder:
                print(f"Sending StagedChangesCommitRequestDelegated to rydnr")
                await app.accept(
                    StagedChangesCommitRequestDelegated(
                        args.message, args.repository_folder
                    )
                )
