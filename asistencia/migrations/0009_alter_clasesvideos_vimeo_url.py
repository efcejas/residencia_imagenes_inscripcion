# Generated by Django 5.0.4 on 2024-07-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0008_alter_clasificaciontematica_seccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clasesvideos',
            name='vimeo_url',
            field=models.URLField(error_messages={'unique': 'Ese video ya está registrado.'}, unique=True, verbose_name='URL de Vimeo'),
        ),
    ]
