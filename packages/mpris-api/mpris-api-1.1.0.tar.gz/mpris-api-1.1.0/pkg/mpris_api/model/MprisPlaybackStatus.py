#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from enum import Enum


class MprisPlaybackStatus(str, Enum):
    STOPPED = 'Stopped'
    PAUSED = 'Paused'
    PLAYING = 'Playing'
