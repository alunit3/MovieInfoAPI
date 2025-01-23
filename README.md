#  🎬 MovieInfoAPI: Your Gateway to Movie & Series Data

[![License: MIT](https://img.shields.io/badge/license-CC--BY--SA--4.0-yellow)](https://creativecommons.org/licenses/by-sa/4.0/) 

## 🌟 Overview

Dive into the world of movies and series with the **IMDb API**, a powerful yet simple RESTful API built with **FastAPI**. This API allows you to effortlessly search for movies and TV series on IMDb and retrieve comprehensive data about them, all with a single API call!

## ✨ Features

*   **🎯 Search & Retrieve:** Search IMDb by title and get all the juicy details in a single request.
*   **📦 No-Fuss Structure:** Clean and organized project structure.
*   **🤝 Easy to Use:** Straightforward API endpoints with clear usage instructions.

## 🚀 Getting Started

### Prerequisites

*   Python 3.10 or higher
*   pip

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/alunit3/MovieInfoAPI.git
    cd MovieInfoAPI
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the API

```bash
python run.py
```

This will start the Uvicorn server, typically on `http://localhost:8000`.

## ⚡️ API Usage

### Endpoint: `/imdb/search/`

**Method:** `GET`

**Description:** Searches IMDb by title and returns comprehensive data for the first matching result.

**Parameters:**

*   `title` (required): The title of the movie or TV series to search for.
*   `country_code` (optional): An ISO 3166-1 alpha-2 country code (e.g., "US", "GB", "ID") to get country-specific results like release dates. Defaults to "US".

**Example Request:**

```bash
curl "http://localhost:8000/imdb/search/?title=The%20Matrix%201999&country_code=US"
```

**Example Response:**

```json
{
  "title": "The Matrix",
  "release_year": 1999,
  "release_date": {
    "month": 6,
    "day": 11,
    "year": 1999,
    "country_id": "GB"
  },
  "release_dates": [
    {
      "month": 6,
      "day": 11,
      "year": 1999,
      "country_id": "GB",
      "release_type": null,
      "attributes": []
    }
  ],
  "runtime_seconds": 8160,
  "poster_url": "https://m.media-amazon.com/images/M/...jpg",
  "title_type": {
    "id": "movie",
    "can_have_episodes": false,
    "is_episode": false,
    "is_series": false
  },
  "meter_rank": {
    "current_rank": 154,
    "rank_change": {
      "direction": "UP",
      "difference": 36
    }
  },
  "cast": [
    {
      "name": "Keanu Reeves",
      "character": "Neo",
      "id": "nm0000206",
      "image_url": "https://m.media-amazon.com/images/M/MV5BNDEzOTdhNDUtY2EyMy00YTNmLWE5MjItZmRjMmQzYTRlMGRkXkEyXkFqcGc@._V1_.jpg"
    },
    // ... more cast members
  ]
}
```

### Error Responses

*   **404 Not Found:**
    *   If the title is not found on IMDb.
    *   If data cannot be retrieved for a found IMDb ID.

    ```json
    {
        "detail": "Title not found"
    }
    ```
    or

    ```json
    {
        "detail": "Data not found for IMDb ID: tt1234567"
    }
    ```

## 📁 Project Structure

```
MovieInfoAPI/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and routes
│   ├── dependencies.py  # Dependency injection (session management)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── imdb.py      # IMDb API logic
│   ├── services/
│   │   ├── __init__.py
│   │   └── imdb_service.py # Core IMDb data fetching functions
│   └── utils/
│       ├── __init__.py
│       └── helpers.py   # Helper functions
├── requirements.txt     # Project dependencies
└── run.py               # Uvicorn startup script
```

## 🤝 Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or create a pull request on the repository.

## 📝 License

This project is licensed under the [CC BY-SA 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/) - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

*   [FastAPI](https://fastapi.tiangolo.com/) - For the amazing web framework.
*   [IMDb](https://imdb.com) - For being the source of all this movie data!
