import logging
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_URL
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=6)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor from a config entry."""
    url = entry.data[CONF_URL]
    name = entry.data.get('name', 'Energy Price')
    monthly_fee = entry.data.get('monthly_fee', 0.0)  

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sensor",
        update_method=lambda: fetch_energy_price(hass, url),
        update_interval=SCAN_INTERVAL,
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    # Setup the energy price sensor and the monthly fee sensor
    async_add_entities([
        EnergyPriceSensor(name, coordinator, entry.entry_id),
        MonthlyFeeSensor(name + " Monthly Fee", monthly_fee, entry.entry_id, hass)
    ], True)

class EnergyPriceSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, coordinator, entry_id):
        """Initialize the sensor."""
        self._name = name
        self.coordinator = coordinator
        self._entry_id = entry_id
        

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{self._entry_id}_energy_price"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data

    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "EUR/kWh"


    @property
    def available(self):
        """Return if sensor is available."""
        return self.coordinator.last_update_success

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return 'measurement'

    @property
    def icon(self):
        """Return the icon to be used for this sensor."""
        return "mdi:currency-eur"

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()

class MonthlyFeeSensor(SensorEntity):
    """Representation of a Monthly Fee Sensor."""

    def __init__(self, name, monthly_fee, entry_id, hass):
        """Initialize the monthly fee sensor."""
        self._name = name
        self._monthly_fee = monthly_fee
        self._entry_id = entry_id
        self.hass = hass

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{self._entry_id}_monthly_fee"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._monthly_fee

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "EUR"

    @property
    def icon(self):
        """Return the icon to be used for this sensor."""
        return "mdi:currency-eur"

    

async def fetch_energy_price(hass, url):
    """Fetch the energy price from a specific URL using aiohttp."""
    session = async_get_clientsession(hass)
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            table = soup.find('table', class_='whoplaystable')
            if not table:
                raise UpdateFailed("Table with class 'whoplaystable' not found.")

            rows = table.find_all('tr', class_='linecolor1')
            if not rows:
                raise UpdateFailed("No rows with class 'linecolor1' found.")

            for row in rows:
                cells = row.find_all('td', class_='evtd_numeric')
                if cells:
                    struck_text = cells[0].find('s')
                    if struck_text:
                        # Remove the struck text from the price if it exists
                        price_text = cells[0].text.replace(struck_text.text, '').strip()
                    else:
                        price_text = cells[0].text.strip()

                    # Clean the price text and convert it to a float
                    price_text = price_text.replace('€', '').replace('$', '').replace(',', '.').strip()
                    try:
                        price_float = float(price_text)
                        return price_float
                    except ValueError:
                        _LOGGER.error("Non-numeric price data found: %s", price_text)
                        continue  # If non-numeric, continue with next row
            raise UpdateFailed("Price data not found in rows")
    except Exception as e:
        _LOGGER.error(f"Error fetching data from {url}: {str(e)}")
        raise UpdateFailed from e
