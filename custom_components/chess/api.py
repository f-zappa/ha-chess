"""API Client for online chess ratings."""

import asyncio
import logging
import socket

import aiohttp
import phpserialize

from const import CONF_CHESSCOM, CONF_FIDE, CONF_LICHESS, CONF_SCHACHBUND

TIMEOUT = 20


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ChessAPI:
    """Universal API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        type: str = "",  # schachbund, fide, lichess, chesscom
        id: str = "",
    ) -> None:
        """Sample API Client."""
        self._session = session
        self._type = type
        self._id = id

    async def get_data(self):
        """Get data from the API."""
        if self._type == CONF_SCHACHBUND:
            return await self.get_schachbund_data()
        if self._type == CONF_FIDE:
            return await self.get_fide_data()
        if self._type == CONF_LICHESS:
            return await self.get_lichess_data()
        if self._type == CONF_CHESSCOM:
            return await self.get_chesscom_data()
        return False

    async def get_schachbund_data(self):
        """Query the Schachbund API for player data and return as dict."""
        if self._id == '':
            return None
        try:
            url = f"https://www.schachbund.de/php/dewis/spieler.php?pkz={self._id}&format=array"
            response = await self.api_request(url)
            return phpserialize.loads(response, decode_strings=True)
        except (KeyError, TypeError, ValueError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
            _LOGGER.debug(
                "Server response:\n %s"
            )
            return None

    async def api_request(self, url) -> dict:
        """Get data from the API."""

        try:
            async with asyncio.timeout(TIMEOUT):
                response = await self._session.get(url)

        except asyncio.Timeout as exception:
            _LOGGER.error(
                "Timeout error after %s fetching information from %s - %s",
                TIMEOUT,
                url,
                exception,
            )

        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )

        return await response.read()
