#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import random
import re
from string import ascii_letters, digits
from typing import Optional, Set

from dbus_next import InvalidObjectPathError, assert_object_path_valid
from unidecode import unidecode


class DbusObjectSpec:

    DEFAULT_RANDOM_NAME_LENGTH: int = 10

    class ValidChars:
        SPACE: str = '_'
        SEPARATOR: str = '/'

        ALPHA: Set[str] = {*ascii_letters}
        NUMERIC: Set[str] = {*digits}
        SPECIAL: Set[str] = {
            SPACE,
            SEPARATOR,
        }
        ALPHA_NUMERIC: Set[str] = ALPHA | NUMERIC
        ALL: Set[str] = ALPHA_NUMERIC | SPECIAL

    @staticmethod
    def assertValid(dbusObj: str) -> None:
        assert_object_path_valid(dbusObj)

    @classmethod
    def sanitize(cls, dbusObj: Optional[str]) -> Optional[str]:
        """
        Sanitizes string to conform with DBus object standard.
        Returns None if input string is None or sanitized string ends up empty.
        """
        if not dbusObj:
            return None

        dbusObj = unidecode(dbusObj)
        dbusObj = cls._ensureSeparatorPrefix(dbusObj=dbusObj)
        dbusObj = cls._replaceWhitespace(dbusObj=dbusObj)
        dbusObj = cls._dropInvalidChars(dbusObj=dbusObj)
        dbusObj = cls._dropDuplicateSeparators(dbusObj=dbusObj)
        dbusObj = cls._dropTrailingSeparator(dbusObj=dbusObj)
        return dbusObj if dbusObj\
            else None

    @classmethod
    def sanitizeOrThrow(cls, dbusObj: Optional[str]) -> str:
        """
        Sanitizes string to conform with DBus object standard.
        Raises `InvalidObjectPathError` if input string is None or sanitized string ends up empty.
        """
        adjustedDbusObj = cls.sanitize(dbusObj=dbusObj)
        if adjustedDbusObj is None:
            raise InvalidObjectPathError(dbusObj)

        return adjustedDbusObj

    @classmethod
    def sanitizeNonNull(cls, dbusObj: Optional[str]) -> str:
        """
        Sanitizes string to conform with DBus object standard.
        Returns random DBus object if input string is None or sanitized string ends up empty.
        """
        dbusObj = cls.sanitize(dbusObj=dbusObj)
        return dbusObj if dbusObj is not None\
            else cls.makeRandom()

    @staticmethod
    def makeRandom(length: int = DEFAULT_RANDOM_NAME_LENGTH) -> str:
        return DbusObjectSpec.ValidChars.SEPARATOR + ''.join(random.choices(
            list(DbusObjectSpec.ValidChars.ALPHA_NUMERIC),
            k=length
        ))

    @staticmethod
    def _dropTrailingSeparator(dbusObj: str) -> str:
        return dbusObj if (
                not dbusObj.endswith(DbusObjectSpec.ValidChars.SEPARATOR)
                or len(dbusObj) == len(DbusObjectSpec.ValidChars.SEPARATOR)
            )\
            else dbusObj[:-1]

    @staticmethod
    def _dropDuplicateSeparators(dbusObj: str) -> str:
        doubleSeparator = ''.join(2*[DbusObjectSpec.ValidChars.SEPARATOR])
        return re.sub(rf'{doubleSeparator}+', DbusObjectSpec.ValidChars.SEPARATOR, dbusObj)

    @staticmethod
    def _dropInvalidChars(dbusObj: str) -> str:
        return ''.join([
            char
            for char in list(dbusObj)
            if char in DbusObjectSpec.ValidChars.ALL
        ])

    @staticmethod
    def _replaceWhitespace(dbusObj: str) -> str:
        return re.sub(r'\s+', DbusObjectSpec.ValidChars.SPACE, dbusObj)

    @staticmethod
    def _ensureSeparatorPrefix(dbusObj: str) -> str:
        return dbusObj if dbusObj.startswith(DbusObjectSpec.ValidChars.SEPARATOR)\
            else f'{DbusObjectSpec.ValidChars.SEPARATOR}{dbusObj}'
