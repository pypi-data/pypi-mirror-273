#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import no_type_check

from dbus_next import PropertyAccess

from mpris_api.adapter.IMprisAdapterTrackList import IMprisAdapterTrackList
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty, dbusSignal
from mpris_api.common.dbusEnums import DbusMethodId, DbusPropertyId, DbusSignalId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant


class MprisTrackListSignalId(DbusSignalId):
    TRACK_LIST_REPLACED = 'TrackListReplaced'
    TRACK_ADDED = 'TrackAdded'
    TRACK_REMOVED = 'TrackRemoved'
    TRACK_METADATA_CHANGED = 'TrackMetadataChanged'


class MprisTrackListPropertyId(DbusPropertyId):
    TRACKS = 'Tracks'
    CAN_EDIT_TRACKS = 'CanEditTracks'


class MprisTrackListMethodId(DbusMethodId):
    GET_TRACKS_METADATA = 'GetTracksMetadata'
    ADD_TRACK = 'AddTrack'
    REMOVE_TRACK = 'RemoveTrack'
    GO_TO = 'GoTo'


class MprisInterfaceTrackList(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterTrackList) -> None:
        super().__init__(f'{MprisConstant.NAME}.TrackList')
        self._adapter: IMprisAdapterTrackList = adapter

    @dbusSignal(name=MprisTrackListSignalId.TRACK_LIST_REPLACED.value)
    @no_type_check
    def trackListReplaced(self, tracks: DbusType.OBJECT_ARRAY, currentTrack: DbusType.OBJECT) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignalId.TRACK_ADDED.value)
    @no_type_check
    def trackAdded(self, metaData: DbusType.VARIANT_DICT, afterTrack: DbusType.OBJECT) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignalId.TRACK_REMOVED.value)
    @no_type_check
    def trackRemoved(self, trackId: DbusType.OBJECT) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignalId.TRACK_METADATA_CHANGED.value)
    @no_type_check
    def trackMetadataChanged(self, trackId: DbusType.OBJECT, metaData: DbusType.VARIANT_DICT) -> None:
        pass

    @dbusProperty(name=MprisTrackListPropertyId.CAN_EDIT_TRACKS.value, access=PropertyAccess.READ)
    @no_type_check
    def canEditTracks(self) -> DbusType.BOOL:
        return self._adapter.canEditTracks()

    @dbusProperty(name=MprisTrackListPropertyId.TRACKS.value, access=PropertyAccess.READ)
    @no_type_check
    def tracks(self) -> DbusType.OBJECT_ARRAY:
        return [str(track) for track in self._adapter.getTracks()]

    @dbusMethod(name=MprisTrackListMethodId.GET_TRACKS_METADATA.value)
    @no_type_check
    def getTracksMetadata(self, trackIds: DbusType.OBJECT_ARRAY) -> DbusType.VARIANT_DICT_ARRAY:
        metaDataList = self._adapter.getTracksMetadata(trackIds=trackIds)
        return [metaData.toVariantDict() for metaData in metaDataList]

    @dbusMethod(name=MprisTrackListMethodId.ADD_TRACK.value)
    @no_type_check
    def addTrack(self, uri: DbusType.STRING, afterTrack: DbusType.OBJECT, goTo: DbusType.BOOL) -> None:
        afterTrackIdOpt = afterTrack if afterTrack != MprisConstant.NO_TRACK_PATH else None
        self._adapter.addTrack(
            uri=uri,
            afterTrackId=afterTrackIdOpt,
            goTo=goTo
        )

    @dbusMethod(name=MprisTrackListMethodId.REMOVE_TRACK.value)
    @no_type_check
    def removeTrack(self, trackId: DbusType.OBJECT) -> None:
        self._adapter.removeTrack(trackId=trackId)

    @dbusMethod(name=MprisTrackListMethodId.GO_TO.value)
    @no_type_check
    def goTo(self, trackId: DbusType.OBJECT) -> None:
        self._adapter.gotTo(trackId=trackId)
