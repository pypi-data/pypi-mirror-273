#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from abc import ABCMeta
from enum import Enum, EnumMeta

from dbus_next import Variant

from mpris_api.common.DbusType import DbusType


class AbcEnumMeta(EnumMeta, ABCMeta):
    pass


class DbusPrimitive(DbusType, Enum, metaclass=AbcEnumMeta):
    NOTHING = (None, '')
    BOOL = (bool, 'b')
    BYTE = (int, 'y')

    INT16 = (int, 'n')
    UINT16 = (int, 'q')

    INT32 = (int, 'i')
    UINT32 = (int, 'u')

    INT64 = (int, 'x')
    UINT64 = (int, 't')

    DOUBLE = (float, 'd')

    STRING = (str, 's')
    OBJECT = (str, 'o')

    VARIANT = (Variant, 'v')
