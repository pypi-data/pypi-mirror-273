#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys

if sys.version_info >= (3, 11):  # TODO: Remove when support dropped for: Python < 3.11
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return str(self.value)


class DbusEnum(StrEnum):  # TODO: Remove when support dropped for: Python < 3.11
    pass


class DbusSignalId(DbusEnum):
    pass


class DbusPropertyId(DbusEnum):
    pass


class DbusMethodId(DbusEnum):
    pass
