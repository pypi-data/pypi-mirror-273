#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import List, Optional, cast

from mpris_api.emitter.MprisEmitterBase import MprisEmitterBase
from mpris_api.emitter.MprisEmitterPlayLists import MprisEmitterPlayLists
from mpris_api.emitter.MprisEmitterPlayer import MprisEmitterPlayer
from mpris_api.emitter.MprisEmitterRoot import MprisEmitterRoot
from mpris_api.emitter.MprisEmitterTrackList import MprisEmitterTrackList


class MprisUpdateNotifier:

    def __init__(
        self,
        emitterRoot: MprisEmitterRoot,
        emitterPlayer: MprisEmitterPlayer,
        emitterTrackList: Optional[MprisEmitterTrackList] = None,
        emitterPlayLists: Optional[MprisEmitterPlayLists] = None
    ) -> None:
        self._emitterRoot: MprisEmitterRoot = emitterRoot
        self._emitterPlayer: MprisEmitterPlayer = emitterPlayer
        self._emitterTrackList: Optional[MprisEmitterTrackList] = emitterTrackList
        self._emitterPlayLists: Optional[MprisEmitterPlayLists] = emitterPlayLists

        self._emitters: List[MprisEmitterBase] = [
            cast(MprisEmitterBase, emitter)
            for emitter in [
                emitterRoot,
                emitterPlayer,
                emitterTrackList,
                emitterPlayLists,
            ]
            if emitter is not None
        ]

    @property
    def emitterRoot(self) -> MprisEmitterRoot:
        return self._emitterRoot

    @property
    def emitterPlayer(self) -> MprisEmitterPlayer:
        return self._emitterPlayer

    @property
    def emitterTrackList(self) -> Optional[MprisEmitterTrackList]:
        return self._emitterTrackList

    @property
    def emitterPlayLists(self) -> Optional[MprisEmitterPlayLists]:
        return self._emitterPlayLists

    def emitPropertyChangeAll(self) -> None:
        for emitter in self._emitters:
            emitter.emitPropertyChangeAll()
