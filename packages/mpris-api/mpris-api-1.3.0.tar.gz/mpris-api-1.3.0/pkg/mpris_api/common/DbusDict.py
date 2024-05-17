#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Any, Dict, Optional, Type

from mpris_api.common.DbusType import IDbusType


class DbusDict(IDbusType):

    def __init__(
        self,
        keyType: IDbusType,
        valueType: IDbusType
    ) -> None:
        self._keyType: IDbusType = keyType
        self._valueType: IDbusType = valueType

    def getSignaturePy(self) -> Optional[Type[Any]]:
        return Dict[self._keyType.getSignaturePy(), self._valueType.getSignaturePy()]  # type: ignore

    def getSignatureDbus(self) -> str:
        return 'a{%s%s}' % (
            self._keyType.getSignatureDbus(),
            self._valueType.getSignatureDbus()
        )
