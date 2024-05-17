#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_api.emitter.MprisEmitterBase import MprisEmitterBase
from mpris_api.interface.MprisInterfaceRoot import MprisInterfaceRoot, MprisRootPropertyId


class MprisEmitterRoot(MprisEmitterBase[MprisRootPropertyId]):

    def __init__(self, interface: MprisInterfaceRoot) -> None:
        super().__init__(interface=interface)
