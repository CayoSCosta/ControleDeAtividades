# Generated by Django 5.1.4 on 2025-01-15 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro_horas', '0004_registro_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='hora_de_pausa',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='registro',
            name='tempo_pausado',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
