from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_savedmentor"),
    ]

    operations = [
        migrations.AddField(
            model_name="mentorprofile",
            name="availability_status",
            field=models.CharField(
                choices=[("available", "Available"), ("busy", "Busy")],
                default="available",
                max_length=20,
            ),
        ),
    ]
