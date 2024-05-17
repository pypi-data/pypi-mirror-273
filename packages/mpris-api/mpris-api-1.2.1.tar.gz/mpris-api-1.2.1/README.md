[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mpris-api.svg)](https://pypi.python.org/pypi/mpris-api)
[![PyPI version shields.io](https://img.shields.io/pypi/v/mpris-api.svg)](https://pypi.python.org/pypi/apris-api)
[![PyPI license](https://img.shields.io/pypi/l/mpris-api.svg)](https://pypi.python.org/pypi/mpris-api)
[![Downloads](https://static.pepy.tech/badge/mpris-api)](https://pepy.tech/project/mpris-api)

# MPRIS API
---
Make your multimedia app discoverable by linux desktop.

## Desciption

This package provides an implementation of MPRIS DBus interface.

MPRIS standard: [MPRIS D-Bus Interface Specification](https://specifications.freedesktop.org/mpris-spec/latest/)

## Usage

Minimal:
```python
from mpris_api.MprisService import MprisService
from mpris_api.adapter.IMprisAdapterRoot import IMprisAdapterRoot
from mpris_api.adapter.IMprisAdapterPlayer import IMprisAdapterPlayer

class SampleMprisAdapterRoot(IMprisAdapterRoot):
    pass  # TODO: Implement interface methods here!

class SampleMprisAdapterPlayer(IMprisAdapterPlayer):
    pass  # TODO: Implement interface methods here!

with MprisService(
    name='my_app_name',
    adapterRoot=SampleMprisAdapterRoot(),
    adapterPlayer=SampleMprisAdapterPlayer(),
) as mprisService:
    mprisService.awaitStop()
```

Full (including tracklists and playlists support):
```python
from mpris_api.MprisService import MprisService
from mpris_api.adapter.IMprisAdapterRoot import IMprisAdapterRoot
from mpris_api.adapter.IMprisAdapterPlayer import IMprisAdapterPlayer
from mpris_api.adapter.IMprisAdapterTrackList import IMprisAdapterTrackList
from mpris_api.adapter.IMprisAdapterPlayLists import IMprisAdapterPlayLists

class SampleMprisAdapterRoot(IMprisAdapterRoot):
    pass  # TODO: Implement interface methods here!

class SampleMprisAdapterPlayer(IMprisAdapterPlayer):
    pass  # TODO: Implement interface methods here!

class SampleMprisAdapterTrackList(IMprisAdapterTrackList):
    pass  # TODO: Implement interface methods here!

class SampleMprisAdapterPlayLists(IMprisAdapterPlayLists):
    pass  # TODO: Implement interface methods here!

with MprisService(
    name='my_app_name',
    adapterRoot=SampleMprisAdapterRoot(),
    adapterPlayer=SampleMprisAdapterPlayer(),
    adapterTrackList=SampleMprisAdapterTrackList(),
    adapterPlayLists=SampleMprisAdapterPlayLists(),
) as mprisService:
    mprisService.awaitStop()
```

## License
MIT
