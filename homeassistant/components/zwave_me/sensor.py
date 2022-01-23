"""Representation of a sensorMultilevel."""
import logging

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import (
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    TEMP_CELSIUS,
)
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import ZWaveMeEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSORS_MAP: dict[str, SensorEntityDescription] = {
    "meterElectric_watt": SensorEntityDescription(
        key="meterElectric_watt",
        device_class=DEVICE_CLASS_POWER,
        native_unit_of_measurement="W",
    ),
    "meterElectric_kilowatt_hour": SensorEntityDescription(
        key="meterElectric_kilowatt_hour",
        device_class=DEVICE_CLASS_ENERGY,
        native_unit_of_measurement="KW/h",
    ),
    "meterElectric_voltage": SensorEntityDescription(
        key="meterElectric_voltage",
        device_class=DEVICE_CLASS_VOLTAGE,
        native_unit_of_measurement="V",
    ),
    "light": SensorEntityDescription(
        key="light",
        device_class=DEVICE_CLASS_ILLUMINANCE,
        native_unit_of_measurement="lx",
    ),
    "noise": SensorEntityDescription(
        key="noise",
        device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
        native_unit_of_measurement="Db",
    ),
    "currentTemperature": SensorEntityDescription(
        key="currentTemperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    "temperature": SensorEntityDescription(
        key="temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
    "generic": SensorEntityDescription(
        key="temperature",
        device_class=DEVICE_CLASS_TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
    ),
}
DEVICE_NAME = "sensorMultilevel"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the number platform."""

    @callback
    def add_new_device(new_device):
        controller = hass.data[DOMAIN][config_entry.entry_id]
        description = get_description(new_device)
        switch = ZWaveMeSensor(controller, new_device, description)

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


class ZWaveMeSensor(ZWaveMeEntity, SensorEntity):
    """Representation of a ZWaveMe sensor."""

    def __init__(self, controller, device, description):
        """Initialize the device."""
        ZWaveMeEntity.__init__(self, controller, device)
        self.entity_description = description

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.device.level
