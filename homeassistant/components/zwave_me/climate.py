"""Representation of a thermostat."""
import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import ZWaveMeEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
TEMPERATURE_DEFAULT_STEP = 0.5

DEVICE_NAME = "thermostat"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the climate platform."""

    @callback
    def add_new_device(new_device):
        controller = hass.data[DOMAIN][config_entry.entry_id]
        climate = ZWaveMeEntity(controller, new_device)

        async_add_entities(
            [
                climate,
            ]
        )

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass, f"ZWAVE_ME_NEW_{DEVICE_NAME.upper()}", add_new_device
        )
    )


class ZWaveMeClimate(ZWaveMeEntity, ClimateEntity):
    """Representation of a ZWaveMe sensor."""

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        self.hass.data[DOMAIN].zwave_api.send_command(
            self.device.id, "exact?level=" + str(temperature)
        )

    def set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        pass

    @property
    def temperature_unit(self):
        """Return the temperature_unit."""
        return self.device.scaleTitle

    @property
    def target_temperature(self):
        """Return the state of the sensor."""
        return self.device.level

    @property
    def max_temp(self):
        """Return the state of the sensor."""
        return self.device.max

    @property
    def min_temp(self):
        """Return the state of the sensor."""
        return self.device.min

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        modes = [HVAC_MODE_COOL, HVAC_MODE_HEAT]
        return modes

    @property
    def hvac_action(self) -> str:
        """Return the current action."""
        return CURRENT_HVAC_HEAT

    @property
    def hvac_mode(self) -> str:
        """Return the current mode."""
        return HVAC_MODE_HEAT

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return TEMPERATURE_DEFAULT_STEP
