from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Modelo: Persona
class Persona(models.Model):
    personaId = models.AutoField(primary_key=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    dui = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo: Empleado
class Empleado(models.Model):
    empleadoId = models.AutoField(primary_key=True)  # Campo de identificación independiente para Empleado
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    profesion = models.CharField(max_length=100)
    domicilio = models.ForeignKey('Domicilio', on_delete=models.CASCADE)
    respondeEconomicamentePor = models.ManyToManyField('Persona', related_name='responsableEconomico', blank=True, null=True)

    def __str__(self):
        return f"Empleado {self.empleadoId} - {self.persona.nombre} {self.persona.apellido}"


# Modelo: Local
class Local(models.Model):
    localId = models.AutoField(primary_key=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.PROTECT, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    tamanio = models.DecimalField(max_digits=5, decimal_places=2)
    ubicacion = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Local {self.local_id} - {self.nombre}"

# Modelo: Empresa
class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    representante = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='empresasRepresentadas')

    def __str__(self):
        return f"Empresa {self.empresa_id} - {self.nombre}"

# Modelo: Domicilio
class Domicilio(models.Model):
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    pais = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)

    def __str__(self):
        return f"Domicilio {self.direccion}, {self.ciudad}, {self.pais}"