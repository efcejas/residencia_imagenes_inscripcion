# Generated by Django 5.0.4 on 2024-04-07 22:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0009_registroasistencia_llegada_a_tiempo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registroasistencia',
            name='fecha_hora',
        ),
        migrations.AddField(
            model_name='registroasistencia',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fecha'),
        ),
        migrations.AddField(
            model_name='registroasistencia',
            name='hora',
            field=models.TimeField(default='00:00', verbose_name='Hora'),
        ),
    ]