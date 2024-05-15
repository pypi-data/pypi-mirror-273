#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys
from dataclasses import dataclass
from typing import Optional, Tuple

from mpris_api.common.DbusObjectSpec import DbusObjectSpec


@dataclass(frozen=True, **({'kw_only': True} if sys.version_info >= (3, 10) else {}))   # TODO: Adjust when support dropped for: Python < 3.10
class MprisPlaylist:
    playlistId: str
    name: str
    iconUri: Optional[str] = None

    def __post_init__(self) -> None:
        DbusObjectSpec.assertValid(dbusObj=self.playlistId)

    def toTuple(self) -> Tuple[str, str, Optional[str]]:
        return (
            self.playlistId,
            self.name,
            self.iconUri
        )
