#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from enum import Enum


class MprisLoopStatus(str, Enum):
    NONE = 'None'
    TRACK = 'Track'
    PLAYLIST = 'Playlist'
