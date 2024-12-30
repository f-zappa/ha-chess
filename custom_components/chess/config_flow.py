"""Config flow for the schachbund integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant

# from homeassistant.data_entry_flow import section
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

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


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input is valid."""
    # TODO validate the data can be used to set up a connection.

    # Return info that you want to store in the config entry.
    return {"title": f"Schachbund PKZ {data[CONF_ID]}"}


class SchachbundConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for chess ratings."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle config flow."""
        errors = {}
        _LOGGER.error("User input: %s", user_input)

        if user_input is not None:
            await self.async_set_unique_id(
                user_input[CONF_TYPE] + "_" + user_input[CONF_ID]
            )
            self._abort_if_unique_id_configured()
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"

            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TYPE): SelectSelector(
                        SelectSelectorConfig(
                            options=[CONF_CHESSCOM, CONF_FIDE, CONF_LICHESS, CONF_SCHACHBUND],
                                               mode=SelectSelectorMode.LIST,
                                               translation_key=CONF_TYPE,),
                    ),
                    vol.Required(CONF_ID): str,
                },
            ),
            errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
