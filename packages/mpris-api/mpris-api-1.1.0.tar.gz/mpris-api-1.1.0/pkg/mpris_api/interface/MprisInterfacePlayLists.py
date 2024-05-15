#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import no_type_check

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterPlayLists import IMprisAdapterPlayLists
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty, dbusSignal
from mpris_api.common.dbusEnums import DbusMethodId, DbusPropertyId, DbusSignalId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant
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
    @no_type_check
    def playlistChanged(self, playlist: DbusType.TUPLE_OSS) -> None:
        pass

    @dbusProperty(name=MprisPlayListsPropertyId.PLAYLIST_COUNT.value, access=PropertyAccess.READ)
    @no_type_check
    def playlistCount(self) -> DbusType.UINT32:
        return self._adapter.getPlaylistCount()

    @dbusProperty(name=MprisPlayListsPropertyId.ORDERINGS.value, access=PropertyAccess.READ)
    @no_type_check
    def orderings(self) -> DbusType.STRING_ARRAY:
        return [ordering.value for ordering in self._adapter.getAvailableOrderings()]

    @dbusProperty(name=MprisPlayListsPropertyId.ACTIVE_PLAYLIST.value, access=PropertyAccess.READ)
    @no_type_check
    def activePlaylist(self) -> DbusType.MAYBE_TUPLE_OSS:
        activePlaylist = self._adapter.getActivePlaylist()
        return (False, None) if activePlaylist is None\
            else (True, activePlaylist.toTuple())

    @dbusMethod(name=MprisPlayListsMethodId.ACTIVATE_PLAYLIST.value)
    @no_type_check
    def activatePlaylist(self, playlistId: DbusType.OBJECT) -> None:
        self._adapter.activatePlaylist(playlistId=playlistId)

    @dbusMethod(name=MprisPlayListsMethodId.GET_PLAYLISTS.value)
    @no_type_check
    def getPlaylists(
        self,
        index: DbusType.UINT32,
        maxCount: DbusType.UINT32,
        order: DbusType.STRING,
        reverseOrder: DbusType.BOOL
    ) -> DbusType.TUPLE_OSS_ARRAY:
        self._adapter.getPlaylists(
            index=index,
            maxCount=maxCount,
            order=MprisPlaylistOrdering(order),
            reverseOrder=reverseOrder
        )
