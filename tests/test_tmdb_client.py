import pytest
from unittest.mock import patch, MagicMock
from agent.tmdb_client import (
    get_movies_by_genre,
    search_person,
    get_movies_by_person,
    attach_poster_urls,
    GENRE_IDS,
)


FAKE_MOVIES = [
    {
        "id": 1,
        "title": "Arrival",
        "release_date": "2016-11-11",
        "vote_average": 7.9,
        "vote_count": 12000,
        "popularity": 18.5,
        "overview": "A linguist works with the military.",
        "poster_path": "/poster1.jpg",
        "genre_ids": [878],
    },
    {
        "id": 2,
        "title": "Unknown Gem",
        "release_date": "2012-03-10",
        "vote_average": 8.1,
        "vote_count": 600,
        "popularity": 5.2,
        "overview": "A quiet masterpiece.",
        "poster_path": "/poster2.jpg",
        "genre_ids": [18],
    },
]


@patch("agent.tmdb_client.requests.get")
def test_get_movies_by_genre_returns_list(mock_get):
    mock_get.return_value.json.return_value = {"results": FAKE_MOVIES}
    mock_get.return_value.raise_for_status = MagicMock()

    result = get_movies_by_genre(genre_id=878)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["title"] == "Arrival"


@patch("agent.tmdb_client.requests.get")
def test_get_movies_by_genre_passes_correct_params(mock_get):
    mock_get.return_value.json.return_value = {"results": []}
    mock_get.return_value.raise_for_status = MagicMock()

    get_movies_by_genre(genre_id=53, min_rating=7.5)

    call_params = mock_get.call_args[1]["params"]
    assert call_params["with_genres"] == 53
    assert call_params["vote_average.gte"] == 7.5


@patch("agent.tmdb_client.requests.get")
def test_search_person_returns_id(mock_get):
    mock_get.return_value.json.return_value = {
        "results": [{"id": 99, "name": "Christopher Nolan"}]
    }
    mock_get.return_value.raise_for_status = MagicMock()

    person_id = search_person("Christopher Nolan")
    assert person_id == 99


@patch("agent.tmdb_client.requests.get")
def test_search_person_returns_none_when_not_found(mock_get):
    mock_get.return_value.json.return_value = {"results": []}
    mock_get.return_value.raise_for_status = MagicMock()

    person_id = search_person("Nonexistent Person")
    assert person_id is None


def test_attach_poster_urls_adds_url():
    movies = [{"poster_path": "/abc.jpg", "title": "Test"}]
    result = attach_poster_urls(movies)
    assert result[0]["poster_url"] == "https://image.tmdb.org/t/p/w500/abc.jpg"


def test_attach_poster_urls_handles_missing_poster():
    movies = [{"poster_path": None, "title": "Test"}]
    result = attach_poster_urls(movies)
    assert result[0]["poster_url"] == ""


def test_genre_ids_has_expected_genres():
    assert "Sci-Fi" in GENRE_IDS
    assert "Thriller" in GENRE_IDS
    assert GENRE_IDS["Sci-Fi"] == 878


@patch("agent.tmdb_client.requests.get")
def test_get_movies_by_person_returns_filtered_list(mock_get):
    mock_get.return_value.json.return_value = {
        "cast": [
            {"id": 10, "title": "Good Film", "vote_average": 8.0, "vote_count": 500},
        ],
        "crew": [
            {"id": 20, "title": "Great Film", "vote_average": 8.5, "vote_count": 300},
            {"id": 10, "title": "Good Film", "vote_average": 8.0, "vote_count": 500},  # duplicate
        ],
    }
    mock_get.return_value.raise_for_status = MagicMock()

    result = get_movies_by_person(person_id=99)

    assert len(result) == 2  # duplicate removed
    assert result[0]["title"] == "Great Film"  # sorted by vote_average desc


@patch("agent.tmdb_client.requests.get")
def test_get_movies_by_person_filters_by_min_rating(mock_get):
    mock_get.return_value.json.return_value = {
        "cast": [
            {"id": 1, "title": "Low Rated", "vote_average": 5.0, "vote_count": 200},
            {"id": 2, "title": "High Rated", "vote_average": 8.0, "vote_count": 200},
        ],
        "crew": [],
    }
    mock_get.return_value.raise_for_status = MagicMock()

    result = get_movies_by_person(person_id=99, min_rating=7.0)

    assert len(result) == 1
    assert result[0]["title"] == "High Rated"
