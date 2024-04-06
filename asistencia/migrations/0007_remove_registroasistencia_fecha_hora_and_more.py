# Generated by Django 5.0.3 on 2024-04-03 00:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0006_alter_registroasistencia_fecha_hora'),
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
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Hora'),
        ),
    ]