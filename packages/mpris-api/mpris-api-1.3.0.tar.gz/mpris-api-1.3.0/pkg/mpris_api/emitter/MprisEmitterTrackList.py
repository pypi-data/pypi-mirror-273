#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import List

from mpris_api.common.DbusObject import DbusObject
from mpris_api.emitter.MprisEmitterBase import MprisEmitterBase
from mpris_api.interface.MprisInterfaceTrackList import MprisInterfaceTrackList, MprisTrackListPropertyId
from mpris_api.model.MprisMetaData import MprisMetaData


class MprisEmitterTrackList(MprisEmitterBase[MprisTrackListPropertyId]):

    def __init__(self, interface: MprisInterfaceTrackList) -> None:
        super().__init__(interface=interface)
        self._interface: MprisInterfaceTrackList = interface

    def emitTrackListReplaced(self, tracks: List[DbusObject], currentTrack: DbusObject) -> None:
        self._interface.trackListReplaced(
            tracks=[track.getValue() for track in tracks],
            currentTrack=currentTrack.getValue()
        )

    def emitTrackAdded(self, metaData: MprisMetaData, afterTrack: DbusObject) -> None:
        self._interface.trackAdded(
            metaData=metaData.getValue(),
            afterTrack=afterTrack.getValue()
        )

    def emitTrackRemoved(self, trackId: DbusObject) -> None:
        self._interface.trackRemoved(trackId=trackId.getValue())

    def emitTrackMetadataChanged(self, trackId: DbusObject, metaData: MprisMetaData) -> None:
        self._interface.trackMetadataChanged(
            trackId=trackId.getValue(),
            metaData=metaData.getValue()
        )
