import requests
from homeassistant.helpers.entity import Entity
from datetime import timedelta
import phpserialize

# Define the scan interval
SCAN_INTERVAL = timedelta(minutes=180)


def setup_platform(hass, config, add_entities, discovery_info=None):
    player_id = config.get("player_id")
    add_entities([SchachbundSensor(player_id)])


class SchachbundSensor(Entity):
    def __init__(self, player_id):
        self._player_id = player_id
        self._state = None

    @property
    def name(self):
        return f"Schachbund Player {self._player_id}"

    @property
    def state(self):
        return self._state

    @property
    def should_poll(self):
        return True

    def update(self):
        response = requests.get(
            f"https://www.schachbund.de/php/dewis/"
            f"spieler.php?pkz={self._player_id}&format=array")
        # Convert the PHP array to a Python dictionary
        php_array = phpserialize.loads(response.content, decode_strings=True)
        self._state = php_array['spieler']['dwz']
