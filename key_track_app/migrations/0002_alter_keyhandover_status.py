# Generated by Django 4.2.3 on 2023-07-16 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('key_track_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyhandover',
            name='status',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('entregado', 'Entregado')], default='pendiente', max_length=20, verbose_name='Estado'),
        ),
    ]
