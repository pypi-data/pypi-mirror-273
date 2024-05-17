#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Any, List, Optional, Tuple, Type

from mpris_api.common.DbusType import IDbusType


class DbusTuple(IDbusType):

    def __init__(self, *itemType: IDbusType) -> None:
        self._itemTypes: List[IDbusType] = list(itemType)

    def getSignaturePy(self) -> Optional[Type[Any]]:
        itemSignatures = tuple([
            itemType.getSignaturePy()
            for itemType in self._itemTypes
        ])
        return Tuple[itemSignatures]  # type: ignore

    def getSignatureDbus(self) -> str:
        itemSignatures = ''.join([
            itemType.getSignatureDbus()
            for itemType in self._itemTypes
        ])
        return f'({itemSignatures})'
