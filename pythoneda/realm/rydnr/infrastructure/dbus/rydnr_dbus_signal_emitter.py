"""
pythoneda/realm/rydnr/infrastructure/dbus/rydnr_dbus_signal_emitter.py

This file defines the RydnrDbusSignalEmitter class.

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
from dbus_next import BusType
from pythoneda.event import Event
from pythoneda.shared.artifact_changes.events.commit_staged_changes_requested import CommitStagedChangesRequested
from pythoneda.shared.artifact_changes.events.infrastructure.dbus.dbus_change_staging_requested import DbusCommitStagedChangesRequested
from pythoneda.infrastructure.dbus.dbus_signal_emitter import DbusSignalEmitter
from typing import Dict

class RydnrDbusSignalEmitter(DbusSignalEmitter):

    """
    A Port that emits Rydnr events as d-bus signals.

    Class name: RydnrDbusSignalEmitter

    Responsibilities:
        - Connect to d-bus.
        - Emit domain events as d-bus signals on behalf of Rydnr.

    Collaborators:
        - pythoneda.application.PythonEDA: Requests emitting events.
        - pythoneda.shared.artifact_changes.events.infrastructure.dbus.dbus_change_staging_requested.DbusCommitStagedChangesRequested
    """
    def __init__(self):
        """
        Creates a new RydnrDbusSignalEmitter instance.
        """
        super().__init__()

    def emitters(self) -> Dict:
        """
        Retrieves the configured event emitters.
        :return: A dictionary with the event class name as key, and a dictionary as value. Such dictionary must include the following entries:
          - "interface": the event interface,
          - "busType": the bus type,
          - "transformer": a function capable of transforming the event into a string.
          - "signature": a function capable of returning the types of the event parameters.
        :rtype: Dict
        """
        result = {}
        key = self.fqdn_key(CommitStagedChangesRequested)
        result[key] = {
                "interface": DbusCommitStagedChangesRequested,
                "busType": BusType.SYSTEM,
                "transformer": DbusCommitStagedChangesRequested.transform_CommitStagedChangesRequested,
                "signature": DbusCommitStagedChangesRequested.signature_for_CommitStagedChangesRequested
            }

        return result
