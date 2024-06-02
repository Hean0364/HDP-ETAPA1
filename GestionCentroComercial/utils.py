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
    contratoBaseModelo.archivo = datosContratoBase["archivo"]
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
        empleadoModelo.informacionAdicional = datosEmpleado["informacionAdicional"] #reciente

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
# *****************************************************************************
def definirCamposContratoBase(contratoBaseModelo, contratoBaseFormulario):
    datosContratoBase = {
        "contratista": contratoBaseModelo.contratista,
        "fechaInicio": contratoBaseModelo.fechaInicio,
        "fechaFin": contratoBaseModelo.fechaFin,
        "vigente": contratoBaseModelo.vigente,
        "contenido": contratoBaseModelo.contenido,
        "archivo": contratoBaseModelo.archivo
    }
    # FIXME:
    contratoBaseFormulario.initial = datosContratoBase

    return contratoBaseFormulario

def definirCamposEmpresa(empresaModelo, empresaFormulario):

    datosEmpresa = {
        "empresaNombre": empresaModelo.nombre,
        "representanteNombre": empresaModelo.representante.nombre,
        "representanteApellido": empresaModelo.representante.apellido,
        "representanteDui": empresaModelo.representante.dui
    }
    empresaFormulario.initial = datosEmpresa
    return empresaFormulario

def definirCamposEmpleado(empleadoModelo, empleadoFormulario):
    datosEmpleado = {
        "nombre": empleadoModelo.persona.nombre,
        "apellido": empleadoModelo.persona.apellido,
        "dui": empleadoModelo.persona.dui,
        "ciudad": empleadoModelo.domicilio.ciudad,
        "direccion": empleadoModelo.domicilio.direccion,
        "pais": empleadoModelo.domicilio.pais,
        "departamento": empleadoModelo.domicilio.departamento,
        "profesion": empleadoModelo.profesion,
        "informacionAdicional": empleadoModelo.informacionAdicional,
    }
    empleadoFormulario.initial = datosEmpleado
    return empleadoFormulario

def definirCamposContratoArrendamiento(contratoArrrendamientoModelo, contratoArrendamientoFormulario):
    datosLocal = {
        "locales": contratoArrrendamientoModelo.reserva
    }
    contratoArrendamientoFormulario.initial = datosLocal
    return contratoArrendamientoFormulario

def definirCamposContratoServicio(contratoServicioModelo, contratoServicioFormulario):
    datosContratoServicio = {
        "contratante": contratoServicioModelo.contratante
    }
    contratoServicioFormulario.initial = datosContratoServicio
    return contratoServicioFormulario

def definirCamposContratoPersonal(contratoPersonalModelo, contratoPersonalFormulario):
    datosContratoPersonal = {
        "contratante": contratoPersonalModelo.contratante
    }
    contratoPersonalFormulario.initial = datosContratoPersonal
    return contratoPersonalFormulario

def asignacionContratoArrendamiento(formularioBase, formularioEmpresa, formularioLocal, nuevoContratoBase, nuevoContratoArrendamiento, nuevaPersona, nuevaEmpresa):
    # Limpiamos datos obtenidos en los formularios
    datosContratoBase = formularioBase.cleaned_data
    datosEmpresa = formularioEmpresa.cleaned_data
    datosLocal = formularioLocal.cleaned_data

    # Guardar contrato base
    guardarContratoBase(nuevoContratoBase, datosContratoBase)

    # Guardar empresa y representante
    guardarEmpresa(nuevaEmpresa, nuevaPersona, datosEmpresa)

    # Guardar contrato de arrendamiento
    guardarContratoArrendamiento(nuevoContratoArrendamiento, nuevaEmpresa, datosLocal)

def asignacionContratoServicio(formularioBase, formularioEmpresa, nuevoContratoBase, nuevoContratoServicio, nuevaPersona, nuevaEmpresa):
    # Limpiamos datos obtenidos en los formularios
    datosContratoBase = formularioBase.cleaned_data
    datosEmpresa = formularioEmpresa.cleaned_data

    # Guardar contrato base
    guardarContratoBase(nuevoContratoBase, datosContratoBase)

    # Guardar empresa y representante
    guardarEmpresa(nuevaEmpresa, nuevaPersona, datosEmpresa)

    # Guardar contrato de arrendamiento
    guardarContratoServicio(nuevoContratoServicio, nuevaEmpresa)


def asignacionContratoPersonal(formularioBase, formularioEmpleado, nuevoContratoBase, nuevoContratoPersonal, nuevaPersona, nuevoDomicilio, nuevoEmpleado):
    # Limpiamos datos obtenidos en los formularios
    datosContratoBase = formularioBase.cleaned_data
    datosEmpleado = formularioEmpleado.cleaned_data

    # Metodos de guardado
    guardarContratoBase(nuevoContratoBase, datosContratoBase)
    guardarEmpleado(nuevoEmpleado, nuevaPersona, nuevoDomicilio, datosEmpleado)
    guardarContratoPersonal(nuevoContratoPersonal, nuevoEmpleado)

def hacerFormularioReadonly(formulario):
    for field in formulario.fields.values():
        field.widget.attrs['readonly'] = True
        field.widget.attrs['disabled'] = True  # Opcional
    return formulario