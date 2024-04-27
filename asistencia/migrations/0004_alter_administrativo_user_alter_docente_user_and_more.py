# Generated by Django 5.0.4 on 2024-04-21 16:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0003_administrativo_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrativo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='administrativo_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='docente',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='docente_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='residente',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='residente_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
