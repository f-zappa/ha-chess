import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN


class SchachbundConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Schachbund", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("player_id"): str,
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SchachbundOptionsFlowHandler(config_entry)


class SchachbundOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "player_id",
                    default=self.config_entry.data.get("player_id")
                ): str,
            })
        )
