DOMAIN = "schachbund"


def setup(hass, config):
    return True


def setup_entry(hass, entry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True


def unload_entry(hass, entry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
