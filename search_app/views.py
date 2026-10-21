from django.shortcuts import render
from .models import Document

def search_view(request):
  query = request.GET.get('q', '')
  results = []

  if query:
    # Basic filtering placeholder until Dev 1, 2, and 3 plug in their modules
    results = Document.objects.filter(content__icontains=query)

  return render(request, 'search_app/search.html', {'results': results, 'query': query})
