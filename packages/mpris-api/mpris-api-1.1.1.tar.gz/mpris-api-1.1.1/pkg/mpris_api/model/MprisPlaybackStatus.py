#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_api.common.dbusEnums import DbusEnum


class MprisPlaybackStatus(DbusEnum):
    STOPPED = 'Stopped'
    PAUSED = 'Paused'
    PLAYING = 'Playing'
