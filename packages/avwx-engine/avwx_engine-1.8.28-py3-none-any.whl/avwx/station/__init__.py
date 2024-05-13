"""
This module contains station/airport dataclasses and search functions.

For the purposes of AVWX, a station is any physical location that has an ICAO
or GPS identification code. These are usually airports, but smaller locations
might not generate certain report types or defer to larger stations nearby. For
example, small airports with an AWOS system might not send the report to NOAA
or other local authority. They also include remote weather observation stations
not associated with airports like weather buouys.

# Classes

- [avwx.Station](./station/station.html#Station)
"""

from .meta import __LAST_UPDATED__, station_list, uses_na_format, valid_station
from .station import Station, nearest
from .search import search


__all__ = (
    "__LAST_UPDATED__",
    "search",
    "station_list",
    "Station",
    "nearest",
    "uses_na_format",
    "valid_station",
)
