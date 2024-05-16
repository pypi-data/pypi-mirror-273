#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Dict, List

from dbus_next import PropertyAccess, Variant

from mpris_api.adapter.IMprisAdapterTrackList import IMprisAdapterTrackList
from mpris_api.common.DbusArray import DbusArray
from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.dbusDecorators import dbusInterfaceSignature, dbusMethod, dbusProperty, dbusSignal
from mpris_api.common.dbusEnums import DbusMethodId, DbusPropertyId, DbusSignalId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant
from mpris_api.model.MprisMetaData import MprisMetaData


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
    @dbusInterfaceSignature(
        argTypes=[DbusArray(DbusPrimitive.OBJECT), DbusPrimitive.OBJECT],
        returnType=DbusPrimitive.NOTHING
    )
    def trackListReplaced(self, tracks: List[str], currentTrack: str) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignalId.TRACK_ADDED.value)
    @dbusInterfaceSignature(
        argTypes=[MprisMetaData.getType(), DbusPrimitive.OBJECT],
        returnType=DbusPrimitive.NOTHING
    )
    def trackAdded(self, metaData: Dict[str, Variant], afterTrack: str) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignalId.TRACK_REMOVED.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.OBJECT],
        returnType=DbusPrimitive.NOTHING
    )
    def trackRemoved(self, trackId: str) -> None:
        pass

    @dbusSignal(name=MprisTrackListSignalId.TRACK_METADATA_CHANGED.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.OBJECT, MprisMetaData.getType()],
        returnType=DbusPrimitive.NOTHING
    )
    def trackMetadataChanged(self, trackId: str, metaData: Dict[str, Variant]) -> None:
        pass

    @dbusProperty(name=MprisTrackListPropertyId.CAN_EDIT_TRACKS.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canEditTracks(self) -> bool:
        return self._adapter.canEditTracks()

    @dbusProperty(name=MprisTrackListPropertyId.TRACKS.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusArray(DbusPrimitive.OBJECT)
    )
    def tracks(self) -> List[str]:
        return [track.getValue() for track in self._adapter.getTracks()]

    @dbusMethod(name=MprisTrackListMethodId.GET_TRACKS_METADATA.value)
    @dbusInterfaceSignature(
        argTypes=[DbusArray(DbusPrimitive.OBJECT)],
        returnType=DbusArray(MprisMetaData.getType())
    )
    def getTracksMetadata(self, trackIds: List[str]) -> List[Dict[str, Variant]]:
        metaDataList = self._adapter.getTracksMetadata(trackIds=trackIds)
        return [metaData.getValue() for metaData in metaDataList]

    @dbusMethod(name=MprisTrackListMethodId.ADD_TRACK.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.STRING, DbusPrimitive.OBJECT, DbusPrimitive.BOOL],
        returnType=DbusPrimitive.NOTHING
    )
    def addTrack(self, uri: str, afterTrack: str, goTo: bool) -> None:
        afterTrackIdOpt = afterTrack if afterTrack != MprisConstant.NO_TRACK_PATH else None
        self._adapter.addTrack(
            uri=uri,
            afterTrackId=afterTrackIdOpt,
            goTo=goTo
        )

    @dbusMethod(name=MprisTrackListMethodId.REMOVE_TRACK.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.OBJECT],
        returnType=DbusPrimitive.NOTHING
    )
    def removeTrack(self, trackId: str) -> None:
        self._adapter.removeTrack(trackId=trackId)

    @dbusMethod(name=MprisTrackListMethodId.GO_TO.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.OBJECT],
        returnType=DbusPrimitive.NOTHING
    )
    def goTo(self, trackId: str) -> None:
        self._adapter.gotTo(trackId=trackId)
