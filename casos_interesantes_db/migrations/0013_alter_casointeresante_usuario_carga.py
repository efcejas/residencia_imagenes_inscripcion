# Generated by Django 5.0.4 on 2024-09-12 01:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casos_interesantes_db', '0012_casointeresante_usuario_carga_alter_paciente_dni'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='casointeresante',
            name='usuario_carga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='casos_interesantes', to=settings.AUTH_USER_MODEL, verbose_name='Usuario que cargó el caso'),
        ),
    ]
