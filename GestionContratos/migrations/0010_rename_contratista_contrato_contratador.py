# Generated by Django 4.2.13 on 2024-06-02 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GestionContratos', '0009_rename_archivo_url_contrato_archivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contrato',
            old_name='contratista',
            new_name='contratador',
        ),
    ]
