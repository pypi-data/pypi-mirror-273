#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_api.emitter.MprisEmitterBase import MprisEmitterBase
from mpris_api.interface.MprisInterfacePlayer import MprisInterfacePlayer, MprisPlayerPropertyId


class MprisEmitterPlayer(MprisEmitterBase[MprisPlayerPropertyId]):

    def __init__(self, interface: MprisInterfacePlayer) -> None:
        super().__init__(interface=interface)
        self._interface: MprisInterfacePlayer = interface

    def emitSeeked(self, position: int) -> None:
        self._interface.seeked(position=position)
