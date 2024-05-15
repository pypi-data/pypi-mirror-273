#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from enum import Enum


class MprisPlaylistOrdering(str, Enum):
    ALPHABETICAL = 'Alphabetical'
    CREATION_DATE = 'CreationDate'
    MODIFIED_DATE = 'ModifiedDate'
    LAST_PLAY_DATE = 'LastPlayDate'
    USER_DEFINED = 'UserDefined'
