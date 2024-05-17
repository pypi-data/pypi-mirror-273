#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_api.emitter.MprisEmitterBase import MprisEmitterBase
from mpris_api.interface.MprisInterfacePlayLists import MprisInterfacePlayLists, MprisPlayListsPropertyId
from mpris_api.model.MprisPlaylist import MprisPlaylist


class MprisEmitterPlayLists(MprisEmitterBase[MprisPlayListsPropertyId]):

    def __init__(self, interface: MprisInterfacePlayLists) -> None:
        super().__init__(interface=interface)
        self._interface: MprisInterfacePlayLists = interface

    def emitPlaylistChanged(self, playlist: MprisPlaylist) -> None:
        self._interface.playlistChanged(playlist=playlist.getValue())
