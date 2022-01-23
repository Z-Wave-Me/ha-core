"""Representation of a doorlock."""
import logging

from homeassistant.components.lock import LockEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import ZWaveMeEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
DEVICE_NAME = "doorlock"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the lock platform."""

    @callback
    def add_new_device(new_device):
        controller = hass.data[DOMAIN][config_entry.entry_id]
        switch = ZWaveMeLock(controller, new_device)

        async_add_entities(
            [
                switch,
            ]
        )

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass, f"ZWAVE_ME_NEW_{DEVICE_NAME.upper()}", add_new_device
        )
    )


class ZWaveMeLock(ZWaveMeEntity, LockEntity):
    """Representation of a ZWaveMe binary sensor."""

    @property
    def is_locked(self):
        """Return the state of the lock."""
        return self.device.level == "close"

    def unlock(self, **kwargs):
        """Send command to unlock the lock."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "open")

    def lock(self, **kwargs):
        """Send command to unlock the lock."""
        self.hass.data[DOMAIN].zwave_api.send_command(self.device.id, "close")
