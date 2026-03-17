from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_conversation_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MentorReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField()),
                ("text", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("applicant", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="given_reviews",
                    to=settings.AUTH_USER_MODEL,
                )),
                ("conversation", models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="review",
                    to="chat.conversation",
                )),
                ("mentor", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="received_reviews",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
