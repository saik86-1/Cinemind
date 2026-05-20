MIN_RATING = 7.5
MIN_VOTES = 500
MAX_POPULARITY = 20.0


def is_hidden_gem(movie: dict) -> bool:
    return (
        movie.get("vote_average", 0) >= MIN_RATING
        and movie.get("vote_count", 0) >= MIN_VOTES
        and movie.get("popularity", 999) <= MAX_POPULARITY
    )


def find_hidden_gem(movies: list[dict]) -> dict | None:
    if not movies:
        return None

    gems = [m for m in movies if is_hidden_gem(m)]

    if gems:
        return min(gems, key=lambda m: m.get("popularity", 999))

    # Fallback: find the lowest-popularity film with at least a 7.0 rating
    quality = [m for m in movies if m.get("vote_average", 0) >= 7.0]
    if not quality:
        return None

    return min(quality, key=lambda m: m.get("popularity", 999))
