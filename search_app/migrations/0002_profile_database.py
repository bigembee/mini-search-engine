from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("search_app", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("country", models.CharField(default="Nigeria", max_length=100)),
            ],
            options={"ordering": ("country", "state", "city")},
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(max_length=90, unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="InternProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("intern_id", models.CharField(max_length=20, unique=True)),
                ("full_name", models.CharField(max_length=150)),
                ("first_name", models.CharField(max_length=80)),
                ("last_name", models.CharField(blank=True, max_length=80)),
                ("role", models.CharField(max_length=100)),
                ("work_mode", models.CharField(choices=[("remote", "Remote"), ("virtual", "Virtual"), ("hybrid", "Hybrid"), ("on-site", "On-site")], max_length=20)),
                ("work_days", models.CharField(default="Mon-Fri", max_length=40)),
                ("shift_start", models.TimeField()),
                ("shift_end", models.TimeField()),
                ("daily_hours", models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("employment_type", models.CharField(choices=[("intern", "Intern"), ("contract", "Contract"), ("full-time", "Full-time")], max_length=20)),
                ("status", models.CharField(choices=[("active", "Active"), ("on-leave", "On Leave"), ("completed", "Completed"), ("inactive", "Inactive")], default="active", max_length=20)),
                ("search_keywords", models.TextField(blank=True, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("location", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="interns", to="search_app.location")),
            ],
            options={"ordering": ("intern_id",)},
        ),
        migrations.CreateModel(
            name="InternSkill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("proficiency", models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("intern", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="search_app.internprofile")),
                ("skill", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="search_app.skill")),
            ],
        ),
        migrations.AddField(
            model_name="internprofile", name="skills",
            field=models.ManyToManyField(related_name="interns", through="search_app.InternSkill", to="search_app.skill"),
        ),
        migrations.AddConstraint(
            model_name="location",
            constraint=models.UniqueConstraint(fields=("city", "state", "country"), name="unique_profile_location"),
        ),
        migrations.AddConstraint(
            model_name="internskill",
            constraint=models.UniqueConstraint(fields=("intern", "skill"), name="unique_intern_skill"),
        ),
        migrations.AddIndex(model_name="internprofile", index=models.Index(fields=("status", "role"), name="intern_status_role_idx")),
        migrations.AddIndex(model_name="internprofile", index=models.Index(fields=("work_mode", "location"), name="intern_work_location_idx")),
    ]
