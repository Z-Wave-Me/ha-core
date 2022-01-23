"""Constants for ZWaveMe."""

from homeassistant.const import Platform

# Base component constants
DOMAIN = "zwave_me"

ZWAVE_PLATFORMS = [
    "switchMultilevel",
    "switchBinary"
]

PLATFORMS = [
    Platform.NUMBER,
    Platform.BINARY_SENSOR
]
