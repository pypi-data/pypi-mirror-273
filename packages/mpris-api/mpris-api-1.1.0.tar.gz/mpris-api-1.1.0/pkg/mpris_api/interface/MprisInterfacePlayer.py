#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import no_type_check

from dbus_next import PropertyAccess
from tunit.unit import Microseconds

from mpris_api.adapter.IMprisAdapterPlayer import IMprisAdapterPlayer
from mpris_api.common.DbusObjectSpec import DbusObjectSpec
from mpris_api.common.DbusType import DbusType
from mpris_api.common.dbusDecorators import dbusMethod, dbusProperty, dbusSignal
from mpris_api.common.dbusEnums import DbusMethodId, DbusPropertyId, DbusSignalId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant
from mpris_api.model.MprisLoopStatus import MprisLoopStatus
from mpris_api.model.MprisMetaData import MprisMetaDataField
from mpris_api.model.MprisPlaybackStatus import MprisPlaybackStatus


class MprisInvalidTrackException(Exception):
    pass


class MprisPlayerSignalId(DbusSignalId):
    SEEKED = 'Seeked'


class MprisPlayerPropertyId(DbusPropertyId):
    CAN_CONTROL = 'CanControl'
    CAN_PLAY = 'CanPlay'
    CAN_PAUSE = 'CanPause'
    CAN_GO_NEXT = 'CanGoNext'
    CAN_GO_PREVIOUS = 'CanGoPrevious'
    CAN_SEEK = 'CanSeek'
    MINIMUM_RATE = 'MinimumRate'
    MAXIMUM_RATE = 'MaximumRate'
    RATE = 'Rate'
    VOLUME = 'Volume'
    METADATA = 'Metadata'
    PLAYBACK_STATUS = 'PlaybackStatus'
    POSITION = 'Position'
    LOOP_STATUS = 'LoopStatus'
    SHUFFLE = 'Shuffle'


class MprisPlayerMethodId(DbusMethodId):
    STOP = 'Stop'
    PLAY = 'Play'
    PAUSE = 'Pause'
    PLAY_PAUSE = 'PlayPause'
    NEXT = 'Next'
    PREVIOUS = 'Previous'
    SEEK = 'Seek'
    SET_POSITION = 'SetPosition'
    OPEN_URI = 'OpenUri'


class MprisInterfacePlayer(MprisInterfaceBase):

    def __init__(self, adapter: IMprisAdapterPlayer) -> None:
        super().__init__(f'{MprisConstant.NAME}.Player')
        self._adapter: IMprisAdapterPlayer = adapter

    @dbusSignal(name=MprisPlayerSignalId.SEEKED.value)
    @no_type_check
    def seeked(self, position: DbusType.INT64) -> None:
        return

    @dbusProperty(name=MprisPlayerPropertyId.CAN_CONTROL.value, access=PropertyAccess.READ)
    @no_type_check
    def canControl(self) -> DbusType.BOOL:
        return self._adapter.canControl()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_PLAY.value, access=PropertyAccess.READ)
    @no_type_check
    def canPlay(self) -> DbusType.BOOL:
        return self._adapter.canPlay()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_PAUSE.value, access=PropertyAccess.READ)
    @no_type_check
    def canPause(self) -> DbusType.BOOL:
        return self._adapter.canPause()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_GO_NEXT.value, access=PropertyAccess.READ)
    @no_type_check
    def canGoNext(self) -> DbusType.BOOL:
        return self._adapter.canGoNext()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_GO_PREVIOUS.value, access=PropertyAccess.READ)
    @no_type_check
    def canGoPrevious(self) -> DbusType.BOOL:
        return self._adapter.canGoPrevious()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_SEEK.value, access=PropertyAccess.READ)
    @no_type_check
    def canSeek(self) -> DbusType.BOOL:
        return self._adapter.canSeek()

    @dbusProperty(name=MprisPlayerPropertyId.MINIMUM_RATE.value, access=PropertyAccess.READ)
    @no_type_check
    def minimumRate(self) -> DbusType.DOUBLE:
        return self._adapter.getMinimumRate()

    @dbusProperty(name=MprisPlayerPropertyId.MAXIMUM_RATE.value, access=PropertyAccess.READ)
    @no_type_check
    def maximumRate(self) -> DbusType.DOUBLE:
        return self._adapter.getMaximumRate()

    @dbusProperty(name=MprisPlayerPropertyId.RATE.value)
    @no_type_check
    def rate(self) -> DbusType.DOUBLE:
        return self._adapter.getRate()

    @rate.setter  # type: ignore
    @no_type_check
    def rate(self, value: DbusType.DOUBLE) -> None:
        self._adapter.setRate(value=value)

    @dbusProperty(name=MprisPlayerPropertyId.VOLUME.value)
    @no_type_check
    def volume(self) -> DbusType.DOUBLE:
        return self._adapter.getVolume()

    @volume.setter  # type: ignore
    @no_type_check
    def volume(self, value: DbusType.DOUBLE) -> None:
        self._adapter.setVolume(value=value)

    @dbusProperty(name=MprisPlayerPropertyId.METADATA.value, access=PropertyAccess.READ)
    @no_type_check
    def metadata(self) -> DbusType.VARIANT_DICT:
        metaData = self._adapter.getMetadata().toVariantDict()
        if metaData[MprisMetaDataField.TRACK_ID] == MprisConstant.NO_TRACK_PATH:
            raise MprisInvalidTrackException(f'Interface cannot return metadata with reserved track ID! trackId="{MprisConstant.NO_TRACK_PATH}"')

        return metaData

    @dbusProperty(name=MprisPlayerPropertyId.PLAYBACK_STATUS.value, access=PropertyAccess.READ)
    @no_type_check
    def playbackStatus(self) -> DbusType.STRING:
        return self._adapter.getPlaybackStatus().value

    @dbusProperty(name=MprisPlayerPropertyId.POSITION.value, access=PropertyAccess.READ)
    @no_type_check
    def position(self) -> DbusType.INT64:
        return int(self._adapter.getPosition())

    @dbusProperty(name=MprisPlayerPropertyId.LOOP_STATUS.value)
    @no_type_check
    def loopStatus(self) -> DbusType.STRING:
        return self._adapter.getLoopStatus().value

    @loopStatus.setter  # type: ignore
    @no_type_check
    def loopStatus(self, value: DbusType.STRING) -> None:
        self._adapter.setLoopStatus(value=MprisLoopStatus(value=value))

    @dbusProperty(name=MprisPlayerPropertyId.SHUFFLE.value)
    @no_type_check
    def shuffle(self) -> DbusType.BOOL:
        return self._adapter.isShuffle()

    @shuffle.setter  # type: ignore
    @no_type_check
    def shuffle(self, value: DbusType.BOOL) -> None:
        self._adapter.setShuffle(value=value)

    @dbusMethod(name=MprisPlayerMethodId.STOP.value)
    @no_type_check
    def stop(self) -> None:
        self._adapter.stop()

    @dbusMethod(name=MprisPlayerMethodId.PLAY.value)
    @no_type_check
    def play(self) -> None:
        self._adapter.play()

    @dbusMethod(name=MprisPlayerMethodId.PAUSE.value)
    @no_type_check
    def pause(self) -> None:
        self._adapter.pause()

    @dbusMethod(name=MprisPlayerMethodId.PLAY_PAUSE.value)
    @no_type_check
    def playPause(self) -> None:
        playbackStatus = self._adapter.getPlaybackStatus()
        if playbackStatus == MprisPlaybackStatus.PLAYING:
            self._adapter.pause()
        else:
            self._adapter.play()

    @dbusMethod(name=MprisPlayerMethodId.NEXT.value)
    @no_type_check
    def next(self) -> None:
        self._adapter.next()

    @dbusMethod(name=MprisPlayerMethodId.PREVIOUS.value)
    @no_type_check
    def previous(self) -> None:
        self._adapter.previous()

    @dbusMethod(name=MprisPlayerMethodId.SEEK.value)
    @no_type_check
    def seek(self, offset: DbusType.INT64) -> None:
        position = self._adapter.getPosition() + offset
        self._adapter.seek(position=position)

    @dbusMethod(name=MprisPlayerMethodId.SET_POSITION.value)
    @no_type_check
    def setPosition(self, trackId: DbusType.OBJECT, position: DbusType.INT64) -> None:
        DbusObjectSpec.assertValid(dbusObj=trackId)
        self._adapter.seek(position=Microseconds(position), trackId=trackId)

    @dbusMethod(name=MprisPlayerMethodId.OPEN_URI.value)
    @no_type_check
    def openUri(self, uri: DbusType.STRING) -> None:
        self._adapter.openUri(uri=uri)
