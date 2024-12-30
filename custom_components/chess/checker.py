"""Quick test to check if the APIs are working."""
import asyncio
from pprint import pprint

import aiohttp
from api import ChessAPI  # Import the API Client

schachbund_pkz = '10221248'
fide_id = '4618378'

async def main():
    """Test the API."""
    async with aiohttp.ClientSession() as session:
        mySchachbund = ChessAPI(session, "schachbund_user", schachbund_pkz)
        schach = await mySchachbund.get_data()
        pprint(schach)


asyncio.run(main())

