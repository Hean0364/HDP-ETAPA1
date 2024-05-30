from django.db import models
from GestionCentroComercial.utils import TipoContrato


# Create your models here.
# Modelo: Contrato
class Contrato(models.Model):
    contratoId = models.AutoField(primary_key=True) # ID del contrato
    fechaInicio = models.DateField() # Fecha de inicio
    fechaFin = models.DateField(null=True)
    vigente = models.BooleanField()
    contenido = models.TextField()
    contratista = models.ForeignKey('Sistema.Empleado', on_delete=models.PROTECT, related_name='contratacionesEmpleado', blank=True) # Referencia al empleado que elabora el contrato


    def __str__(self):
        return f"Contrato {self.contratoId}"

# Modelo: ContratoEmpleado
class ContratoEmpleado(models.Model):
    contrato = models.OneToOneField(Contrato, on_delete=models.CASCADE, related_name='contratoEmpleadoDetalle') # contrato del que deriva
    contratante = models.ForeignKey('Sistema.Empleado', on_delete=models.PROTECT, related_name='contratosEmpleado')
    tipo = models.CharField(max_length=20, default=TipoContrato.EMPLEADO.value, editable=False)

    def __str__(self):
        return f"ContratoEmpleado {self.contrato.contratoId} - Empleado {self.contratante_id} - ContratoID {self.contrato.contratoId}"

# Modelo: ContratoEmpresa
class ContratoEmpresa(models.Model):
    contrato = models.OneToOneField(Contrato, on_delete=models.CASCADE, related_name='contratoEmpresaDetalle') # contrato del que deriva
    contratante = models.ForeignKey('Sistema.Empresa', on_delete=models.PROTECT, related_name='contratosEmpresa')
    tipo = models.CharField(max_length=20, default=TipoContrato.EMPRESA.value, editable=False)

    def __str__(self):
        return f"ContratoEmpresa {self.contrato.contratoId} - Empresa {self.contratante_id}  - ContratoID {self.contrato.contratoId}"

# Modelo: ContratoArrendamiento
class ContratoArrendamiento(models.Model):
    contrato = models.OneToOneField(Contrato, on_delete=models.CASCADE, related_name='contratoArrendamientoDetalle') # contrato del que deriva
    contratante = models.ForeignKey('Sistema.Empresa', on_delete=models.PROTECT, related_name='contratosArrendamiento')
    reserva = models.ForeignKey('Sistema.Local', on_delete=models.PROTECT, related_name='contratosArrendamiento')
    tipo = models.CharField(max_length=20, default=TipoContrato.ARRENDAMIENTO.value, editable=False)

    def __str__(self):
        return f"ContratoArrendamiento {self.contratoId} - Empresa {self.contratante_id} - ContratoID {self.contrato.contratoId}"
