"""Constants for ZWaveMe."""

from homeassistant.const import Platform

# Base component constants
DOMAIN = "zwave_me"

ZWAVE_PLATFORMS = ["switchMultilevel", "switchRGB", "switchRGBW"]

PLATFORMS = [Platform.NUMBER, Platform.LIGHT]
