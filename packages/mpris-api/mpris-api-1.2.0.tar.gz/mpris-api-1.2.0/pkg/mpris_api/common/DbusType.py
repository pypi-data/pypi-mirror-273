#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from typing import Any, Optional, Type


class IDbusType(ABC):
    @abstractmethod
    def getSignaturePy(self) -> Optional[Type[Any]]: ...
    @abstractmethod
    def getSignatureDbus(self) -> str: ...


class DbusType(IDbusType):

    def __init__(
        self,
        signaturePy: Optional[Type[Any]],
        signatureDbus: str
    ) -> None:
        self._signaturePy: Optional[Type[Any]] = signaturePy
        self._signatureDbus: str = signatureDbus

    def getSignaturePy(self) -> Optional[Type[Any]]:
        return self._signaturePy

    def getSignatureDbus(self) -> str:
        return self._signatureDbus
