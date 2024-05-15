#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys

if sys.version_info >= (3, 11):  # TODO: Adjust when support dropped for: Python < 3.11
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        def __str__(self) -> str:
            return str(self.value)


class DbusSignalId(StrEnum):
    pass


class DbusPropertyId(StrEnum):
    pass


class DbusMethodId(StrEnum):
    pass
