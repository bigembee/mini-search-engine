# search_app/models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Location(models.Model):
    """Reusable geographic dimension for profile filtering."""

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Nigeria")

    class Meta:
        ordering = ("country", "state", "city")
        constraints = [
            models.UniqueConstraint(
                fields=("city", "state", "country"), name="unique_profile_location"
            )
        ]

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"


class Skill(models.Model):
    """Canonical skill vocabulary used by the search index."""

    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class InternProfile(models.Model):
    class WorkMode(models.TextChoices):
        REMOTE = "remote", "Remote"
        VIRTUAL = "virtual", "Virtual"
        HYBRID = "hybrid", "Hybrid"
        ONSITE = "on-site", "On-site"

    class EmploymentType(models.TextChoices):
        INTERN = "intern", "Intern"
        CONTRACT = "contract", "Contract"
        FULL_TIME = "full-time", "Full-time"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ON_LEAVE = "on-leave", "On Leave"
        COMPLETED = "completed", "Completed"
        INACTIVE = "inactive", "Inactive"

    intern_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    role = models.CharField(max_length=100)
    work_mode = models.CharField(max_length=20, choices=WorkMode.choices)
    work_days = models.CharField(max_length=40, default="Mon-Fri")
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    daily_hours = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(24)],
    )
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="interns")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    skills = models.ManyToManyField(Skill, through="InternSkill", related_name="interns")
    search_keywords = models.TextField(editable=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("intern_id",)
        indexes = [
            models.Index(fields=("status", "role"), name="intern_status_role_idx"),
            models.Index(fields=("work_mode", "location"), name="intern_work_location_idx"),
        ]

    def __str__(self):
        return f"{self.intern_id} — {self.full_name}"

    def rebuild_search_keywords(self):
        skill_names = self.skills.values_list("name", flat=True)
        self.search_keywords = " | ".join([
            self.full_name, self.role, self.get_work_mode_display(),
            str(self.location), *skill_names,
        ])


class InternSkill(models.Model):
    intern = models.ForeignKey(InternProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT)
    proficiency = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("intern", "skill"), name="unique_intern_skill")
        ]

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
