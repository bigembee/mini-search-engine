import re
from collections import Counter
from difflib import get_close_matches

_TOKEN_RE = re.compile(r"[a-z0-9']+")

# Common words used to check spelling
DICTIONARY = {
    "hello", "world", "python", "programming", "computer",
    "apple", "banana", "orange", "good", "bad", "book",
    "school", "student", "teacher", "love", "happy",
    "beautiful", "friend", "people", "language", "test",
    "cat", "dog", "run", "running", "great", "is", "are",
    "the", "this", "that", "and", "you", "he", "she"
}


def normalize_token(token):
    return token.lower().strip("'")


def correct_spelling(token):
    if token in DICTIONARY:
        return token

    matches = get_close_matches(
        token, DICTIONARY, n=1, cutoff=0.8
    )

    if matches:
        return matches[0]

    return token


def tokenize(text):
    if not text:
        return []

    tokens = []

    for token in _TOKEN_RE.findall(text.lower()):
        cleaned = normalize_token(token)

        if cleaned:
            corrected = correct_spelling(cleaned)
            tokens.append(corrected)

    return tokens


def term_counts(text):
    return Counter(tokenize(text))
