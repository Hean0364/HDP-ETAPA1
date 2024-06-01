from django.contrib import admin
from .models import Domicilio, Empresa, Persona, Local, Empleado

# Register your models here.

# Para la aplicación 'Sistema'
admin.site.register(Domicilio)
admin.site.register(Empresa)
admin.site.register(Persona)
admin.site.register(Local)
admin.site.register(Empleado)
