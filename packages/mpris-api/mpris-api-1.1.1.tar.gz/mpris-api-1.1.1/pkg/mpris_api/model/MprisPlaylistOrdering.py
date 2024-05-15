#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_api.common.dbusEnums import DbusEnum


class MprisPlaylistOrdering(DbusEnum):
    ALPHABETICAL = 'Alphabetical'
    CREATION_DATE = 'CreationDate'
    MODIFIED_DATE = 'ModifiedDate'
    LAST_PLAY_DATE = 'LastPlayDate'
    USER_DEFINED = 'UserDefined'
