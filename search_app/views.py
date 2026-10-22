from django.shortcuts import render

from .utils.indexer import build_inverted_index
from .utils.ranker import rank_documents

SAMPLE_DOCUMENTS = [
    {
        "title": "Python for data science",
        "content": "Python is widely used in data science for analysis, modelling, and automation. Teams use notebooks, pandas, and visualisations to understand large datasets.",
    },
    {
        "title": "Building a mini search engine",
        "content": "A search engine indexes documents, tokenises text, and ranks pages by relevance to a user query. Inverted indexes and scoring functions help return the most useful matches first.",
    },
    {
        "title": "Volcano safety guide",
        "content": "Volcanoes can erupt suddenly, so communities prepare evacuation routes, monitor tremors, and follow local authorities during alerts and ashfall warnings.",
    },
    {
        "title": "Remote team productivity",
        "content": "Remote teams stay productive with clear communication, handover notes, shared goals, and repeatable workflows that reduce context switching and delays.",
    },
    {
        "title": "Machine learning basics",
        "content": "Machine learning models learn patterns from training data and then make predictions on new information, with quality depending on data quality and model tuning.",
    },
]


def _search_documents(query):
    query = (query or '').strip()
    if not query:
        return []

    inverted_index = build_inverted_index(SAMPLE_DOCUMENTS)
    _ = inverted_index
    return rank_documents(SAMPLE_DOCUMENTS, query)


def search_view(request):
    query = request.GET.get('q', '').strip()
    results = _search_documents(query)

    return render(request, 'search_app/search.html', {
        'results': results,
        'query': query,
        'total_results': len(results),
    })
