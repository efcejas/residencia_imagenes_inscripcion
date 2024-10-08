# Generated by Django 5.0.4 on 2024-08-15 23:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0012_alter_clasificaciontematica_seccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='AteneoEvaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ateneo_fecha', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha del ateneo')),
                ('importancia_tema', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Qué tan importante te resultó el tema propuesto?')),
                ('puntaje_contenido_cientifico', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Qué puntaje le darias a la presentación,  teniendo en cuenta el contenido cientifico de la misma?')),
                ('puntaje_calidad_presentacion', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Qué puntaje le darias a la presentación,  teniendo en cuenta la calidad del contenido y la forma de presentación?')),
                ('puntaje_calidad_texto', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Qué puntaje le darias a la calidad del texto de la presentación,  teniendo en cuenta la claridad de la informacion y la ortografía?')),
                ('claridad_presentacion_oral', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Qué tan clara fue la presentación oral?')),
                ('puntaje_bibliografia', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Qué puntaje le darias al tipo de bibliografía elegida?')),
                ('uso_tiempo', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Como calificaría el uso del tiempo en la presentación?')),
                ('cumplimiento_objetivos', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Que tanto se cumplieron los objetivos de aprendizaje?')),
                ('nota_general', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='¿Qué nota general le darias a la presentación?')),
                ('comentario_aprendizaje', models.TextField(help_text='Comenta brevemente que aprendiste con la presentación')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
