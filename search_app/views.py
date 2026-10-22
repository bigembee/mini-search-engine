from django.shortcuts import render

from .models import Document, InternProfile
from .utils.indexer import build_inverted_index
from .utils.ranker import rank_documents

def _search_documents(query):
    query = (query or '').strip()
    if not query:
        return []

    profile_documents = [
        {
            "title": profile.role,
            "full_name": profile.full_name,
            "avatar_index": profile.avatar_index,
            "location": str(profile.location),
            "work_mode": profile.get_work_mode_display(),
            "work_days": profile.work_days,
            "daily_hours": profile.daily_hours,
            "skills": ", ".join(profile.skills.values_list("name", flat=True)),
            "content": (
                f"{profile.search_keywords} | Work days: {profile.work_days} | {profile.daily_hours} hours/day"
            ),
        }
        for profile in InternProfile.objects.filter(status=InternProfile.Status.ACTIVE)
    ]
    stored_documents = list(Document.objects.values("title", "content"))
    documents = profile_documents + stored_documents

    inverted_index = build_inverted_index(documents)
    _ = inverted_index
    return rank_documents(documents, query)


def _render_search_page(request, results_page=False):
    query = request.GET.get('q', '').strip() if results_page else ''
    results = _search_documents(query) if results_page else []
    return render(request, 'search_app/search.html', {
        'results': results,
        'query': query,
        'total_results': len(results),
    })


def search_view(request):
    return _render_search_page(request)


def search_results_view(request):
    query = request.GET.get('q', '').strip()
    results = _search_documents(query)
    return render(request, 'search_app/results.html', {
        'results': results,
        'query': query,
        'total_results': len(results),
    })
