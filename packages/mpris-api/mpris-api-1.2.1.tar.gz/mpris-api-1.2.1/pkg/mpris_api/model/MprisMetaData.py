#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

from dbus_next import Variant
from tunit.unit import Microseconds

from mpris_api.common.DbusArray import DbusArray
from mpris_api.common.DbusDict import DbusDict
from mpris_api.common.DbusObject import DbusObject
from mpris_api.common.DbusPrimitive import DbusPrimitive
from mpris_api.common.DbusType import IDbusType
from mpris_api.common.IDbusTypeWrapper import IDbusTypeWrapper


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


META_DATA_TYPES: Dict[str, IDbusType] = {
    MprisMetaDataField.TRACK_ID: DbusPrimitive.OBJECT,
    MprisMetaDataField.LENGTH: DbusPrimitive.INT64,
    MprisMetaDataField.ART_URL: DbusPrimitive.STRING,
    MprisMetaDataField.URL: DbusPrimitive.STRING,
    MprisMetaDataField.TITLE: DbusPrimitive.STRING,
    MprisMetaDataField.ARTIST: DbusArray(DbusPrimitive.STRING),
    MprisMetaDataField.ALBUM: DbusPrimitive.STRING,
    MprisMetaDataField.ALBUM_ARTIST: DbusArray(DbusPrimitive.STRING),
    MprisMetaDataField.DISC_NUMBER: DbusPrimitive.INT32,
    MprisMetaDataField.TRACK_NUMBER: DbusPrimitive.INT32,
    MprisMetaDataField.COMMENT: DbusArray(DbusPrimitive.STRING),
}


@dataclass(frozen=True, **({'kw_only': True} if sys.version_info >= (3, 10) else {}))  # TODO: Adjust when support dropped for: Python < 3.10
class MprisMetaData(IDbusTypeWrapper[Dict[str, Variant]]):

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

    @classmethod
    def getType(cls) -> IDbusType:
        return DbusDict(
            keyType=DbusPrimitive.STRING,
            valueType=DbusPrimitive.VARIANT
        )

    def getValue(self) -> Dict[str, Variant]:
        metaDataDict = {
            MprisMetaDataField.TRACK_ID: self.trackId.getValue(),
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
            key: Variant(
                signature=META_DATA_TYPES[key].getSignatureDbus(),
                value=value
            )
            for key, value in metaDataDict.items()
            if value is not None
        }
