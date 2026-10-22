import re
from collections import Counter
from difflib import get_close_matches

_TOKEN_RE = re.compile(r"[a-z0-9']+")

# Fallback vocabulary for common search terms. The real matching is stronger when
# the system compares against the actual indexed document terms.
DICTIONARY = {
    "django", "react", "javascript", "java", "sql", "postgres",
    "database", "backend", "frontend", "api", "developer",
    "software", "engineer", "design", "machine", "learning",
    "data", "science", "mobile", "cloud", "security",
    "good", "head", "python", "programming", "golden"
}


def normalize_token(token):
    if token is None:
        return ""

    token = str(token).lower().strip()
    token = token.strip("'")
    token = re.sub(r"\s+", "", token)
    return token


def _remove_repeated_trailing_chars(token):
    if len(token) < 3:
        return token

    while len(token) > 1 and token[-1] == token[-2]:
        token = token[:-1]

    return token


def correct_spelling(token, vocabulary=None):
    token = normalize_token(token)
    if not token:
        return ""

    known_terms = set(normalize_token(item) for item in (vocabulary or DICTIONARY) if item)
    if token in known_terms:
        return token

    candidate = _remove_repeated_trailing_chars(token)
    if candidate in known_terms:
        return candidate

    matches = get_close_matches(token, sorted(known_terms), n=1, cutoff=0.72)
    if matches:
        return matches[0]

    return token


def _token_variants(tokens):
    variants = set()
    for index in range(len(tokens) - 1):
        left, right = tokens[index], tokens[index + 1]
        variants.add(left + right)
        variants.add(right + left)
    return sorted(variants)


def tokenize(text, vocabulary=None):
    if not text:
        return []

    raw_tokens = [normalize_token(token) for token in _TOKEN_RE.findall(text.lower()) if normalize_token(token)]
    tokens = []
    seen = set()

    for token in raw_tokens:
        corrected = correct_spelling(token, vocabulary=vocabulary)
        if corrected and corrected not in seen:
            tokens.append(corrected)
            seen.add(corrected)

    for variant in _token_variants(raw_tokens):
        corrected = correct_spelling(variant, vocabulary=vocabulary)
        if corrected and corrected not in seen:
            tokens.append(corrected)
            seen.add(corrected)

    return tokens


def term_counts(text):
    return Counter(tokenize(text))
