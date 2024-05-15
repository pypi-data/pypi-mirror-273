#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

from dbus_next import Variant
from tunit.unit import Microseconds

from mpris_api.common.DbusObject import DbusObject


class MprisMetaDataField:
    TRACK_ID: str = 'mpris:trackid'
    LENGTH: str = 'mpris:length'
    ART_URL: str = 'mpris:artUrl'
    URL: str = 'xesam:url'
    TITLE: str = 'xesam:title'
    ARTIST: str = 'xesam:artist'
    ALBUM: str = 'xesam:album'
    ALBUM_ARTIST: str = 'xesam:albumArtist'
    DISC_NUMBER: str = 'xesam:discNumber'
    TRACK_NUMBER: str = 'xesam:trackNumber'
    COMMENT: str = 'xesam:comment'


META_DATA_TYPES: Dict[str, str] = {
    MprisMetaDataField.TRACK_ID: 'o',
    MprisMetaDataField.LENGTH: 'x',
    MprisMetaDataField.ART_URL: 's',
    MprisMetaDataField.URL: 's',
    MprisMetaDataField.TITLE: 's',
    MprisMetaDataField.ARTIST: 'as',
    MprisMetaDataField.ALBUM: 's',
    MprisMetaDataField.ALBUM_ARTIST: 'as',
    MprisMetaDataField.DISC_NUMBER: 'i',
    MprisMetaDataField.TRACK_NUMBER: 'i',
    MprisMetaDataField.COMMENT: 'as',
}


@dataclass(frozen=True, **({'kw_only': True} if sys.version_info >= (3, 10) else {}))  # TODO: Adjust when support dropped for: Python < 3.10
class MprisMetaData:
    trackId: DbusObject
    length: Optional[Microseconds] = None
    artUrl: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    artists: Optional[List[str]] = None
    album: Optional[str] = None
    albumArtists: Optional[List[str]] = None
    discNumber: Optional[int] = None
    trackNumber: Optional[int] = None
    comments: Optional[List[str]] = None

    def toVariantDict(self) -> Dict[str, Variant]:
        metaDataDict = {
            MprisMetaDataField.TRACK_ID: str(self.trackId),
            MprisMetaDataField.LENGTH: int(self.length) if self.length is not None else None,
            MprisMetaDataField.ART_URL: self.artUrl,
            MprisMetaDataField.URL: self.url,
            MprisMetaDataField.TITLE: self.title,
            MprisMetaDataField.ARTIST: self.artists,
            MprisMetaDataField.ALBUM: self.album,
            MprisMetaDataField.ALBUM_ARTIST: self.albumArtists,
            MprisMetaDataField.DISC_NUMBER: self.discNumber,
            MprisMetaDataField.TRACK_NUMBER: self.trackNumber,
            MprisMetaDataField.COMMENT: self.comments,
        }
        return {
            key: Variant(signature=META_DATA_TYPES[key], value=value)
            for key, value in metaDataDict.items()
            if value is not None
        }
