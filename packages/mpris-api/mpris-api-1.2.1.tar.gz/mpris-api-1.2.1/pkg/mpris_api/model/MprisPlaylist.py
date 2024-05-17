#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys
from dataclasses import dataclass
from typing import Tuple

from mpris_api.common.DbusObjectSpec import DbusObjectSpec
from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.DbusTuple import DbusTuple
from mpris_api.common.DbusType import IDbusType
from mpris_api.common.IDbusTypeWrapper import IDbusTypeWrapper


@dataclass(frozen=True, **({'kw_only': True} if sys.version_info >= (3, 10) else {}))   # TODO: Adjust when support dropped for: Python < 3.10
class MprisPlaylist(IDbusTypeWrapper[Tuple[str, str, str]]):
    playlistId: str
    name: str
    iconUri: str = ''

    def __post_init__(self) -> None:
        DbusObjectSpec.assertValid(dbusObj=self.playlistId)

    @classmethod
    def getType(cls) -> IDbusType:
        return DbusTuple(
            DbusPrimitive.OBJECT,
            DbusPrimitive.STRING,
            DbusPrimitive.STRING,
        )

    def getValue(self) -> Tuple[str, str, str]:
        return (
            self.playlistId,
            self.name,
            self.iconUri
        )
