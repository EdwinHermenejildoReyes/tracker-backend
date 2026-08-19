from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrivals', '0002_arrival_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrival',
            name='event_id',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
    ]
