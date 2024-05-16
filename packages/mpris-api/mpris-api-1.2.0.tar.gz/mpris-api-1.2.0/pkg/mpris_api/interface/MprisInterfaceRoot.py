#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from pathlib import Path
from typing import List

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterRoot import IMprisAdapterRoot
from mpris_api.common.DbusArray import DbusArray
from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.dbusDecorators import dbusInterfaceSignature, dbusMethod, dbusProperty
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
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canQuit(self) -> bool:
        return self._adapter.canQuit()

    @dbusProperty(name=MprisRootPropertyId.CAN_RAISE.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canRaise(self) -> bool:
        return self._adapter.canRaise()

    @dbusProperty(name=MprisRootPropertyId.CAN_SET_FULL_SCREEN.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canSetFullscreen(self) -> bool:
        return self._adapter.canSetFullscreen()

    @dbusProperty(name=MprisRootPropertyId.IDENTITY.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.STRING
    )
    def identity(self) -> str:
        return self._adapter.getIdentity()

    @dbusProperty(name=MprisRootPropertyId.DESKTOP_ENTRY.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.STRING
    )
    def desktopEntry(self) -> str:
        desktopEntry = self._adapter.getDesktopEntry()
        return '' if desktopEntry is None\
            else str(Path(desktopEntry).with_suffix(''))

    @dbusProperty(name=MprisRootPropertyId.SUPPORTED_URI_SCHEMES.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusArray(DbusPrimitive.STRING)
    )
    def supportedUriSchemes(self) -> List[str]:
        return self._adapter.getSupportedUriSchemes()

    @dbusProperty(name=MprisRootPropertyId.SUPPORTED_MIME_TYPES.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusArray(DbusPrimitive.STRING)
    )
    def supportedMimeTypes(self) -> List[str]:
        return self._adapter.getSupportedMimeTypes()

    @dbusProperty(name=MprisRootPropertyId.HAS_TRACK_LIST.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def hasTracklist(self) -> bool:
        return self._adapter.hasTracklist()

    @dbusProperty(name=MprisRootPropertyId.FULL_SCREEN.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def fullScreen(self) -> bool:
        return self._adapter.isFullScreen()

    @fullScreen.setter  # type: ignore
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.BOOL],
        returnType=DbusPrimitive.NOTHING
    )
    def fullScreen(self, value: bool) -> None:
        self._adapter.setFullScreen(value=value)

    @dbusMethod(name=MprisRootMethodId.QUIT.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def quitApp(self) -> None:
        self._adapter.quitApp()

    @dbusMethod(name=MprisRootMethodId.RAISE.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def raiseApp(self) -> None:
        self._adapter.raiseApp()
