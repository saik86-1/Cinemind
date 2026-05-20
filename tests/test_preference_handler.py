from agent.preference_handler import (
    PREFERENCE_TYPES,
    MOOD_GENRE_MAP,
    get_follow_up_config,
    build_tmdb_params,
)


def test_preference_types_contains_expected_keys():
    assert "Genre" in PREFERENCE_TYPES
    assert "Actor / Actress" in PREFERENCE_TYPES
    assert "Director" in PREFERENCE_TYPES
    assert "My mood" in PREFERENCE_TYPES
    assert "Hidden gems" in PREFERENCE_TYPES


def test_get_follow_up_config_genre_returns_options():
    config = get_follow_up_config("Genre")
    assert config["type"] == "chips"
    assert "Sci-Fi" in config["options"]
    assert "Thriller" in config["options"]


def test_get_follow_up_config_actor_returns_text_input():
    config = get_follow_up_config("Actor / Actress")
    assert config["type"] == "text"
    assert "placeholder" in config


def test_get_follow_up_config_mood_returns_chips():
    config = get_follow_up_config("My mood")
    assert config["type"] == "chips"
    assert "Feel-good" in config["options"]


def test_build_tmdb_params_genre():
    params = build_tmdb_params(preference_type="Genre", preference_value="Sci-Fi")
    assert params["genre_id"] == 878
    assert params["method"] == "genre"


def test_build_tmdb_params_mood():
    params = build_tmdb_params(preference_type="My mood", preference_value="Feel-good")
    assert params["method"] == "genre"
    assert isinstance(params["genre_id"], int)


def test_build_tmdb_params_actor():
    params = build_tmdb_params(preference_type="Actor / Actress", preference_value="Cate Blanchett")
    assert params["method"] == "person"
    assert params["person_name"] == "Cate Blanchett"


def test_build_tmdb_params_hidden_gems():
    params = build_tmdb_params(preference_type="Hidden gems", preference_value="2010s")
    assert params["method"] == "genre"
    assert params["min_rating"] >= 7.5
