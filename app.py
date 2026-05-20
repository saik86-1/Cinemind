import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dotenv import load_dotenv

from agent.preference_handler import PREFERENCE_TYPES, get_follow_up_config, build_tmdb_params
from agent.tmdb_client import get_movies_by_genre, get_movies_by_person, search_person, attach_poster_urls
from agent.hidden_gem import find_hidden_gem
from agent.llm_client import rank_and_explain
from ui.components import (
    inject_styles,
    render_logo,
    render_preference_chips,
    render_follow_up,
    render_movie_card,
    render_reasoning_trail,
)

load_dotenv()

st.set_page_config(
    page_title="CineMind",
    page_icon="▶",
    layout="centered",
)

def init_state():
    defaults = {
        "step": "preference_type",
        "pref_type": None,
        "pref_value": None,
        "results": None,
        "reasoning": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset():
    for key in ["step", "pref_type", "pref_value", "results", "reasoning"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def fetch_movies(params: dict) -> list[dict]:
    if params["method"] == "genre":
        movies = get_movies_by_genre(
            genre_id=params["genre_id"],
            min_rating=params.get("min_rating", 7.0),
        )
    elif params["method"] == "person":
        person_id = search_person(params["person_name"])
        if not person_id:
            return []
        movies = get_movies_by_person(person_id)
    else:
        movies = []

    return attach_poster_urls(movies)


def run_agent(pref_type: str, pref_value: str) -> tuple[list[dict], list[str]]:
    reasoning = []

    params = build_tmdb_params(pref_type, pref_value)
    reasoning.append(f"Preference detected: <strong>{pref_type} → {pref_value}</strong>")

    movies = fetch_movies(params)
    reasoning.append(f"Fetched <strong>{len(movies)} candidates</strong> from TMDB")

    if not movies:
        return [], reasoning

    gem = find_hidden_gem(movies)
    if gem:
        reasoning.append(
            f"Identified hidden gem: <strong>{gem['title']}</strong> "
            f"(rating {gem['vote_average']}, popularity {gem.get('popularity', 0.0):.1f})"
        )
    else:
        reasoning.append("No hidden gem found in this result set — showing top-rated picks")

    preference_label = f"{pref_type}: {pref_value}"
    ranked = rank_and_explain(movies, preference_label, gem)
    reasoning.append(f"LLM selected and explained <strong>{len(ranked)} films</strong>")

    enriched = []
    for item in ranked:
        match = next((m for m in movies if m["title"] == item["title"]), None)
        if match:
            match["llm_reason"] = item["reason"]
            match["is_gem"] = (gem is not None and match["title"] == gem["title"])
            enriched.append(match)

    return enriched, reasoning


def main():
    init_state()
    inject_styles()
    render_logo()

    if st.session_state.step == "preference_type":
        selected = render_preference_chips(PREFERENCE_TYPES, key="pref_type")
        if selected:
            st.session_state.pref_type = selected
            st.session_state.step = "follow_up"
            st.rerun()

    elif st.session_state.step == "follow_up":
        st.markdown(
            f'<div style="color:#aaa; font-size:13px; margin-bottom:16px;">← {st.session_state.pref_type}</div>',
            unsafe_allow_html=True,
        )
        config = get_follow_up_config(st.session_state.pref_type)
        selected = render_follow_up(config, key="pref_value")
        if selected:
            st.session_state.pref_value = selected
            st.session_state.step = "loading"
            st.rerun()

    elif st.session_state.step == "loading":
        with st.spinner("CineMind is thinking..."):
            try:
                results, reasoning = run_agent(
                    st.session_state.pref_type,
                    st.session_state.pref_value,
                )
            except Exception as e:
                results = []
                reasoning = [f"Something went wrong: {e}"]
            st.session_state.results = results
            st.session_state.reasoning = reasoning
            st.session_state.step = "results"
            st.rerun()

    elif st.session_state.step == "results":
        results = st.session_state.results

        if not results:
            st.warning("Couldn't find matches. Try a different preference.")
        else:
            st.markdown(
                f'<div class="cm-section-label">Top picks for you — {st.session_state.pref_value}</div>',
                unsafe_allow_html=True,
            )
            for movie in results:
                render_movie_card(
                    movie,
                    reason=movie.get("llm_reason", ""),
                    is_gem=movie.get("is_gem", False),
                )

        render_reasoning_trail(st.session_state.reasoning)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start over"):
            reset()


if __name__ == "__main__":
    main()
