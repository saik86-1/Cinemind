import os
import re
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


def build_prompt(movies: list[dict], preference_label: str, hidden_gem: dict | None) -> str:
    movie_list = "\n".join([
        f"{i + 1}. {m['title']} ({m.get('release_date', '')[:4]}) "
        f"— Rating: {m['vote_average']}/10 — {m.get('overview', '')[:120]}"
        for i, m in enumerate(movies[:20])
    ])

    hidden_gem_note = ""
    if hidden_gem:
        hidden_gem_note = (
            f"\nIMPORTANT: '{hidden_gem['title']}' is a hidden gem — "
            f"you MUST include it in your picks and explain why it's underrated.\n"
        )

    return f"""You are a world-class film curator helping someone find what to watch tonight.

User preference: {preference_label}
{hidden_gem_note}
From this list of films, pick the 5 best matches. For each, write ONE sentence (max 15 words) explaining why it fits the user's preference.

Films:
{movie_list}

Respond ONLY with a valid JSON array, no extra text:
[{{"title": "exact film title from the list", "reason": "one sentence explanation"}}]"""


def rank_and_explain(
    movies: list[dict],
    preference_label: str,
    hidden_gem: dict | None,
) -> list[dict]:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = build_prompt(movies, preference_label, hidden_gem)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences robustly
    raw = re.sub(r"```(?:json)?\s*", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # LLM returned malformed JSON — return empty list so the app degrades gracefully
        return []
