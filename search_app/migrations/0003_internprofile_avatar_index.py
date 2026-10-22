from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("search_app", "0002_profile_database")]

    operations = [
        migrations.AddField(
            model_name="internprofile",
            name="avatar_index",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
