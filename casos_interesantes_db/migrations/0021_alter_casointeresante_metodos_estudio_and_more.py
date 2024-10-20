# Generated by Django 5.0.4 on 2024-10-20 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casos_interesantes_db', '0020_remove_casointeresante_contraste_ev_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casointeresante',
            name='metodos_estudio',
            field=models.ManyToManyField(help_text='Seleccione el método principal de estudio utilizado para el caso. Puede seleccionar más de uno si corresponde.', to='casos_interesantes_db.metodoestudio', verbose_name='Métodos de estudio'),
        ),
        migrations.AlterField(
            model_name='casointeresante',
            name='organo',
            field=models.ForeignKey(help_text='Seleccione el órgano donde se encuentra la patología, si corresponde.', on_delete=django.db.models.deletion.CASCADE, related_name='casos_interesantes', to='casos_interesantes_db.organo', verbose_name='Órgano'),
        ),
    ]
