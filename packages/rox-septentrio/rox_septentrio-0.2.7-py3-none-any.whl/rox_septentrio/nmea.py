#!/usr/bin/env python3
"""
nmea parser

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

import time
from typing import NamedTuple
import pynmea2
from rox_septentrio.converters import GpsConverter, heading_to_theta

gps_converter = GpsConverter()


class SSN(pynmea2.ProprietarySentence):
    """proprietary message definition"""

    # docs: https://geodesy.noaa.gov/pub/abilich/antcalCorbin/Firmware%20User%20Manual.pdf
    fields = [
        ("no_desc", "_"),
        ("no_desc", "sentence_type"),
        ("no_desc", "timestamp"),
        ("no_desc", "date"),
        ("no_desc", "heading", float),
        ("no_desc", "roll"),
        ("no_desc", "pitch"),
        ("no_desc", "heading_stdev", float),
        ("no_desc", "roll_stdev"),
        ("no_desc", "pitch_stdev"),
        ("no_desc", "sats_used"),
        ("no_desc", "rtk_mode", int),
        ("no_desc", "magnetic_variation"),
        ("no_desc", "mag_var_direction"),
    ]


class PositionData(NamedTuple):
    """latitude and longitude data"""

    lat: float
    lon: float
    x: float
    y: float
    gps_qual: int
    time: str
    ts: float  # system time (epoch)

    def to_dict(self) -> dict:
        return self._asdict()  # type: ignore # pylint: disable=no-member


class HeadingData(NamedTuple):
    """heading data"""

    heading: float
    heading_stdev: float
    theta: float
    ts: float

    def to_dict(self) -> dict:
        return self._asdict()  # type: ignore # pylint: disable=no-member


def timestamp() -> float:
    return round(time.time(), 3)


def parse(txt: str) -> PositionData | HeadingData | None:
    """parse nmea message"""

    if txt.startswith("$PSSN"):
        msg = pynmea2.parse(txt)

        return HeadingData(
            heading=round(msg.heading, 3),  # type: ignore
            heading_stdev=msg.heading_stdev,  # type: ignore
            theta=heading_to_theta(msg.heading),  # type: ignore
            ts=timestamp(),
        )

    elif txt.startswith("$GPGGA"):
        msg = pynmea2.parse(txt)

        x, y = gps_converter.latlon_to_enu((msg.latitude, msg.longitude))  # type: ignore

        return PositionData(
            lat=msg.latitude,  # type: ignore
            lon=msg.longitude,  # type: ignore
            x=round(x, 3),
            y=round(y, 3),
            gps_qual=msg.gps_qual,  # type: ignore
            time=msg.timestamp.strftime("%H:%M:%S.%f"),  # type: ignore
            ts=timestamp(),
        )

    else:
        return None
