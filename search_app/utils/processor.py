import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9']+")


def normalize_token(token):
    return token.lower().strip("'")


def tokenize(text):
    if not text:
        return []

    tokens = []
    for token in _TOKEN_RE.findall(text.lower()):
        cleaned = normalize_token(token)
        if cleaned:
            tokens.append(cleaned)
    return tokens


def term_counts(text):
    return Counter(tokenize(text))
