#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Any, List, Optional, Type

from mpris_api.common.DbusType import IDbusType


class DbusArray(IDbusType):

    def __init__(self, itemType: IDbusType) -> None:
        self._itemType: IDbusType = itemType

    def getSignaturePy(self) -> Optional[Type[Any]]:
        return List[self._itemType.getSignaturePy()]  # type: ignore

    def getSignatureDbus(self) -> str:
        return f'a{self._itemType.getSignatureDbus()}'
