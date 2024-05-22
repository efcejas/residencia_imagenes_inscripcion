# Generated by Django 5.0.4 on 2024-05-22 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_grupo', models.CharField(error_messages={'unique': 'Ya existe un grupo registrado con ese nombre.'}, max_length=50, unique=True, verbose_name='Nombre del grupo')),
                ('aula', models.CharField(max_length=10, verbose_name='Aula')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
    ]
