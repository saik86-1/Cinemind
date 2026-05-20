from agent.tmdb_client import GENRE_IDS

PREFERENCE_TYPES = [
    "Genre",
    "Actor / Actress",
    "Director",
    "Story-first",
    "Hidden gems",
    "My mood",
    "Star cast",
]

MOOD_GENRE_MAP = {
    "Something light": {"genre_id": GENRE_IDS["Comedy"], "min_rating": 6.5},
    "Mind-bending": {"genre_id": GENRE_IDS["Sci-Fi"], "min_rating": 7.0},
    "Emotionally heavy": {"genre_id": GENRE_IDS["Drama"], "min_rating": 7.5},
    "Feel-good": {"genre_id": GENRE_IDS["Comedy"], "min_rating": 7.0},
    "Can't sleep": {"genre_id": GENRE_IDS["Horror"], "min_rating": 7.0},
    "Date night": {"genre_id": GENRE_IDS["Romance"], "min_rating": 7.0},
}

STORY_GENRE_MAP = {
    "Mind-bending plot": GENRE_IDS["Thriller"],
    "Character-driven": GENRE_IDS["Drama"],
    "Based on true events": GENRE_IDS["Documentary"],
    "Plot twists": GENRE_IDS["Thriller"],
}

DECADE_MIN_YEAR = {
    "70s–80s": 1970,
    "90s": 1990,
    "2000s": 2000,
    "2010s": 2010,
    "Recent": 2018,
}


def get_follow_up_config(preference_type: str) -> dict:
    if preference_type == "Genre":
        return {
            "type": "chips",
            "label": "Which genre?",
            "options": list(GENRE_IDS.keys()),
        }
    if preference_type in ("Actor / Actress", "Director"):
        label = "Which actor or actress?" if preference_type == "Actor / Actress" else "Which director?"
        return {
            "type": "text",
            "label": label,
            "placeholder": "Type a name, e.g. Cate Blanchett",
        }
    if preference_type == "Story-first":
        return {
            "type": "chips",
            "label": "What kind of story?",
            "options": list(STORY_GENRE_MAP.keys()),
        }
    if preference_type == "Hidden gems":
        return {
            "type": "chips",
            "label": "Which era?",
            "options": list(DECADE_MIN_YEAR.keys()),
        }
    if preference_type == "My mood":
        return {
            "type": "chips",
            "label": "What's the vibe?",
            "options": list(MOOD_GENRE_MAP.keys()),
        }
    if preference_type == "Star cast":
        return {
            "type": "chips",
            "label": "Which genre with great ensemble casts?",
            "options": ["Drama", "Action", "Comedy", "Thriller"],
        }
    return {"type": "chips", "label": "Pick one", "options": []}


def build_tmdb_params(preference_type: str, preference_value: str) -> dict:
    if preference_type == "Genre":
        return {
            "method": "genre",
            "genre_id": GENRE_IDS.get(preference_value, GENRE_IDS["Drama"]),
            "min_rating": 7.0,
        }
    if preference_type in ("Actor / Actress", "Director"):
        return {
            "method": "person",
            "person_name": preference_value,
        }
    if preference_type == "Story-first":
        return {
            "method": "genre",
            "genre_id": STORY_GENRE_MAP.get(preference_value, GENRE_IDS["Drama"]),
            "min_rating": 7.0,
        }
    if preference_type == "Hidden gems":
        return {
            "method": "genre",
            "genre_id": GENRE_IDS["Drama"],
            "min_rating": 7.5,
            "min_year": DECADE_MIN_YEAR.get(preference_value, 2000),
        }
    if preference_type == "My mood":
        mood_config = MOOD_GENRE_MAP.get(
            preference_value,
            {"genre_id": GENRE_IDS["Drama"], "min_rating": 7.0}
        )
        return {"method": "genre", **mood_config}
    if preference_type == "Star cast":
        return {
            "method": "genre",
            "genre_id": GENRE_IDS.get(preference_value, GENRE_IDS["Drama"]),
            "min_rating": 7.0,
        }
    return {"method": "genre", "genre_id": GENRE_IDS["Drama"], "min_rating": 7.0}
