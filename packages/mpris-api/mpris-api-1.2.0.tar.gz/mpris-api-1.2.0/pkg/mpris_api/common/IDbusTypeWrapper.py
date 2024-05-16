#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from mpris_api.common.DbusType import IDbusType

T = TypeVar('T')


class IDbusTypeWrapper(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def getType(cls) -> IDbusType: ...
    @abstractmethod
    def getValue(self) -> T: ...
