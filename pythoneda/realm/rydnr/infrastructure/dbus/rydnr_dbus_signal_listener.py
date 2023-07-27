"""
pythoneda/realm/rydnr/infrastructure/dbus/rydnr_dbus_signal_listener.py

This file defines the RydnrDbusSignalListener class.

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
from dbus_next import BusType, Message
from pythoneda.event import Event
from pythoneda.realm.rydnr.events.staged_changes_commit_request_delegated import StagedChangesCommitRequestDelegated
from pythoneda.realm.rydnr.events.infrastructure.dbus.dbus_staged_changes_commit_request_delegated import DbusStagedChangesCommitRequestDelegated
from pythoneda.infrastructure.dbus.dbus_signal_listener import DbusSignalListener
from typing import Dict

class RydnrDbusSignalListener(DbusSignalListener):

    """
    A Port that listens to Rydnr-relevant d-bus signals.

    Class name: RydnrDbusSignalListener

    Responsibilities:
        - Connect to d-bus.
        - Listen to signals relevant to Rydnr.

    Collaborators:
        - pythoneda.application.pythoneda.PythonEDA: Receives relevant domain events.
        - pythoneda.artifact_changes.events.infrastructure.dbus.dbus_staged_changes_commit_request_delegated.DbusStagedChangesCommitRequestDelegated
    """

    def __init__(self):
        """
        Creates a new RydnrDbusSignalListener instance.
        """
        super().__init__()

    def signal_receivers(self, app) -> Dict:
        """
        Retrieves the configured signal receivers.
        :param app: The PythonEDA instance.
        :type app: pythoneda.application.pythoneda.PythonEDA
        :return: A dictionary with the signal name as key, and the tuple interface and bus type as the value.
        :rtype: Dict
        """
        result = {}
        key = self.fqdn_key(StagedChangesCommitRequestDelegated)
        result[key] = [
            DbusStagedChangesCommitRequestDelegated, BusType.SYSTEM
        ]
        return result

    def parse_pythonedarealmrydnr_StagedChangesCommitRequestDelegated(self, message: Message) -> StagedChangesCommitRequestDelegated:
        """
        Parses given d-bus message containing a StagedChangesCommitRequestDelegated event.
        :param message: The message.
        :type message: dbus_next.Message
        :return: The StagedChangesCommitRequestDelegated event.
        :rtype: pythoneda.realm.rydnr.events.staged_changes_commit_request_delegated.StagedChangesCommitRequestDelegated
        """
        return DbusStagedChangesCommitRequestDelegated.parse_pythonedarealmrydnr_StagedChangesCommitRequestDelegated(message)

    async def listen_pythonedarealmrydnr_StagedChangesCommitRequestDelegated(self, event: StagedChangesCommitRequestDelegated):
        """
        Gets notified when a signal for a TagCredentialsRequested event occurs.
        :param event: The event.
        :rtype: pythoneda.realm.rydnr.events.staged_changes_commit_request_delegated.StagedChangesCommitRequestDelegated
        """
        await self.app.accept(event)
