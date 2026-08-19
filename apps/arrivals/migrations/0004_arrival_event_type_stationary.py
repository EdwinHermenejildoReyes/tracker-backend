from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arrivals', '0003_arrival_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrival',
            name='event_type',
            field=models.CharField(
                choices=[('enter', 'Entrada'), ('exit', 'Salida'), ('stationary', 'Estacionario')],
                default='enter',
                max_length=10,
            ),
        ),
    ]
