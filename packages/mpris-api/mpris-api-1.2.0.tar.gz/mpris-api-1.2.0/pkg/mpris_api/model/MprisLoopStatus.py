#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_api.common.dbusEnums import DbusEnum


class MprisLoopStatus(DbusEnum):
    NONE = 'None'
    TRACK = 'Track'
    PLAYLIST = 'Playlist'
