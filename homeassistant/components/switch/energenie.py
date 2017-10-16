"""
Support for energenie switches using the pi-mote raspberry pi board

https://energenie4u.co.uk/catalogue/product/ENER314
"""
import logging

import voluptuous as vol

from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_SWITCHES, CONF_ID, CONF_NAME)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['energenie==1.0.1']

SWITCH_SCHEMA = vol.Schema({
    vol.Required(CONF_ID): cv.positive_int,
    vol.Optional(CONF_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_SWITCHES): vol.Schema({cv.string: SWITCH_SCHEMA}),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the energenie switch."""
    switches = config.get(CONF_SWITCHES)
    devices = [
        EnergenieSwitch(
            hass,
            properties.get(CONF_NAME, dev_name),
            properties.get(CONF_ID))
        for (dev_name, properties) in switches.items()
    ]
    add_devices(devices)


class EnergenieSwitch(SwitchDevice):
    """Representation of an Energenie switch."""

    def __init__(self, hass, name, switch_id):
        """Store the name and ID"""
        self._hass = hass
        self._name = name
        self._id = switch_id
        self._state = False

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if we think the switch is on."""
        return self._state

    @property
    def assumed_state(self):
        """Return true because we don't know actual state."""
        return True

    def turn_on(self):
        """Turn the switch on."""
        import energenie
        energenie.switch_on(self._id)
        self._state = True
        self.update_ha_state()

    def turn_off(self):
        """Turn the switch off."""
        import energenie
        energenie.switch_off(self._id)
        self._state = False
        self.update_ha_state()
