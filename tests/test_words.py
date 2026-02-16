# tests/test_words.py
from src.word_bot import define_word

def test_serendipity():
    out = define_word("serendipity")
    assert "serendipity" in out
    assert "[definition]" in out

def test_photosynthesis():
    out = define_word("photosynthesis")
    assert "synthesis" in out or "chemical" in out

def test_unknown_word():
    out = define_word("serendipitee")
    assert "No entry found" in out