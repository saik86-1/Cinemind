import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

GENRE_IDS = {
    "Action": 28,
    "Comedy": 35,
    "Documentary": 99,
    "Drama": 18,
    "Horror": 27,
    "Romance": 10749,
    "Sci-Fi": 878,
    "Thriller": 53,
}


class TMDBError(Exception):
    """Raised when a TMDB API call fails."""
    pass


def _api_key() -> str:
    key = os.getenv("TMDB_API_KEY")
    if not key:
        raise ValueError("TMDB_API_KEY not set in .env")
    return key


def get_movies_by_genre(
    genre_id: int,
    min_rating: float = 7.0,
    min_votes: int = 200,
    page: int = 1,
) -> list[dict]:
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": _api_key(),
        "with_genres": genre_id,
        "vote_average.gte": min_rating,
        "vote_count.gte": min_votes,
        "sort_by": "vote_average.desc",
        "page": page,
        "language": "en-US",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise TMDBError(str(exc)) from exc
    return response.json().get("results", [])


def search_person(name: str) -> int | None:
    url = f"{TMDB_BASE_URL}/search/person"
    params = {"api_key": _api_key(), "query": name}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise TMDBError(str(exc)) from exc
    results = response.json().get("results", [])
    if not results:
        return None
    top = results[0]
    if top["name"].lower() == name.lower():
        return top["id"]
    # Partial match fallback — still return if the name contains the query
    if name.lower() in top["name"].lower() or top["name"].lower() in name.lower():
        return top["id"]
    return None


def get_movies_by_person(
    person_id: int,
    min_rating: float = 6.5,
    min_votes: int = 100,
) -> list[dict]:
    url = f"{TMDB_BASE_URL}/person/{person_id}/movie_credits"
    params = {"api_key": _api_key(), "language": "en-US"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise TMDBError(str(exc)) from exc
    data = response.json()

    seen = set()
    movies = []
    for credit in data.get("cast", []) + data.get("crew", []):
        mid = credit.get("id")
        if mid in seen:
            continue
        seen.add(mid)
        if (
            credit.get("vote_average", 0) >= min_rating
            and credit.get("vote_count", 0) >= min_votes
        ):
            movies.append(credit)

    movies.sort(key=lambda m: m.get("vote_average", 0), reverse=True)
    return movies


def attach_poster_urls(movies: list[dict]) -> list[dict]:
    for movie in movies:
        path = movie.get("poster_path") or ""
        movie["poster_url"] = f"{TMDB_IMAGE_BASE}{path}" if path else ""
    return movies
