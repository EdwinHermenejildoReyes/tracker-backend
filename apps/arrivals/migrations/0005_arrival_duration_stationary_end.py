from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrivals', '0004_arrival_event_type_stationary'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrival',
            name='duration_seconds',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='arrival',
            name='event_type',
            field=models.CharField(
                choices=[
                    ('enter', 'Entrada'),
                    ('exit', 'Salida'),
                    ('stationary', 'Estacionario'),
                    ('stationary_end', 'Fin estacionario'),
                ],
                default='enter',
                max_length=14,
            ),
        ),
    ]
