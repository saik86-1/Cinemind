import streamlit as st
from ui.styles import DARK_CSS


def inject_styles():
    st.markdown(DARK_CSS, unsafe_allow_html=True)


def render_logo():
    st.markdown('<div class="cm-logo">▶ CineMind</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="cm-tagline">Your personal film curator — tell us your mood, we find your movie.</div>',
        unsafe_allow_html=True,
    )


def render_preference_chips(options: list[str], key: str) -> str | None:
    st.markdown('<div class="cm-question">What are you in the mood for?</div>', unsafe_allow_html=True)
    st.markdown('<div class="cm-subtext">Pick one to begin</div>', unsafe_allow_html=True)

    cols = st.columns(min(len(options), 4))
    for i, option in enumerate(options):
        col = cols[i % len(cols)]
        with col:
            if st.button(option, key=f"{key}_{i}"):
                return option
    return None


def render_follow_up(config: dict, key: str) -> str | None:
    st.markdown(f'<div class="cm-question">{config["label"]}</div>', unsafe_allow_html=True)

    if config["type"] == "chips":
        options = config["options"]
        cols = st.columns(min(len(options), 4))
        for i, option in enumerate(options):
            col = cols[i % len(cols)]
            with col:
                if st.button(option, key=f"{key}_{i}"):
                    return option
    elif config["type"] == "text":
        value = st.text_input("", placeholder=config.get("placeholder", ""), key=key)
        if st.button("Search →", key=f"{key}_submit") and value:
            return value

    return None


def render_movie_card(movie: dict, reason: str, is_gem: bool = False):
    title = movie.get("title", "Unknown")
    year = movie.get("release_date", "")[:4]
    rating = movie.get("vote_average", 0)
    poster_url = movie.get("poster_url", "")

    col1, col2 = st.columns([1, 3])

    with col1:
        if poster_url:
            st.image(poster_url, width=100)
        else:
            st.markdown("🎬", unsafe_allow_html=False)

    with col2:
        badges = f'<span class="cm-rating">★ {rating:.1f}</span>'
        if is_gem:
            badges += ' <span class="cm-gem-badge">Hidden gem</span>'

        st.markdown(
            f"""
            <div class="cm-card">
                <div class="cm-card-title">{title}</div>
                <div class="cm-card-meta">{year} &nbsp;·&nbsp; {badges}</div>
                <div class="cm-card-reason">{reason}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_reasoning_trail(steps: list[str]):
    steps_html = "".join(
        f'<div class="cm-step"><strong>{i + 1}.</strong> {step}</div>'
        for i, step in enumerate(steps)
    )
    st.markdown(
        f"""
        <div class="cm-section-label">How the agent thought</div>
        <div class="cm-reasoning">{steps_html}</div>
        """,
        unsafe_allow_html=True,
    )
