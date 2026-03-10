from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('active', 'Active'), ('declined', 'Declined')],
                default='active',  # existing conversations stay active
                max_length=20,
            ),
        ),
    ]
