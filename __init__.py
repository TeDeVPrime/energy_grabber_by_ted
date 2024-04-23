from homeassistant.core import HomeAssistant
from homeassistant import config_entries
from homeassistant.helpers.dispatcher import async_dispatcher_send
import logging

from .const import DOMAIN, CONF_URL

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Energy Grabber by Ted - EGT component from configuration.yaml (if any)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up Energy Grabber by Ted - EGT from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        'data': entry.data,
        'update_listener': entry.add_update_listener(async_update_options)
    }
    try:
        await hass.config_entries.async_forward_entry_setup(entry, 'sensor')
        _LOGGER.info(f"Energy Grabber by Ted - EGT integration loaded for {entry.title}")
        return True
    except Exception as e:
        _LOGGER.error(f"Failed to set up Energy Grabber by Ted - EGT integration: {str(e)}", exc_info=True)
        return False

async def async_unload_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, 'sensor')
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info(f"Energy Grabber by Ted - EGT integration unloaded for {entry.title}")
    return unload_ok

async def update_listener(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Handle options update."""
    _LOGGER.debug(f"Listener triggered for update on {entry.entry_id}")
    async_dispatcher_send(hass, f"{DOMAIN}_{entry.entry_id}_data_updated")

async def async_update_options(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    """Handle options update."""
    _LOGGER.debug(f"Updating options for entry {entry.entry_id}")
    hass.data[DOMAIN][entry.entry_id]['data'] = entry.data
    async_dispatcher_send(hass, f"{DOMAIN}_{entry.entry_id}_data_updated")
    _LOGGER.debug("Dispatcher signal sent for config entry update")

