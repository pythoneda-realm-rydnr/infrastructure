"""
pythoneda/realm/rydnr/infrastructure/cli/test_jupyter_request_cli.py

This file defines the TestJupyterRequestCli.

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
import asyncio
import os
from pathlib import Path
from pythoneda.shared.code_requests.jupyter.jupyter_code_request import (
    JupyterCodeRequest,
)
from pythoneda.primary_port import PrimaryPort
import shutil
import subprocess
import sys
import tempfile

class TestJupyterRequestCli(PrimaryPort):

    """
    A PrimaryPort to test Jupyter requests.

    Class name: TestJupyterRequestCli

    Responsibilities:
        - Parse the command-line to test Jupyter requests.

    Collaborators:
        - pythoneda.shared.code_requests.jupyter.jupyter_code_request.JupyterCodeRequest
    """

    def priority(self) -> int:
        return 100

    async def accept(self, app):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: PythonEDA
        """
        print(f'In test_jupyter_code_request_cli.py')
        parser = argparse.ArgumentParser(description="Test a Jupyter request")
        parser.add_argument(
            "command",
            choices=["jupyter"],
            nargs="?",
            default=None,
            help="Test a Jupyter request",
        )
        args, unknown_args = parser.parse_known_args()

        if args.command == "jupyter":
            jupyter_code_request = JupyterCodeRequest()
            with tempfile.TemporaryDirectory() as tempd:
                task = asyncio.create_task(self.run_flake(tempd))
                await task

    async def run_flake(self, tempFolder):
        jupyter_code_request = JupyterCodeRequest()
        jupyter_code_request.append("print('Hello, World!')")
        # create a flake in a temporary folder
        shutil.copy(Path(os.getcwd()) / ".." / "application" / "flake.nix", Path(tempFolder) / "flake.nix")
        shutil.copy(Path(os.getcwd()) / ".." / "application" / "pyprojecttoml.template", Path(tempFolder) / "pyprojecttoml.template")
        try:
            subprocess.run(["git", "init", "."], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tempFolder)
        except subprocess.CalledProcessError as err:
            print(err.stderr)
        with open(Path(tempFolder) / "code-request.ipynb", "w", encoding="utf-8") as f:
            jupyter_code_request.write(f)
        try:
            subprocess.run(["git", "add", "flake.nix", "pyprojecttoml.template", "code-request.ipynb"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tempFolder)
        except subprocess.CalledProcessError as err:
            print(err.stderr)
        # run `nix run`
        try:
            process = await asyncio.create_subprocess_shell("nix run .", stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tempFolder)
        except subprocess.CalledProcessError as err:
            print(err.stderr)

        stdout, stderr = await process.communicate()

        if stdout:
            print(stdout.decode())
        if stderr:
            print(stderr.decode())

        print(f'nix run {tempFolder} finished')

        return process
