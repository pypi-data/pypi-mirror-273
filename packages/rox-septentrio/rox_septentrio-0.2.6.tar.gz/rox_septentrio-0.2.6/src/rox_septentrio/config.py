#!/usr/bin/env python3
"""
global configuration

Copyright (c) 2024 ROX Automation - Jev Kuznetsov
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class MqttConfig(BaseSettings):
    """MQTT related settings"""

    model_config = SettingsConfigDict(env_prefix="mqtt_")

    host: str = "localhost"
    port: int = 1883

    position_topic: str = "/gps/position"
    direction_topic: str = "/gps/direction"


class GpsConfig(BaseSettings):
    """gps config"""

    model_config = SettingsConfigDict(env_prefix="gps_")

    port: str = "/dev/gps_nmea"
    baud: int = 115_200
