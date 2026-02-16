# src/word_bot.py
import nltk
from nltk.corpus import wordnet as wn

# Ensure resources are downloaded [cite: 501]
try:
    wn.synsets('dog')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

def _pos_map(wn_pos):
    """Maps WordNet POS tags to readable names."""
    return {
        'n': 'noun',
        'v': 'verb',
        'a': 'adjective',
        'r': 'adverb',
        's': 'adjective satellite'
    }.get(wn_pos, 'unknown')

def define_word(word: str) -> str:
    """
    Look up a word in WordNet and return a formatted string.
    """
    synsets = wn.synsets(word)
    
    if not synsets:
        return (f"[word]\n{word}\n"
                f"[pos]\nunknown\n"
                f"[definition]\nNo entry found. Check spelling or try a simpler term.")

    # Pick the most frequent synset [cite: 517]
    s = synsets[0]
    
    pos = _pos_map(s.pos())
    definition = s.definition()
    
    # Get examples (limit to 2) [cite: 513]
    examples = s.examples()[:2]
    if examples:
        examples_text = "\n".join(f"- {ex}" for ex in examples)
    else:
        examples_text = "(no example available)"

    # Get synonyms (limit to 3, excluding the word itself) [cite: 513]
    synonyms = sorted(set([l.name().replace('_', ' ') for l in s.lemmas() if l.name().lower() != word.lower()]))[:3]
    synonyms_text = ", ".join(synonyms) if synonyms else "(none)"

    # Pronunciation is N/A for offline WordNet [cite: 516]
    pronunciation = "N/A"

    return (
        f"[word]\n{word}\n"
        f"[pos]\n{pos}\n"
        f"[pronunciation]\n{pronunciation}\n"
        f"[definition]\n{definition}\n"
        f"[examples]\n{examples_text}\n"
        f"[synonyms]\n{synonyms_text}"
    )