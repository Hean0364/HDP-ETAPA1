from django.contrib import admin
from .models import Contrato, ContratoEmpresa, ContratoEmpleado, ContratoArrendamiento

# Register your models here.

# Para la aplicación 'GestionContratos'
admin.site.register(Contrato)
admin.site.register(ContratoEmpresa)
admin.site.register(ContratoEmpleado)
admin.site.register(ContratoArrendamiento)