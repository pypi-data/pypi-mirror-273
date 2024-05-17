#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from mpris_api.common.DbusObject import DbusObject
from mpris_api.model.MprisConstant import MprisConstant


class MprisTrack:
    NO_TRACK: DbusObject = DbusObject(value=MprisConstant.NO_TRACK_PATH)
    DEFAULT: DbusObject = DbusObject.fromSegments('track', '1')
