# Generated by Django 5.0.4 on 2024-10-28 01:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examen',
            options={'verbose_name': 'Examen', 'verbose_name_plural': 'Exámenes'},
        ),
        migrations.AlterModelOptions(
            name='pregunta',
            options={'verbose_name': 'Pregunta', 'verbose_name_plural': 'Preguntas'},
        ),
        migrations.AlterModelOptions(
            name='residente',
            options={'verbose_name': 'Residente', 'verbose_name_plural': 'Residentes'},
        ),
        migrations.AlterModelOptions(
            name='respuesta',
            options={'verbose_name': 'Respuesta', 'verbose_name_plural': 'Respuestas'},
        ),
        migrations.AddField(
            model_name='pregunta',
            name='texto_ayuda',
            field=models.TextField(blank=True, verbose_name='Texto de ayuda'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='creado_en',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='descripcion',
            field=models.TextField(verbose_name='Descripción del examen'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='titulo',
            field=models.CharField(max_length=200, verbose_name='Título del examen'),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='examen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preguntas', to='imat.examen', verbose_name='Examen'),
        ),
        migrations.AlterField(
            model_name='pregunta',
            name='texto',
            field=models.CharField(max_length=500, verbose_name='Texto de la pregunta'),
        ),
        migrations.AlterField(
            model_name='residente',
            name='apellido',
            field=models.CharField(max_length=100, verbose_name='Apellido'),
        ),
        migrations.AlterField(
            model_name='residente',
            name='dni',
            field=models.CharField(max_length=15, unique=True, verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='residente',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='creado_en',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='imat.pregunta', verbose_name='Pregunta'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='residente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='imat.residente', verbose_name='Residente'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='texto',
            field=models.TextField(verbose_name='Texto de la respuesta'),
        ),
    ]
