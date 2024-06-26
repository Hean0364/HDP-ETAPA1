# Generated by Django 4.2.13 on 2024-05-30 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('pais', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('empresa_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('personaId', models.AutoField(primary_key=True, serialize=False)),
                ('apellido', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=100)),
                ('dui', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('localId', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=50)),
                ('tamanio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ubicacion', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistema.empresa')),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='representante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresasRepresentadas', to='Sistema.persona'),
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('empleadoId', models.AutoField(primary_key=True, serialize=False)),
                ('profesion', models.CharField(max_length=100)),
                ('domicilio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistema.domicilio')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Sistema.persona')),
                ('respondeEconomicamentePor', models.ManyToManyField(blank=True, related_name='responsableEconomico', to='Sistema.persona')),
            ],
        ),
    ]
