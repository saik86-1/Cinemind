import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# Provide a dummy TMDB_API_KEY so tests that mock requests.get don't fail
# on the _api_key() guard before any real network call is attempted.
os.environ.setdefault("TMDB_API_KEY", "test_dummy")
