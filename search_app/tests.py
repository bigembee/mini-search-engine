from django.test import SimpleTestCase

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
