from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_aiohttp_session
from app.services.imdb_service import search_imdb, get_imdb_data
import aiohttp

router = APIRouter(
    prefix="/imdb",
    tags=["imdb"],
)


@router.get("/search/")
async def search_by_title(
    title: str,
    country_code: str = "US",
    session: aiohttp.ClientSession = Depends(get_aiohttp_session),
):
    """
    Searches IMDb by title and returns the full data of the first result.
    """
    imdb_id = await search_imdb(session, title, country_code)
    if imdb_id:
        data = await get_imdb_data(session, imdb_id, country_code)
        if data:
            return data
        else:
            raise HTTPException(
                status_code=404, detail=f"Data not found for IMDb ID: {imdb_id}"
            )
    else:
        raise HTTPException(status_code=404, detail="Title not found")
