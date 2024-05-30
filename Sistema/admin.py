from django.contrib import admin
from .models import Domicilio, Empresa, Persona, Local, Empleado

# Register your models here.

# Para la aplicación 'Sistema'
admin.site.register(Domicilio)
admin.site.register(Empresa)
admin.site.register(Persona)
admin.site.register(Local)

class EmpleadoAdmin(admin.ModelAdmin):
    filter_horizontal = ('respondeEconomicamentePor',)  # Esto cambia el widget a un campo de selección múltiple más amigable
    
admin.site.register(Empleado, EmpleadoAdmin)
