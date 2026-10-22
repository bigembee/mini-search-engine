from collections import Counter

from .processor import tokenize


def _score_document(document, query_terms):
    if not query_terms:
        return 0.0

    text = f"{document.get('title', '')} {document.get('content', '')}"
    token_counts = Counter(tokenize(text))
    query_counts = Counter(query_terms)

    score = 0.0
    for term, query_weight in query_counts.items():
        score += token_counts.get(term, 0) * query_weight

    title_tokens = set(tokenize(document.get('title', '')))
    title_bonus = sum(1 for term in query_terms if term in title_tokens)
    return score + (title_bonus * 3)


def rank_documents(documents, query):
    query_terms = [term for term in tokenize(query) if term]
    ranked = []

    for document in documents:
        score = _score_document(document, query_terms)
        if score > 0:
            ranked.append({
                "title": document.get("title", "Untitled"),
                "content": document.get("content", ""),
                "score": round(score, 2),
                **{field: document[field] for field in (
                    "full_name", "avatar_index", "location", "work_mode",
                    "work_days", "daily_hours", "skills",
                ) if field in document},
            })

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked
