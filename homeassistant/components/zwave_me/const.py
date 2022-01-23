"""Constants for ZWaveMe."""

from homeassistant.const import Platform

# Base component constants
DOMAIN = "zwave_me"

ZWAVE_PLATFORMS = ["switchMultilevel", "doorlock"]

PLATFORMS = [Platform.NUMBER, Platform.LOCK]
