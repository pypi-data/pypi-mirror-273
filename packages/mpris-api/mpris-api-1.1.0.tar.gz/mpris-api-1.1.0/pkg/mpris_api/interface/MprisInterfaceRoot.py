#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path
from typing import no_type_check

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterRoot import IMprisAdapterRoot
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty
from mpris_api.common.dbusEnums import DbusMethodId, DbusPropertyId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant


class MprisRootPropertyId(DbusPropertyId):
    CAN_QUIT = 'CanQuit'
    CAN_RAISE = 'CanRaise'
    CAN_SET_FULL_SCREEN = 'CanSetFullscreen'
    HAS_TRACK_LIST = 'HasTrackList'
    FULL_SCREEN = 'Fullscreen'
    IDENTITY = 'Identity'
    DESKTOP_ENTRY = 'DesktopEntry'
    SUPPORTED_URI_SCHEMES = 'SupportedUriSchemes'
    SUPPORTED_MIME_TYPES = 'SupportedMimeTypes'


class MprisRootMethodId(DbusMethodId):
    QUIT = 'Quit'
    RAISE = 'Raise'


class MprisInterfaceRoot(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterRoot) -> None:
        super().__init__(MprisConstant.NAME)
        self._adapter: IMprisAdapterRoot = adapter

    @dbusProperty(name=MprisRootPropertyId.CAN_QUIT.value, access=PropertyAccess.READ)
    @no_type_check
    def canQuit(self) -> DbusType.BOOL:
        return self._adapter.canQuit()

    @dbusProperty(name=MprisRootPropertyId.CAN_RAISE.value, access=PropertyAccess.READ)
    @no_type_check
    def canRaise(self) -> DbusType.BOOL:
        return self._adapter.canRaise()

    @dbusProperty(name=MprisRootPropertyId.CAN_SET_FULL_SCREEN.value, access=PropertyAccess.READ)
    @no_type_check
    def canSetFullscreen(self) -> DbusType.BOOL:
        return self._adapter.canSetFullscreen()

    @dbusProperty(name=MprisRootPropertyId.IDENTITY.value, access=PropertyAccess.READ)
    @no_type_check
    def identity(self) -> DbusType.STRING:
        return self._adapter.getIdentity()

    @dbusProperty(name=MprisRootPropertyId.DESKTOP_ENTRY.value, access=PropertyAccess.READ)
    @no_type_check
    def desktopEntry(self) -> DbusType.STRING:
        desktopEntry = self._adapter.getDesktopEntry()
        return '' if desktopEntry is None\
            else str(Path(desktopEntry).with_suffix(''))

    @dbusProperty(name=MprisRootPropertyId.SUPPORTED_URI_SCHEMES.value, access=PropertyAccess.READ)
    @no_type_check
    def supportedUriSchemes(self) -> DbusType.STRING_ARRAY:
        return self._adapter.getSupportedUriSchemes()

    @dbusProperty(name=MprisRootPropertyId.SUPPORTED_MIME_TYPES.value, access=PropertyAccess.READ)
    @no_type_check
    def supportedMimeTypes(self) -> DbusType.STRING_ARRAY:
        return self._adapter.getSupportedMimeTypes()

    @dbusProperty(name=MprisRootPropertyId.HAS_TRACK_LIST.value, access=PropertyAccess.READ)
    @no_type_check
    def hasTracklist(self) -> DbusType.BOOL:
        return self._adapter.hasTracklist()

    @dbusProperty(name=MprisRootPropertyId.FULL_SCREEN.value)
    @no_type_check
    def fullScreen(self) -> DbusType.BOOL:
        return self._adapter.isFullScreen()

    @fullScreen.setter  # type: ignore
    @no_type_check
    def fullScreen(self, value: DbusType.BOOL) -> None:
        self._adapter.setFullScreen(value=value)

    @dbusMethod(name=MprisRootMethodId.QUIT.value)
    @no_type_check
    def quitApp(self) -> None:
        self._adapter.quitApp()

    @dbusMethod(name=MprisRootMethodId.RAISE.value)
    @no_type_check
    def raiseApp(self) -> None:
        self._adapter.raiseApp()
