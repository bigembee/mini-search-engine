from datetime import time

from django.test import SimpleTestCase, TestCase

from .models import InternProfile, Location, Skill
from .utils.ranker import rank_documents


class SearchRankingTests(SimpleTestCase):
    def test_ranks_highest_frequency_matches_first(self):
        documents = [
            {"title": "Python for data science", "content": "Python Python data analysis using Python for insights."},
            {"title": "Python in practice", "content": "Learn Python with simple examples."},
        ]

        results = rank_documents(documents, "python")

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["title"], "Python for data science")
        self.assertGreater(results[0]["score"], results[1]["score"])

    def test_returns_empty_results_when_query_is_blank(self):
        documents = [{"title": "Python guide", "content": "Learn Python with hands-on examples."}]

        results = rank_documents(documents, "   ")

        self.assertEqual(results, [])


class DatabaseSearchTests(TestCase):
    def setUp(self):
        location = Location.objects.create(city="Lagos", state="Lagos", country="Nigeria")
        profile = InternProfile.objects.create(
            intern_id="INT-SEARCH", full_name="Ada Search", first_name="Ada",
            role="Backend Developer", work_mode="remote", work_days="Mon-Fri",
            shift_start=time(9), shift_end=time(17), daily_hours=8, location=location,
            employment_type="intern", status="active",
        )
        skill = Skill.objects.create(name="Django", slug="django-search")
        profile.skills.add(skill)
        profile.rebuild_search_keywords()
        profile.save(update_fields=["search_keywords", "updated_at"])

    def test_search_uses_active_profiles_from_database(self):
        response = self.client.get("/results/?q=django")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search_app/results.html")
        self.assertContains(response, "Ada Search")
        self.assertContains(response, 'action="/results/"')

    def test_inactive_profiles_are_not_returned(self):
        InternProfile.objects.update(status=InternProfile.Status.INACTIVE)

        response = self.client.get("/results/?q=django")

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "Ada Search")
