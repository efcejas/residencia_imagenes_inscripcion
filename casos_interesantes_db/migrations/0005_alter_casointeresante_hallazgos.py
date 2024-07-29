# Generated by Django 5.0.4 on 2024-07-29 00:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casos_interesantes_db', '0004_remove_casointeresante_hallazgos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casointeresante',
            name='hallazgos',
            field=models.ForeignKey(help_text='Seleccione la patología que se encontró en el estudio.', on_delete=django.db.models.deletion.CASCADE, related_name='casos_interesantes', to='casos_interesantes_db.patologia', verbose_name='Hallazgos'),
        ),
    ]