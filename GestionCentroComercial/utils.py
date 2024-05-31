from Sistema.models import Empresa, Empleado, Local, Persona

from enum import Enum
from django.shortcuts import redirect
from django.urls import reverse

class TipoContrato(Enum):
    EMPRESA = 'Empresa'
    ARRENDAMIENTO = 'Arrendamiento'
    EMPLEADO = 'Empleado'
    ARRENDAMIENTO_ARRENDAMIENTO = "Arrendamiento"
    SERVICIO_EMPRESA = "Servicio"
    PERSONAL_EMPLEADO = "Personal"


def test():
    print("Éxito")

def checkAdmin(request):
    return request.user.groups.filter(name="Administrador").exists()

from django.shortcuts import redirect, reverse

def requiereLogin(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Si el usuario está autenticado, ejecuta la función decorada
            return view_func(request, *args, **kwargs)
        else:
            # Si el usuario no está autenticado, redirige a la página de inicio de sesión
            return redirect(reverse('login'))
    return wrapper

def requiereAdmin(view_func):
    def wrapper(request, *args, **kwargs):
        if checkAdmin(request):
            # Si el usuario es un administrador, ejecuta la función decorada
            return view_func(request, *args, **kwargs)
        else:
            # Si el usuario no es un administrador, redirige a la página anterior
            referer = request.META.get('HTTP_REFERER', reverse('home'))
            return redirect(referer)
    return wrapper

def checkConditions(a,b):
      print(f"Primera = {a}, Segunda = {b}, Igualdad = {a == b}")



def guardarContratoBase(contratoBaseModelo, datosContratoBase):
    contratoBaseModelo.contratista = datosContratoBase["contratista"]
    contratoBaseModelo.fechaInicio = datosContratoBase["fechaInicio"]
    contratoBaseModelo.fechaFin = datosContratoBase["fechaFin"]
    contratoBaseModelo.vigente = datosContratoBase["vigente"]
    contratoBaseModelo.contenido = datosContratoBase["contenido"]
    contratoBaseModelo.save()

def guardarEmpresa(empresaModelo, representanteModelo, datosEmpresa):
        empresaModelo.nombre = datosEmpresa["empresaNombre"]
        empresaModelo.representante.nombre = datosEmpresa["representanteNombre"]
        empresaModelo.representante.apellido = datosEmpresa["representanteApellido"]
        empresaModelo.representante.dui = datosEmpresa["representanteDui"]
        representanteModelo.save()
        empresaModelo.save()

def guardarEmpleado(empleadoModelo, personaModelo, domicilioModelo, datosEmpleado):
        empleadoModelo.persona.nombre = datosEmpleado["nombre"]
        empleadoModelo.persona.apellido = datosEmpleado["apellido"]
        empleadoModelo.persona.dui = datosEmpleado["dui"]

        empleadoModelo.domicilio.ciudad = datosEmpleado["ciudad"]
        empleadoModelo.domicilio.direccion = datosEmpleado["direccion"]
        empleadoModelo.domicilio.pais = datosEmpleado["pais"]
        empleadoModelo.domicilio.departamento = datosEmpleado["departamento"]

        empleadoModelo.profesion  = datosEmpleado["profesion"]

        domicilioModelo.save()
        personaModelo.save()
        empleadoModelo.save()

def guardarContratoArrendamiento(contratoArrrendamientoModelo, empresaModelo, datosLocal):
    contratoArrrendamientoModelo.contratante = empresaModelo
    contratoArrrendamientoModelo.reserva = Local.objects.get(localId=datosLocal["locales"])
    contratoArrrendamientoModelo.save()

def guardarContratoServicio(contratoServicioModelo, empresaModelo):
    test()
    contratoServicioModelo.contratante = empresaModelo
    contratoServicioModelo.save()


def guardarContratoPersonal(contratoPersonalModelo, empleadoModelo):
    test()
    contratoPersonalModelo.contratante = empleadoModelo
    contratoPersonalModelo.save()