from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("search_app", "0003_internprofile_avatar_index")]

    operations = [
        migrations.AlterField(
            model_name="internprofile",
            name="employment_type",
            field=models.CharField(
                choices=[
                    ("intern", "Intern"),
                    ("contract", "Contract"),
                    ("full-time", "Full-time"),
                    ("part-time", "Part-time"),
                ],
                max_length=20,
            ),
        ),
    ]
