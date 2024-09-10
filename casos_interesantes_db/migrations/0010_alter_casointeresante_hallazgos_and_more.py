# Generated by Django 5.0.4 on 2024-09-07 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casos_interesantes_db', '0009_casointeresante_registrado_por'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casointeresante',
            name='hallazgos',
            field=models.TextField(help_text='Ingrese los hallazgos más relevantes del caso. Por ejemplo: Tumor en lóbulo superior derecho, Colangiocarcinoma, Neumonía bilateral, etc.', verbose_name='Hallazgos'),
        ),
        migrations.RemoveField(
            model_name='casointeresante',
            name='registrado_por',
        ),
        migrations.AlterField(
            model_name='casointeresante',
            name='contraste_ev',
            field=models.BooleanField(default=False, help_text='¿Se utilizó contraste endovenoso en el estudio?', verbose_name='Contraste'),
        ),
        migrations.AlterField(
            model_name='casointeresante',
            name='contraste_or',
            field=models.BooleanField(default=False, help_text='¿Se utilizó contraste oral en el estudio?', verbose_name='Contraste oral'),
        ),
        migrations.DeleteModel(
            name='Patologia',
        ),
    ]