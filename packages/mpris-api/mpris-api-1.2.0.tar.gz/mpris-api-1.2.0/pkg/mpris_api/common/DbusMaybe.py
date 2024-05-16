#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from dataclasses import dataclass
from typing import Any, Optional, Tuple, Type

from mpris_api.common.DbusType import IDbusType


@dataclass
class DbusMaybe(IDbusType):

    def __init__(self, valueSpec: IDbusType) -> None:
        self._valueSpec: IDbusType = valueSpec

    def getSignaturePy(self) -> Optional[Type[Any]]:
        return Tuple[bool, Optional[self._valueSpec.getSignaturePy()]]  # type: ignore

    def getSignatureDbus(self) -> str:
        return f'(b{self._valueSpec.getSignatureDbus()})'
