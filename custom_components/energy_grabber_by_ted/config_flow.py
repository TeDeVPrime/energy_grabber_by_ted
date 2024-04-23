import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_URL
import logging

_LOGGER = logging.getLogger(__name__)

class GreekEnergyPricesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Energy Grabber by Ted - EGT Monitor."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @staticmethod
    @config_entries.HANDLERS.register(DOMAIN)
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Manage the configuration from the user input."""
        errors = {}
        if user_input is not None:
            url = user_input.get(CONF_URL)
            friendly_name = user_input.get(CONF_NAME, "Default Friendly Name")
            monthly_fee = user_input.get('monthly_fee')

            if await self._test_url(url):
                # If the URL is valid, create the config entry
                return self.async_create_entry(title=friendly_name, data={CONF_URL: url, CONF_NAME: friendly_name, 'monthly_fee': monthly_fee})
            else:
                errors['base'] = 'invalid_url'

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_URL, description="URL of the Energy Price Source"): str,
                vol.Required(CONF_NAME, default="Friendly Name for the sensor", description="Friendly Name for the Sensor"): str,
                vol.Required('monthly_fee', default=5.0): vol.All(vol.Coerce(float), vol.Range(min=0))
            }),
            errors=errors,
            description_placeholders={
                'URL': 'Enter the URL to fetch the energy prices from',
                'Friendly Name': 'Enter a name for this sensor in Home Assistant',
                'Monthly Fee': 'Enter the monthly fee from your provider chosen package.'
            }
        )

    async def _test_url(self, url):
        """Test the URL to see if it can be accessed successfully."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return True
        except Exception as e:
            _LOGGER.error(f"Error accessing URL: {url}, Error: {str(e)}")
            return False

class OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:            
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required('monthly_fee', default=self.config_entry.options.get('monthly_fee', 0.0)): vol.All(vol.Coerce(float), vol.Range(min=0))
            })
        )
