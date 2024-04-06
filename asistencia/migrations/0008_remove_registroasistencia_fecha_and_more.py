# Generated by Django 5.0.3 on 2024-04-03 00:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0007_remove_registroasistencia_fecha_hora_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registroasistencia',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='registroasistencia',
            name='hora',
        ),
        migrations.AddField(
            model_name='registroasistencia',
            name='fecha_hora',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha y hora'),
            preserve_default=False,
        ),
    ]