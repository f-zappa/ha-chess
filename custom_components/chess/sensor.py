"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.core_config import Config
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import ChessAPI
from .const import (
    CONF_CHESSCOM,
    CONF_FIDE,
    CONF_ID,
    CONF_LICHESS,
    CONF_SCHACHBUND,
    CONF_TYPE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: Config):
    """Set up integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Initializate entries."""
    if entry.data[CONF_TYPE] not in [CONF_SCHACHBUND, CONF_FIDE, CONF_LICHESS, CONF_CHESSCOM]:
        return False

    client = ChessAPI(CONF_TYPE, CONF_ID)
    coordinator = ChessCoordinator(hass, client)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        ChessPlayerSensor(coordinator, idx) for idx in enumerate(coordinator.data))
    return None


class ChessCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: ChessAPI) -> None:
        """Initialize."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=2),
        )
        self._session = async_get_clientsession(hass)
        self._client = client

    async def _async_setup(self, hass: HomeAssistant):
        pass

    async def _async_update_data(self):
        """Fetch data from schachbund.de."""
        try:
            async with self._session as session:
                return self._client.get_data()

        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}")


class ChessPlayerSensor(CoordinatorEntity, SensorEntity):
    """Schachbund Sensor."""

    def __init__(self, coordinator, pkz) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, context=pkz)
        self._pkz = pkz
        self._state = None

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._state = self.coordinator.data[self._pkz]["state"]
        self.async_write_ha_state()
