#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations  # TODO: Remove when support dropped for: Python < ?

from typing import Any

from mpris_api.common.DbusObjectSpec import DbusObjectSpec
from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.DbusType import IDbusType
from mpris_api.common.IDbusTypeWrapper import IDbusTypeWrapper


class DbusObjectComparisonException(Exception):
    pass


class DbusObject(IDbusTypeWrapper[str]):

    def __init__(self, value: str) -> None:
        self._value: str = DbusObjectSpec.sanitizeOrThrow(dbusObj=value)

    def __eq__(self, other: Any) -> bool:
        return self._value == self._adjustOther(other=other)._value

    def __ne__(self, other: Any) -> bool:
        return self._value != self._adjustOther(other=other)._value

    def __str__(self) -> str:
        return self._value

    @classmethod
    def getType(cls) -> IDbusType:
        return DbusPrimitive.OBJECT

    def getValue(self) -> str:
        return self._value

    @staticmethod
    def _adjustOther(other: Any) -> DbusObject:
        if not isinstance(other, DbusObject):
            raise DbusObjectComparisonException(f'{DbusObject.__name__} can only be compared with another instance of the same type! type(other)="{type(other)}"')
        return other

    @classmethod
    def fromName(cls, name: str) -> DbusObject:
        return cls.fromSegments(name)

    @classmethod
    def makeRandom(cls) -> DbusObject:
        return cls.fromSegments(DbusObjectSpec.makeRandom())

    @classmethod
    def fromSegments(cls, *segments: str) -> DbusObject:
        value = DbusObjectSpec.ValidChars.SEPARATOR + DbusObjectSpec.ValidChars.SEPARATOR.join([
            *segments,
        ])
        return cls(value=value)
