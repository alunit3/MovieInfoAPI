import json

import aiohttp
from app.utils.helpers import (
    generate_amazon_session_id,
    get_safe_value,
    parse_release_dates,
)


async def search_imdb(
    session: aiohttp.ClientSession, query: str, country_code: str = "US"
):
    """
    Searches IMDb for a movie/series and returns the IMDb ID of the first result.
    """
    sessionid = generate_amazon_session_id()

    search_headers = {
        "Host": "caching.graphql.imdb.com",
        "X-Apollo-Operation-Id": "9a7f4e7d324a58f47c5f23645232caf60a1c16c3a386f49cd19ab7c6c981b0dd",
        "X-Apollo-Operation-Name": "MainSearchQuery",
        "Accept": "multipart/mixed; deferSpec=20220824, application/json",
        "X-Imdb-Weblab-Treatment-Overrides": '{"IMDB_ANDROID_SEARCH_ALGORITHM_UPDATES_415420":"C"}',
        "X-Imdb-Consent-Info": "e30",
        "X-Imdb-Weblab-Search-Algorithm": "C",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Supreme; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36 IMDb/9.1.2.109120200 (Supreme|Supreme; Android 34; Supreme) IMDb-flg/9.1.2 (1080,2031,403,402) IMDb-var/app-andr-ph",
        "X-Imdb-Client-Name": "imdb-app-android",
        "X-Imdb-Client-Version": "9.1.2.109120200",
        "Content-Type": "application/json",
        "X-Imdb-User-Language": "en-US",
        "X-Imdb-User-Country": country_code,
        "X-Amzn-Sessionid": sessionid,
    }

    search_params = {
        "operationName": "MainSearchQuery",
        "variables": f'{{"first":1,"options":{{"searchTerm":"{query}","type":["TITLE"]}},"knownForLimit":1}}',
        "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"9a7f4e7d324a58f47c5f23645232caf60a1c16c3a386f49cd19ab7c6c981b0dd"}}',
    }

    async with session.get(
        "https://caching.graphql.imdb.com/",
        params=search_params,
        headers=search_headers,
    ) as resp:
        resp.raise_for_status()
        search_data = await resp.json()

        if (
            not search_data
            or "data" not in search_data
            or "mainSearch" not in search_data["data"]
            or "edges" not in search_data["data"]["mainSearch"]
            or not search_data["data"]["mainSearch"]["edges"]
        ):
            print(f"Error: No search results found for query: {query}")
            return None

        first_result = search_data["data"]["mainSearch"]["edges"][0]
        node = first_result.get("node")
        if node and node.get("entity") and node["entity"].get("__typename") == "Title":
            return node["entity"].get("id")
        else:
            print(f"Error: First search result is not a title for query: {query}")
            return None


async def get_imdb_data(
    session: aiohttp.ClientSession, imdb_id: str, country_code: str = "US"
):
    """
    Fetches IMDb data for a given IMDb ID using the GraphQL API.
    """
    sessionid = generate_amazon_session_id()
    metadata_headers = {
        "Host": "caching.graphql.imdb.com",
        "X-Apollo-Operation-Id": "969a32f792c8d7a0dfeda930be9540a38829ca1a000a76a77191755e9022c5e1",
        "X-Apollo-Operation-Name": "TitlesPersistedMetadataQuery",
        "Accept": "multipart/mixed; deferSpec=20220824, application/json",
        "X-Imdb-Consent-Info": "e30",
        "X-Imdb-Weblab-Search-Algorithm": "C",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Supreme; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36 IMDb/9.1.2.109120200 (Supreme|Supreme; Android 34; Supreme) IMDb-flg/9.1.2 (1080,2031,403,402) IMDb-var/app-andr-ph",
        "X-Imdb-Client-Name": "imdb-app-android",
        "X-Imdb-Client-Version": "9.1.2.109120200",
        "Content-Type": "application/json",
        "X-Imdb-User-Language": "en-US",
        "X-Imdb-User-Country": country_code,
        "X-Amzn-Sessionid": sessionid,
    }

    metadata_params = {
        "operationName": "TitlesPersistedMetadataQuery",
        "variables": f'{{"tconsts":["{imdb_id}"],"link":"ANDROID","filter":{{"countries":["{country_code}"],"wideRelease":"WIDE_RELEASE_ONLY"}},"includeWatchOptions":false,"platformId":"ANDROID","numReleaseDates":5}}',
        "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"969a32f792c8d7a0dfeda930be9540a38829ca1a000a76a77191755e9022c5e1"}}',
    }

    async with session.get(
        "https://caching.graphql.imdb.com/",
        params=metadata_params,
        headers=metadata_headers,
    ) as resp:
        resp.raise_for_status()
        metadata_obj = await resp.json()

        if (
            not metadata_obj
            or "data" not in metadata_obj
            or "titles" not in metadata_obj["data"]
            or not metadata_obj["data"]["titles"]
        ):
            print(f"Error: No metadata found for IMDb ID: {imdb_id}")
            return None

        title_data = metadata_obj["data"]["titles"][0]

        cast_data = await get_cast_data(session, imdb_id, sessionid)
        if cast_data:
            title_data["cast"] = cast_data

        parsed_data = {
            "title": get_safe_value(title_data, ["titleText", "text"]),
            "release_year": get_safe_value(title_data, ["releaseYear", "year"]),
            "release_date": {
                "month": get_safe_value(title_data, ["releaseDate", "month"]),
                "day": get_safe_value(title_data, ["releaseDate", "day"]),
                "year": get_safe_value(title_data, ["releaseDate", "year"]),
                "country_id": get_safe_value(
                    title_data, ["releaseDate", "country", "id"]
                ),
            },
            "release_dates": parse_release_dates(title_data),
            "runtime_seconds": get_safe_value(title_data, ["runtime", "seconds"]),
            "poster_url": get_safe_value(title_data, ["primaryImage", "url"]),
            "title_type": {
                "id": get_safe_value(title_data, ["titleType", "id"]),
                "can_have_episodes": get_safe_value(
                    title_data, ["titleType", "canHaveEpisodes"]
                ),
                "is_episode": get_safe_value(title_data, ["titleType", "isEpisode"]),
                "is_series": get_safe_value(title_data, ["titleType", "isSeries"]),
            },
            "meter_rank": {
                "current_rank": get_safe_value(
                    title_data, ["meterRank", "currentRank"]
                ),
                "rank_change": {
                    "direction": get_safe_value(
                        title_data, ["meterRank", "rankChange", "changeDirection"]
                    ),
                    "difference": get_safe_value(
                        title_data, ["meterRank", "rankChange", "difference"]
                    ),
                },
            },
            "cast": get_safe_value(title_data, ["cast"]),
        }

        return parsed_data


async def get_cast_data(session: aiohttp.ClientSession, imdb_id: str, sessionid: str):
    """
    Fetches all cast data (including main cast and other cast) for a given IMDb ID.
    """
    cast_headers = {
        "Host": "caching.graphql.imdb.com",
        "X-Apollo-Operation-Id": "53cd7e947edf8a6a16ef6132e6730f73dbe3f7b9df5660adb0843518caaea68a",
        "X-Apollo-Operation-Name": "TitleTopCastAndCrewQuery",
        "Accept": "multipart/mixed; deferSpec=20220824, application/json",
        "X-Imdb-Consent-Info": "e30",
        "X-Imdb-Weblab-Search-Algorithm": "C",
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Supreme; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36 IMDb/9.1.2.109120200 (Supreme|Supreme; Android 34; Supreme) IMDb-flg/9.1.2 (1080,2031,403,402) IMDb-var/app-andr-ph",
        "X-Imdb-Client-Name": "imdb-app-android",
        "X-Imdb-Client-Version": "9.1.2.109120200",
        "Content-Type": "application/json",
        "X-Imdb-User-Language": "en-US",
        "X-Imdb-User-Country": "US",
        "X-Amzn-Sessionid": sessionid,
    }

    cast_params = {
        "operationName": "TitleTopCastAndCrewQuery",
        "variables": f'{{"id":"{imdb_id}"}}',
        "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"53cd7e947edf8a6a16ef6132e6730f73dbe3f7b9df5660adb0843518caaea68a"}}',
    }

    async with session.get(
        "https://caching.graphql.imdb.com/", params=cast_params, headers=cast_headers
    ) as resp:
        resp.raise_for_status()
        cast_data = await resp.json()

        if not cast_data or "data" not in cast_data or "title" not in cast_data["data"]:
            print(f"Error: No cast data found for IMDb ID: {imdb_id}")
            return None

        cast_credits = []

        # Get main cast from principalCredits
        for group in get_safe_value(cast_data, ["data", "title", "principalCredits"]):
            for credit in get_safe_value(group, ["credits"]):
                if get_safe_value(credit, ["__typename"]) == "Cast":
                    cast_member = {
                        "name": get_safe_value(credit, ["name", "nameText", "text"]),
                        "character": get_safe_value(credit, ["characters", 0, "name"]),
                        "id": get_safe_value(credit, ["name", "id"]),
                        "image_url": get_safe_value(
                            credit, ["name", "primaryImage", "url"]
                        ),
                    }
                    cast_credits.append(cast_member)

        # Get other cast from credits
        edges = get_safe_value(cast_data, ["data", "title", "credits", "edges"])
        if edges:
            for edge in edges:
                node = get_safe_value(edge, ["node"])
                if node and get_safe_value(node, ["__typename"]) == "Cast":
                    cast_member = {
                        "name": get_safe_value(node, ["name", "nameText", "text"]),
                        "character": get_safe_value(node, ["characters", 0, "name"]),
                        "id": get_safe_value(node, ["name", "id"]),
                        "image_url": get_safe_value(
                            node, ["name", "primaryImage", "url"]
                        ),
                    }
                    # Avoid duplicates (in case a cast member is in both lists)
                    if cast_member not in cast_credits:
                        cast_credits.append(cast_member)

        return cast_credits
