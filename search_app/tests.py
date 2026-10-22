from datetime import time

from django.test import TestCase

from .models import InternProfile, InternSkill, Location, Skill


class InternProfileDatabaseTests(TestCase):
    def test_profile_has_normalized_skills_and_search_document(self):
        location = Location.objects.create(city="Lagos", state="Lagos", country="Nigeria")
        profile = InternProfile.objects.create(
            intern_id="INT-TEST", full_name="Ada Lovelace", first_name="Ada",
            role="Backend Developer", work_mode="remote", work_days="Mon-Fri",
            shift_start=time(9), shift_end=time(17), daily_hours=8, location=location,
            employment_type="intern", status="active",
        )
        skill = Skill.objects.create(name="Django", slug="django")
        InternSkill.objects.create(intern=profile, skill=skill)
        profile.rebuild_search_keywords()
        profile.save(update_fields=["search_keywords", "updated_at"])

        self.assertEqual(profile.skills.get(), skill)
        self.assertIn("Ada Lovelace", profile.search_keywords)
        self.assertIn("Django", profile.search_keywords)

    def test_location_cannot_be_duplicated(self):
        values = {"city": "Lagos", "state": "Lagos", "country": "Nigeria"}
        Location.objects.create(**values)
        with self.assertRaises(Exception):
            Location.objects.create(**values)

# Create your tests here.
