import aiohttp
from fastapi import Request


async def get_aiohttp_session(request: Request) -> aiohttp.ClientSession:
    """
    Creates an aiohttp ClientSession for each request and ensures it's closed afterwards.
    """
    async with aiohttp.ClientSession() as session:
        yield session
