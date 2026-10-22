from collections import defaultdict

from .processor import term_counts


def build_inverted_index(documents):
    index = defaultdict(list)

    for document_id, document in enumerate(documents):
        counts = term_counts(f"{document.get('title', '')} {document.get('content', '')}")
        for term, count in counts.items():
            index[term].append({"id": document_id, "count": count})

    return dict(index)


def document_frequency(index):
    return {term: len(entries) for term, entries in index.items()}
