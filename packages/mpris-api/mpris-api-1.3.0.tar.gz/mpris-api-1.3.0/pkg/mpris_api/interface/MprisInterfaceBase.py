#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar, cast

from dbus_next.service import (ServiceInterface as DbusServiceInterface)

from mpris_api.common.dbusEnums import DbusPropertyId

T = TypeVar('T')
TDbusPropertyId = TypeVar('TDbusPropertyId', bound=DbusPropertyId)


class IDbusProperty(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def __get__(self, instance: T, owner: Type[T]) -> Any: ...


class MprisInterfaceBase(DbusServiceInterface):

    def emitAll(self) -> None:
        self.emitFields()

    def emitFields(self, fieldIds: Optional[List[TDbusPropertyId]] = None) -> None:
        self._emitFields(fieldDict=self._getProperties(fieldIds=fieldIds))

    def _emitFields(self, fieldDict: Dict[str, Any]) -> None:
        self.emit_properties_changed(
            changed_properties=fieldDict,
            invalidated_properties=[]
        )

    def _getProperties(self, fieldIds: Optional[List[TDbusPropertyId]]) -> Dict[str, Any]:
        fieldNames = [str(fieldId) for fieldId in fieldIds] if fieldIds is not None else None
        properties = cast(List[IDbusProperty], DbusServiceInterface._get_properties(self))
        return {
            prop.name: prop.__get__(self, self.__class__)
            for prop in properties
            if self._shouldGetProperty(prop=prop, names=fieldNames)
        }

    @staticmethod
    def _shouldGetProperty(prop: IDbusProperty, names: Optional[List[str]]) -> bool:
        return (
            names is None
            or prop.name in names
        )
