# CineMind 🎬

A conversational AI agent that helps you discover movies and TV shows through a visual, chat-like experience — with a Netflix-style dark UI.

Unlike Netflix (which recommends based on your watch history) or Google (which returns links), CineMind asks you questions, reasons through real cinema data, and surfaces personalised picks — including at least one hidden gem — with a transparent explanation of why each was chosen.

## Live Demo

[Add your Streamlit Cloud URL here after deployment]

## Features

- **Conversational preference flow** — pick by Genre, Actor, Director, Mood, Hidden gems, and more
- **Real movie data** — powered by the TMDB API (1M+ titles)
- **AI reasoning** — Llama 3.3 70B (via Groq) picks the best matches and writes one-line explanations
- **Hidden gem detection** — always surfaces one underrated film using a data-driven popularity/quality filter
- **Transparent AI** — shows exactly how the agent thought through your recommendation
- **Netflix-style dark UI** — built with Streamlit

## Running Locally

1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file (see `.env.example`):
   ```
   TMDB_API_KEY=your_tmdb_key
   GROQ_API_KEY=your_groq_key
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Getting API Keys (both free)

- **TMDB:** [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
- **Groq:** [console.groq.com](https://console.groq.com)

## Tech Stack

| Layer | Tool |
|---|---|
| UI + deployment | Streamlit + Streamlit Cloud |
| Movie data | TMDB API |
| LLM reasoning | Groq (Llama 3.3 70B) |
| Language | Python 3.11+ |

## Project Structure

```
cinemind/
├── app.py                      # Streamlit entry point
├── agent/
│   ├── tmdb_client.py          # TMDB API wrapper
│   ├── hidden_gem.py           # Hidden gem filter logic
│   ├── preference_handler.py   # Maps user input → TMDB params
│   └── llm_client.py           # Groq LLM wrapper + prompt
├── ui/
│   ├── components.py           # Reusable Streamlit components
│   └── styles.py               # Netflix-style dark theme CSS
└── tests/                      # 28 tests, all passing
```

## Hidden Gem Algorithm

A film qualifies as a hidden gem when:
- `vote_average >= 7.5` (genuinely good)
- `vote_count >= 500` (enough real votes to trust)
- `popularity <= 20.0` (low mainstream visibility on TMDB)

The lowest-popularity film meeting these criteria is always included in results.
