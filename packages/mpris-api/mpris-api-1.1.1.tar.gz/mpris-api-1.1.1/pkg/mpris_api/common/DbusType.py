#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski


class DbusType:
    BOOL: str = 'b'
    UINT32: str = 'u'
    INT64: str = 'x'
    DOUBLE: str = 'd'

    OBJECT: str = 'o'
    STRING: str = 's'

    VARIANT: str = 'v'

    OBJECT_ARRAY: str = 'ao'
    STRING_ARRAY: str = 'as'
    VARIANT_DICT: str = 'a{sv}'
    VARIANT_DICT_ARRAY: str = 'aa{sv}'
    TUPLE_OSS: str = '(oss)'
    TUPLE_OSS_ARRAY: str = 'a(oss)'
    MAYBE_TUPLE_OSS: str = '(b(oss))'
