# Generated by Django 4.2.3 on 2023-07-21 16:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('key_track_app', '0005_keyhandover_unique_pending_key_handover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal',
            name='phone',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Teléfono'),
        ),
    ]
