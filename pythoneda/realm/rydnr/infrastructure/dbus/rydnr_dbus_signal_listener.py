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
from pythoneda.shared.artifact_changes.events.commit_staged_changes_request_delegated import CommitStagedChangesRequestDelegated
from pythoneda.shared.artifact_changes.events.infrastructure.dbus.dbus_commit_staged_changes_requestDelegated import DbusCommitStagedChangesRequestDelegated
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
        - pythoneda.artifact_changes.events.infrastructure.dbus.dbus_commit_staged_changes_requested.DbusCommitStagedChangesRequested
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
        key = self.fqdn_key(CommitStagedChangesRequested)
        result[key] = [
            DbusCommitStagedChangesRequested, BusType.SYSTEM
        ]
        return result

    def parse_pythonedarealmrydnr_CommitStagedChangesRequestDelegated(self, message: Message) -> CommitStagedChangesRequestDelegated:
        """
        Parses given d-bus message containing a CommitStagedChangesRequested event.
        :param message: The message.
        :type message: dbus_next.Message
        :return: The CommitStagedChangesRequestDelegated event.
        :rtype: pythoneda.realm.rydnr.events.commit_staged_changes_request_delegated.CommitStagedChangesRequestDelegated
        """
        return DbusCommitStagedChangesRequestDelegated.parse_pythonedarealmrydnr_CommitStagedChangesRequestDelegated(message)

    async def listen_pythonedarealmrydnr_CommitStagedChangesRequestDelegated(self, event: CommitStagedChangesRequestDelegated):
        """
        Gets notified when a signal for a TagCredentialsRequested event occurs.
        :param event: The event.
        :rtype: pythoneda.realm.rydnr.events.commit_staged_changes_request_delegated.CommitStagedChangesRequestDelegated
        """
        await self.app.accept(event)
