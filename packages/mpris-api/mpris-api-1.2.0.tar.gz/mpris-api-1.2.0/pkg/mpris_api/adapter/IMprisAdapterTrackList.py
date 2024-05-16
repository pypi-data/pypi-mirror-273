#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from typing import List, Optional

from mpris_api.model.MprisMetaData import MprisMetaData
from mpris_api.common.DbusObject import DbusObject


class IMprisAdapterTrackList(ABC):

    @abstractmethod
    def getTracksMetadata(self, trackIds: List[str]) -> List[MprisMetaData]: ...
    @abstractmethod
    def addTrack(self, uri: str, goTo: bool = False, afterTrackId: Optional[str] = None) -> None: ...
    @abstractmethod
    def removeTrack(self, trackId: str) -> None: ...
    @abstractmethod
    def gotTo(self, trackId: str) -> None: ...

    @abstractmethod
    def canEditTracks(self) -> bool: ...
    @abstractmethod
    def getTracks(self) -> List[DbusObject]: ...
