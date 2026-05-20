from agent.hidden_gem import find_hidden_gem, is_hidden_gem


MOVIES = [
    {
        "title": "Blockbuster",
        "vote_average": 7.8,
        "vote_count": 50000,
        "popularity": 120.5,
    },
    {
        "title": "Quiet Classic",
        "vote_average": 8.0,
        "vote_count": 800,
        "popularity": 8.3,
    },
    {
        "title": "Mediocre Film",
        "vote_average": 5.9,
        "vote_count": 300,
        "popularity": 4.0,
    },
    {
        "title": "Another Gem",
        "vote_average": 7.6,
        "vote_count": 550,
        "popularity": 12.1,
    },
]


def test_find_hidden_gem_returns_lowest_popularity_high_quality():
    gem = find_hidden_gem(MOVIES)
    assert gem is not None
    assert gem["title"] == "Quiet Classic"


def test_find_hidden_gem_returns_none_for_empty_list():
    assert find_hidden_gem([]) is None


def test_find_hidden_gem_ignores_low_rated_films():
    only_bad = [{"title": "Bad Film", "vote_average": 5.0, "vote_count": 200, "popularity": 2.0}]
    assert find_hidden_gem(only_bad) is None


def test_is_hidden_gem_true_for_valid_film():
    film = {"vote_average": 7.8, "vote_count": 600, "popularity": 9.0}
    assert is_hidden_gem(film) is True


def test_is_hidden_gem_false_for_popular_film():
    film = {"vote_average": 8.0, "vote_count": 10000, "popularity": 95.0}
    assert is_hidden_gem(film) is False


def test_is_hidden_gem_false_for_low_vote_count():
    film = {"vote_average": 8.5, "vote_count": 100, "popularity": 5.0}
    assert is_hidden_gem(film) is False
