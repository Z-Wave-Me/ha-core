"""Representation of a switchBinary."""
import logging

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_MOTION,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import ZWaveMeEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSORS_MAP: dict[str, BinarySensorEntityDescription] = {
    "generic": BinarySensorEntityDescription(
        key="motion",
        device_class=DEVICE_CLASS_MOTION,
    ),
    "motion": BinarySensorEntityDescription(
        key="motion",
        device_class=DEVICE_CLASS_MOTION,
    ),
}
DEVICE_NAME = "sensorBinary"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the sensor platform."""

    @callback
    def add_new_device(new_device):
        controller = hass.data[DOMAIN][config_entry.entry_id]
        description = get_description(new_device)
        switch = ZWaveMeBinarySensor(controller, new_device, description)

        async_add_entities(
            [
                switch,
            ]
        )

    @callback
    def get_description(new_device):
        if new_device.probeType in SENSORS_MAP:
            description = SENSORS_MAP.get(new_device.probeType)
        else:
            description = SENSORS_MAP["generic"]
        return description

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass, f"ZWAVE_ME_NEW_{DEVICE_NAME.upper()}", add_new_device
        )
    )


class ZWaveMeBinarySensor(ZWaveMeEntity, BinarySensorEntity):
    """Representation of a ZWaveMe binary sensor."""

    def __init__(self, controller, device, description):
        """Initialize the device."""
        ZWaveMeEntity.__init__(self, controller, device)
        self.entity_description = description

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return self.device.level == "on"
