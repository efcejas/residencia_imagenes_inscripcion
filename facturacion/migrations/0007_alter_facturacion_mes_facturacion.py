# Generated by Django 5.0.4 on 2024-12-03 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0006_alter_facturacion_mes_facturacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturacion',
            name='mes_facturacion',
            field=models.CharField(default='2024-12', editable=False, max_length=7),
        ),
    ]
