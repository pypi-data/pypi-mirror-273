#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import List, Optional, Tuple

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterPlayLists import IMprisAdapterPlayLists
from mpris_api.common.DbusArray import DbusArray
from mpris_api.common.DbusMaybe import DbusMaybe
from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.dbusDecorators import dbusInterfaceSignature, dbusMethod, dbusProperty, dbusSignal
from mpris_api.common.dbusEnums import DbusMethodId, DbusPropertyId, DbusSignalId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant
from mpris_api.model.MprisPlaylist import MprisPlaylist
from mpris_api.model.MprisPlaylistOrdering import MprisPlaylistOrdering


class MprisPlayListsSignalId(DbusSignalId):
    PLAYLIST_CHANGED = 'PlaylistChanged'


class MprisPlayListsPropertyId(DbusPropertyId):
    PLAYLIST_COUNT = 'PlaylistCount'
    ORDERINGS = 'Orderings'
    ACTIVE_PLAYLIST = 'ActivePlaylist'


class MprisPlayListsMethodId(DbusMethodId):
    ACTIVATE_PLAYLIST = 'ActivatePlaylist'
    GET_PLAYLISTS = 'GetPlaylists'


class MprisInterfacePlayLists(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterPlayLists) -> None:
        super().__init__(f'{MprisConstant.NAME}.Playlists')
        self._adapter: IMprisAdapterPlayLists = adapter

    @dbusSignal(name=MprisPlayListsSignalId.PLAYLIST_CHANGED.value)
    @dbusInterfaceSignature(
        argTypes=[MprisPlaylist.getType()],
        returnType=DbusPrimitive.NOTHING
    )
    def playlistChanged(self, playlist: Tuple[str, str, str]) -> None:
        pass

    @dbusProperty(name=MprisPlayListsPropertyId.PLAYLIST_COUNT.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.UINT32
    )
    def playlistCount(self) -> int:
        return self._adapter.getPlaylistCount()

    @dbusProperty(name=MprisPlayListsPropertyId.ORDERINGS.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusArray(DbusPrimitive.STRING)
    )
    def orderings(self) -> List[str]:
        return [ordering.value for ordering in self._adapter.getAvailableOrderings()]

    @dbusProperty(name=MprisPlayListsPropertyId.ACTIVE_PLAYLIST.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusMaybe(MprisPlaylist.getType())
    )
    def activePlaylist(self) -> Tuple[bool, Optional[Tuple[str, str, str]]]:
        activePlaylist = self._adapter.getActivePlaylist()
        return (False, None) if activePlaylist is None\
            else (True, activePlaylist.getValue())

    @dbusMethod(name=MprisPlayListsMethodId.ACTIVATE_PLAYLIST.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.STRING],
        returnType=DbusPrimitive.NOTHING
    )
    def activatePlaylist(self, playlistId: str) -> None:
        self._adapter.activatePlaylist(playlistId=playlistId)

    @dbusMethod(name=MprisPlayListsMethodId.GET_PLAYLISTS.value)
    @dbusInterfaceSignature(
        argTypes=[
            DbusPrimitive.UINT32,
            DbusPrimitive.UINT32,
            DbusPrimitive.STRING,
            DbusPrimitive.BOOL,
        ],
        returnType=DbusArray(MprisPlaylist.getType())
    )
    def getPlaylists(
        self,
        index: int,
        maxCount: int,
        order: str,
        reverseOrder: bool
    ) -> List[Tuple[str, str, str]]:
        return [
            playList.getValue()
            for playList in self._adapter.getPlaylists(
                index=index,
                maxCount=maxCount,
                order=MprisPlaylistOrdering(order),
                reverseOrder=reverseOrder
            )
        ]
