import json
from unittest.mock import patch, MagicMock
from agent.llm_client import rank_and_explain, build_prompt


SAMPLE_MOVIES = [
    {
        "title": "Arrival",
        "release_date": "2016-11-11",
        "vote_average": 7.9,
        "overview": "A linguist works with the military to communicate with aliens.",
    },
    {
        "title": "Ex Machina",
        "release_date": "2014-01-21",
        "vote_average": 7.7,
        "overview": "A programmer interacts with a humanoid robot with AI.",
    },
]

SAMPLE_HIDDEN_GEM = {
    "title": "Coherence",
    "release_date": "2013-06-16",
    "vote_average": 7.2,
    "overview": "Strange things happen during a comet passing.",
}


def test_build_prompt_includes_movie_titles():
    prompt = build_prompt(SAMPLE_MOVIES, "Sci-Fi", SAMPLE_HIDDEN_GEM)
    assert "Arrival" in prompt
    assert "Ex Machina" in prompt


def test_build_prompt_includes_hidden_gem_instruction():
    prompt = build_prompt(SAMPLE_MOVIES, "Sci-Fi", SAMPLE_HIDDEN_GEM)
    assert "Coherence" in prompt
    assert "hidden gem" in prompt.lower()


def test_build_prompt_includes_preference():
    prompt = build_prompt(SAMPLE_MOVIES, "Sci-Fi", None)
    assert "Sci-Fi" in prompt


@patch("agent.llm_client.Groq")
def test_rank_and_explain_returns_list_of_dicts(mock_groq_class):
    fake_response_content = json.dumps([
        {"title": "Arrival", "reason": "Thought-provoking alien contact story."},
        {"title": "Ex Machina", "reason": "Riveting AI thriller with great performances."},
    ])
    mock_client = MagicMock()
    mock_groq_class.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = fake_response_content

    result = rank_and_explain(SAMPLE_MOVIES, "Sci-Fi", SAMPLE_HIDDEN_GEM)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["title"] == "Arrival"
    assert "reason" in result[0]


@patch("agent.llm_client.Groq")
def test_rank_and_explain_calls_groq_with_correct_model(mock_groq_class):
    fake_content = json.dumps([{"title": "Arrival", "reason": "Great."}])
    mock_client = MagicMock()
    mock_groq_class.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[0].message.content = fake_content

    rank_and_explain(SAMPLE_MOVIES, "Sci-Fi", None)

    call_kwargs = mock_client.chat.completions.create.call_args[1]
    assert call_kwargs["model"] == "llama-3.3-70b-versatile"
