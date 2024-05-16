#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from typing import List, Optional

from mpris_api.model.MprisPlaylist import MprisPlaylist
from mpris_api.model.MprisPlaylistOrdering import MprisPlaylistOrdering


class IMprisAdapterPlayLists(ABC):

    @abstractmethod
    def getPlaylistCount(self) -> int: ...
    @abstractmethod
    def getAvailableOrderings(self) -> List[MprisPlaylistOrdering]: ...
    @abstractmethod
    def getActivePlaylist(self) -> Optional[MprisPlaylist]: ...

    @abstractmethod
    def activatePlaylist(self, playlistId: str) -> None: ...
    @abstractmethod
    def getPlaylists(
        self,
        index: int,
        maxCount: int,
        order: MprisPlaylistOrdering,
        reverseOrder: bool
    ) -> List[MprisPlaylist]: ...
