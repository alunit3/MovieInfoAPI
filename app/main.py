from fastapi import FastAPI
from app.routers import imdb

app = FastAPI(
    title="IMDb API", description="An API for fetching IMDb data.", version="1.0.0"
)

app.include_router(imdb.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the IMDb API!"}
