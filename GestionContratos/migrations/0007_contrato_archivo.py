# Generated by Django 4.2.13 on 2024-06-02 00:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionContratos', '0006_alter_contratoempleado_contratante'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='archivos/', validators=[django.core.validators.FileExtensionValidator(['pdf'], message='Solo se permiten archivos PDF.')]),
        ),
    ]
