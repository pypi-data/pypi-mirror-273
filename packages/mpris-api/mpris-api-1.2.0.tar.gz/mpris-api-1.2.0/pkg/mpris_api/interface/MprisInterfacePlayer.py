#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Dict

from dbus_next import PropertyAccess, Variant
from tunit.unit import Microseconds

from mpris_api.adapter.IMprisAdapterPlayer import IMprisAdapterPlayer
from mpris_api.common.DbusObjectSpec import DbusObjectSpec
from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.dbusDecorators import dbusInterfaceSignature, dbusMethod, dbusProperty, dbusSignal
from mpris_api.common.dbusEnums import DbusMethodId, DbusPropertyId, DbusSignalId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase
from mpris_api.model.MprisConstant import MprisConstant
from mpris_api.model.MprisLoopStatus import MprisLoopStatus
from mpris_api.model.MprisMetaData import MprisMetaData, MprisMetaDataField
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
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.INT64],
        returnType=DbusPrimitive.NOTHING
    )
    def seeked(self, position: int) -> None:
        return

    @dbusProperty(name=MprisPlayerPropertyId.CAN_CONTROL.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canControl(self) -> bool:
        return self._adapter.canControl()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_PLAY.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canPlay(self) -> bool:
        return self._adapter.canPlay()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_PAUSE.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canPause(self) -> bool:
        return self._adapter.canPause()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_GO_NEXT.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canGoNext(self) -> bool:
        return self._adapter.canGoNext()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_GO_PREVIOUS.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canGoPrevious(self) -> bool:
        return self._adapter.canGoPrevious()

    @dbusProperty(name=MprisPlayerPropertyId.CAN_SEEK.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def canSeek(self) -> bool:
        return self._adapter.canSeek()

    @dbusProperty(name=MprisPlayerPropertyId.MINIMUM_RATE.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.DOUBLE
    )
    def minimumRate(self) -> float:
        return self._adapter.getMinimumRate()

    @dbusProperty(name=MprisPlayerPropertyId.MAXIMUM_RATE.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.DOUBLE
    )
    def maximumRate(self) -> float:
        return self._adapter.getMaximumRate()

    @dbusProperty(name=MprisPlayerPropertyId.RATE.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.DOUBLE
    )
    def rate(self) -> float:
        return self._adapter.getRate()

    @rate.setter  # type: ignore
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.DOUBLE],
        returnType=DbusPrimitive.NOTHING
    )
    def rate(self, value: float) -> None:
        self._adapter.setRate(value=value)

    @dbusProperty(name=MprisPlayerPropertyId.VOLUME.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.DOUBLE
    )
    def volume(self) -> float:
        return self._adapter.getVolume()

    @volume.setter  # type: ignore
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.DOUBLE],
        returnType=DbusPrimitive.NOTHING
    )
    def volume(self, value: float) -> None:
        self._adapter.setVolume(value=value)

    @dbusProperty(name=MprisPlayerPropertyId.METADATA.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=MprisMetaData.getType()
    )
    def metadata(self) -> Dict[str, Variant]:
        metaData = self._adapter.getMetadata().getValue()
        if metaData[MprisMetaDataField.TRACK_ID] == MprisConstant.NO_TRACK_PATH:
            raise MprisInvalidTrackException(f'Interface cannot return metadata with reserved track ID! trackId="{MprisConstant.NO_TRACK_PATH}"')

        return metaData

    @dbusProperty(name=MprisPlayerPropertyId.PLAYBACK_STATUS.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.STRING
    )
    def playbackStatus(self) -> str:
        return self._adapter.getPlaybackStatus().value

    @dbusProperty(name=MprisPlayerPropertyId.POSITION.value, access=PropertyAccess.READ)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.INT64
    )
    def position(self) -> int:
        return int(self._adapter.getPosition())

    @dbusProperty(name=MprisPlayerPropertyId.LOOP_STATUS.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.STRING
    )
    def loopStatus(self) -> str:
        return self._adapter.getLoopStatus().value

    @loopStatus.setter  # type: ignore
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.STRING],
        returnType=DbusPrimitive.NOTHING
    )
    def loopStatus(self, value: str) -> None:
        self._adapter.setLoopStatus(value=MprisLoopStatus(value=value))

    @dbusProperty(name=MprisPlayerPropertyId.SHUFFLE.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.BOOL
    )
    def shuffle(self) -> bool:
        return self._adapter.isShuffle()

    @shuffle.setter  # type: ignore
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.BOOL],
        returnType=DbusPrimitive.NOTHING
    )
    def shuffle(self, value: bool) -> None:
        self._adapter.setShuffle(value=value)

    @dbusMethod(name=MprisPlayerMethodId.STOP.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def stop(self) -> None:
        self._adapter.stop()

    @dbusMethod(name=MprisPlayerMethodId.PLAY.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def play(self) -> None:
        self._adapter.play()

    @dbusMethod(name=MprisPlayerMethodId.PAUSE.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def pause(self) -> None:
        self._adapter.pause()

    @dbusMethod(name=MprisPlayerMethodId.PLAY_PAUSE.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def playPause(self) -> None:
        playbackStatus = self._adapter.getPlaybackStatus()
        if playbackStatus == MprisPlaybackStatus.PLAYING:
            self._adapter.pause()
        else:
            self._adapter.play()

    @dbusMethod(name=MprisPlayerMethodId.NEXT.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def next(self) -> None:
        self._adapter.next()

    @dbusMethod(name=MprisPlayerMethodId.PREVIOUS.value)
    @dbusInterfaceSignature(
        argTypes=[],
        returnType=DbusPrimitive.NOTHING
    )
    def previous(self) -> None:
        self._adapter.previous()

    @dbusMethod(name=MprisPlayerMethodId.SEEK.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.INT64],
        returnType=DbusPrimitive.NOTHING
    )
    def seek(self, offset: int) -> None:
        position = self._adapter.getPosition() + offset
        self._adapter.seek(position=position)

    @dbusMethod(name=MprisPlayerMethodId.SET_POSITION.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.OBJECT, DbusPrimitive.INT64],
        returnType=DbusPrimitive.NOTHING
    )
    def setPosition(self, trackId: str, position: int) -> None:
        DbusObjectSpec.assertValid(dbusObj=trackId)
        self._adapter.seek(position=Microseconds(position), trackId=trackId)

    @dbusMethod(name=MprisPlayerMethodId.OPEN_URI.value)
    @dbusInterfaceSignature(
        argTypes=[DbusPrimitive.STRING],
        returnType=DbusPrimitive.NOTHING
    )
    def openUri(self, uri: str) -> None:
        self._adapter.openUri(uri=uri)
