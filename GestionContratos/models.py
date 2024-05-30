from django.db import models

# Create your models here.
# Modelo: Contrato
class Contrato(models.Model):
    contrato_id = models.AutoField(primary_key=True) # ID del contrato
    fecha_inicio = models.DateField() # Fecha de inicio
    fecha_fin = models.DateField(null=True)
    vigente = models.BooleanField()
    contenido = models.TextField()
    contratista = models.ForeignKey('Sistema.Empleado', on_delete=models.PROTECT, related_name='contratacionesEmpleado', blank=True) # Referencia al empleado que elabora el contrato


    def __str__(self):
        return f"Contrato {self.contrato_id}"

# Modelo: ContratoEmpleado
class ContratoEmpleado(models.Model):
    contrato = models.OneToOneField(Contrato, on_delete=models.CASCADE, related_name='contratoEmpleadoDetalle') # contrato del que deriva
    contratante = models.ForeignKey('Sistema.Empleado', on_delete=models.PROTECT, related_name='contratosEmpleado')

    def __str__(self):
        return f"ContratoEmpleado {self.contrato_id} - Empleado {self.contratante_id} - ContratoID {self.contrato.contrato_id}"

# Modelo: ContratoEmpresa
class ContratoEmpresa(models.Model):
    contrato = models.OneToOneField(Contrato, on_delete=models.CASCADE, related_name='contratoEmpresaDetalle') # contrato del que deriva
    contratante = models.ForeignKey('Sistema.Empresa', on_delete=models.PROTECT, related_name='contratosEmpresa')

    def __str__(self):
        return f"ContratoEmpresa {self.contrato_id} - Empresa {self.contratante_id}  - ContratoID {self.contrato.contrato_id}"

# Modelo: ContratoArrendamiento
class ContratoArrendamiento(models.Model):
    contrato = models.OneToOneField(Contrato, on_delete=models.CASCADE, related_name='contratoArrendamientoDetalle') # contrato del que deriva
    contratante = models.ForeignKey('Sistema.Empresa', on_delete=models.PROTECT, related_name='contratosArrendamiento')
    reserva = models.ForeignKey('Sistema.Local', on_delete=models.PROTECT, related_name='contratosArrendamiento')

    def __str__(self):
        return f"ContratoArrendamiento {self.contrato_id} - Empresa {self.contratante_id} - ContratoID {self.contrato.contrato_id}"
