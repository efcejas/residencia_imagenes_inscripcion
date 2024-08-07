# Generated by Django 5.0.4 on 2024-07-27 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del paciente')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido del paciente')),
                ('dni', models.CharField(help_text='Ingrese el DNI sin puntos.', max_length=8, unique=True, verbose_name='DNI del paciente')),
            ],
        ),
    ]
