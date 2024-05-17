#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from dataclasses import dataclass
from typing import Any, Optional, Tuple, Type

from mpris_api.common.DbusType import IDbusType


@dataclass
class DbusMaybe(IDbusType):

    def __init__(self, valueType: IDbusType) -> None:
        self._valueType: IDbusType = valueType

    def getSignaturePy(self) -> Optional[Type[Any]]:
        return Tuple[bool, Optional[self._valueType.getSignaturePy()]]  # type: ignore

    def getSignatureDbus(self) -> str:
        return f'(b{self._valueType.getSignatureDbus()})'
