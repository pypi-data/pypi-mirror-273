#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from typing import Generic, List, TypeVar

from mpris_api.common.dbusEnums import DbusPropertyId
from mpris_api.interface.MprisInterfaceBase import MprisInterfaceBase

TDbusPropertyId = TypeVar('TDbusPropertyId', bound=DbusPropertyId)


class MprisEmitterBase(Generic[TDbusPropertyId]):

    def __init__(self, interface: MprisInterfaceBase) -> None:
        self.__interface: MprisInterfaceBase = interface

    def emitPropertyChangeAll(self) -> None:
        self.__interface.emitAll()

    def emitPropertyChange(self, propertyIds: List[TDbusPropertyId]) -> None:
        self.__interface.emitFields(fieldIds=propertyIds)
