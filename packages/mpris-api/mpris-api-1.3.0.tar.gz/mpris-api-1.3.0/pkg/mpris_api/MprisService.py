#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations  # TODO: Remove when support dropped for: Python < ?

import asyncio
import os
import time
from threading import Thread
from types import TracebackType
from typing import Optional, Type

from dbus_next import assert_bus_name_valid
from dbus_next.aio import MessageBus
from tunit.unit import Milliseconds, Seconds

from mpris_api import __logger as logger
from mpris_api.MprisUpdateNotifier import MprisUpdateNotifier
from mpris_api.adapter.IMprisAdapterPlayLists import IMprisAdapterPlayLists
from mpris_api.adapter.IMprisAdapterPlayer import IMprisAdapterPlayer
from mpris_api.adapter.IMprisAdapterRoot import IMprisAdapterRoot
from mpris_api.adapter.IMprisAdapterTrackList import IMprisAdapterTrackList
from mpris_api.emitter.MprisEmitterPlayLists import MprisEmitterPlayLists
from mpris_api.emitter.MprisEmitterPlayer import MprisEmitterPlayer
from mpris_api.emitter.MprisEmitterRoot import MprisEmitterRoot
from mpris_api.emitter.MprisEmitterTrackList import MprisEmitterTrackList
from mpris_api.interface.MprisInterfacePlayLists import MprisInterfacePlayLists
from mpris_api.interface.MprisInterfacePlayer import MprisInterfacePlayer
from mpris_api.interface.MprisInterfaceRoot import MprisInterfaceRoot
from mpris_api.interface.MprisInterfaceTrackList import MprisInterfaceTrackList
from mpris_api.model.MprisConstant import MprisConstant


class MprisService:

    def __init__(
        self,
        name: str,
        adapterRoot: IMprisAdapterRoot,
        adapterPlayer: IMprisAdapterPlayer,
        adapterTrackList: Optional[IMprisAdapterTrackList] = None,
        adapterPlayLists: Optional[IMprisAdapterPlayLists] = None,
    ) -> None:
        assert_bus_name_valid(f'extra_segment_for_validation.{name}')
        self._name: str = f'{MprisConstant.NAME}.{name}.instance{os.getpid()}'

        self._messageBus: Optional[MessageBus] = None

        self._interfaceRoot: MprisInterfaceRoot = MprisInterfaceRoot(adapter=adapterRoot)
        self._interfacePlayer: MprisInterfacePlayer = MprisInterfacePlayer(adapter=adapterPlayer)
        self._interfaceTrackList: Optional[MprisInterfaceTrackList] = None if adapterTrackList is None\
            else MprisInterfaceTrackList(adapter=adapterTrackList)
        self._interfacePlayLists: Optional[MprisInterfacePlayLists] = None if adapterPlayLists is None\
            else MprisInterfacePlayLists(adapter=adapterPlayLists)

        self._emitterRoot: MprisEmitterRoot = MprisEmitterRoot(interface=self._interfaceRoot)
        self._emitterPlayer: MprisEmitterPlayer = MprisEmitterPlayer(interface=self._interfacePlayer)
        self._emitterTrackList: Optional[MprisEmitterTrackList] = None if self._interfaceTrackList is None\
            else MprisEmitterTrackList(interface=self._interfaceTrackList)
        self._emitterPlayLists: Optional[MprisEmitterPlayLists] = None if self._interfacePlayLists is None\
            else MprisEmitterPlayLists(interface=self._interfacePlayLists)

        self._updateNotifier: MprisUpdateNotifier = MprisUpdateNotifier(
            emitterRoot=self._emitterRoot,
            emitterPlayer=self._emitterPlayer,
            emitterTrackList=self._emitterTrackList,
            emitterPlayLists=self._emitterPlayLists,
        )

        self._thread: Optional[Thread] = None

    def __enter__(self) -> MprisService:
        self.start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        self.stop()

    @property
    def isRunning(self) -> bool:
        return (
            self._thread is not None
            and self._thread.is_alive()
        )

    @property
    def updateNotifier(self) -> MprisUpdateNotifier:
        return self._updateNotifier

    def start(self) -> None:
        if self._thread is None:
            self._thread = Thread(
                target=self._run,
                daemon=True,
                name=self.__class__.__name__
            )
            self._thread.start()

    def stop(self) -> None:
        thread = self._thread
        if thread is not None:
            self._disconnect()
            thread.join()
            self._thread = None

    def awaitStop(self, timeout: Optional[Milliseconds] = None) -> bool:
        sleepTime = Milliseconds(100).toRawUnit(unit=Seconds)
        startStamp = time.perf_counter()
        while (
            timeout is None
            or (time.perf_counter() - startStamp) < timeout.toRawUnit(unit=Seconds)
        ):
            if not self.isRunning:
                return True

            time.sleep(sleepTime)

        return False

    def _disconnect(self) -> None:
        try:
            messageBus = self._messageBus
            if messageBus is not None:
                messageBus.disconnect()

        except Exception as ex:
            logger.error(f"Disconnection failed!", exc_info=ex)

    async def _loop(self) -> None:
        try:
            self._messageBus = messageBus = await MessageBus().connect()

            messageBus.export(MprisConstant.PATH, self._interfaceRoot)
            messageBus.export(MprisConstant.PATH, self._interfacePlayer)
            if self._interfaceTrackList:
                messageBus.export(MprisConstant.PATH, self._interfaceTrackList)

            await messageBus.request_name(self._name)

            await messageBus.wait_for_disconnect()

        finally:
            self._disconnect()

    def _run(self) -> None:
        logger.info(f"{self.__class__.__name__} started.")
        try:
            asyncio.run(self._loop())

        finally:
            logger.info(f"{self.__class__.__name__} stopped.")
