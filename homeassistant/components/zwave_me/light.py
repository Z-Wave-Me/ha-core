"""Representation of an RGB light."""
import logging

from homeassistant.components.light import ATTR_RGB_COLOR, COLOR_MODE_RGB, LightEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import ZWaveMeEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the RGB platform."""

    @callback
    def add_new_device(new_device):
        controller = hass.data[DOMAIN][config_entry.entry_id]
        rgb = ZWaveMeRGB(controller, new_device)

        async_add_entities(
            [
                rgb,
            ]
        )

    config_entry.async_on_unload(
        async_dispatcher_connect(hass, "ZWAVE_ME_NEW_SWITCHRGBW", add_new_device)
    )
    config_entry.async_on_unload(
        async_dispatcher_connect(hass, "ZWAVE_ME_NEW_SWITCHRGB", add_new_device)
    )


class ZWaveMeRGB(ZWaveMeEntity, LightEntity):
    """Representation of a ZWaveMe light."""

    def turn_off(self, **kwargs):
        """Turn the device on."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "off")

    def turn_on(self, **kwargs):
        """Turn the device on."""
        color = kwargs.get(ATTR_RGB_COLOR)

        if color is None:
            color = [122, 122, 122]
        cmd = "exact?red={}&green={}&blue={}".format(*color)
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, cmd)

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.device.level == "on"

    @property
    def brightness(self) -> int:
        """Return the brightness of a device."""
        return max(self.device.color.values())

    @property
    def rgb_color(self) -> tuple[int, int, int]:
        """Return the rgb color value [int, int, int]."""
        rgb = self.device.color
        values = (rgb["r"], rgb["g"], rgb["b"])  # ensure order
        return values

    @property
    def supported_color_modes(self) -> set:
        """Return all color modes."""
        return {COLOR_MODE_RGB}

    @property
    def color_mode(self) -> str:
        """Return current color mode."""
        return COLOR_MODE_RGB
