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
from pythoneda.realm.rydnr.events import ChangeStagingCodeRequestDelegated
from pythoneda.realm.rydnr.events.infrastructure.dbus import DbusChangeStagingCodeRequestDelegated
from pythoneda.shared.artifact_changes.events import ChangeStagingCodeDescribed
from pythoneda.shared.artifact_changes.events.infrastructure.dbus import DbusChangeStagingCodeDescribed
from pythoneda.infrastructure.dbus import DbusSignalListener
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
        - pythoneda.realm.rydnr.events.infrastructure.dbus.DbusChangeStagingCodeRequestDelegated
        - pythoneda.artifact_changes.events.infrastructure.dbus.DbusChangeStagingCodeDescribed
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
        :type app: pythoneda.application.PythonEDA
        :return: A dictionary with the signal name as key, and the tuple interface and bus type as the value.
        :rtype: Dict
        """
        result = {}
        key = self.__class__.full_class_name(ChangeStagingCodeRequestDelegated)
        result[key] = [
            DbusChangeStagingCodeRequestDelegated, BusType.SYSTEM
        ]
        key = self.__class__.full_class_name(ChangeStagingCodeDescribed)
        result[key] = [
            DbusChangeStagingCodeDescribed, BusType.SYSTEM
        ]
        return result
