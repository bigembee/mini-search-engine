from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_view, name='search_home'),
    path('results/', views.search_results_view, name='search_results'),
]
