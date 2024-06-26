# Generated by Django 5.0.4 on 2024-06-15 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0002_gruposresidentes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gruposresidentes',
            options={'verbose_name': 'Residentes', 'verbose_name_plural': 'Residentes por año y residencia'},
        ),
        migrations.CreateModel(
            name='Aulas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_aula', models.CharField(max_length=50, verbose_name='Nombre del aula')),
                ('latitud', models.FloatField(verbose_name='Latitud')),
                ('longitud', models.FloatField(verbose_name='Longitud')),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asistencia.sedes')),
            ],
            options={
                'verbose_name': 'Aula',
                'verbose_name_plural': 'Aulas',
            },
        ),
    ]
