from django.shortcuts import render
from django.http import HttpResponse
from .models import Contrato, ContratoArrendamiento, ContratoEmpleado, ContratoEmpresa

def contratos(request):
    contratos = Contrato.objects.all()
    return render(request, "contratosBase.html", {"contratos": contratos})

def contratosArrendamiento(request):
    contratos = ContratoArrendamiento.objects.all()
    return render(request, "contratosBase.html", {"contratos": contratos})


def contratosServicio(request):
    return HttpResponse("Esta vista maneja los contratos de servicio.")

def contratosPersonal(request):
    return HttpResponse("Esta vista maneja los contratos de personal.")

def contratosFiltrados(request, tipo_contrato, filtro_empresa, desde_fecha, vigente):
    mensaje = f"Esta vista maneja los contratos filtrados por tipo de contrato: {tipo_contrato}, empresa: {filtro_empresa}, desde fecha: {desde_fecha}, y vigente: {vigente}."
    return HttpResponse(mensaje)

def contratosPersonalFiltrados(request, filtro_persona, desde_fecha, vigente):
    mensaje = f"Esta vista maneja los contratos de personal filtrados por persona: {filtro_persona}, desde fecha: {desde_fecha}, y vigente: {vigente}."
    return HttpResponse(mensaje)

def nuevoContrato(request, tipo_contrato="arrendamiento"):
    mensaje = f"Esta vista crea un nuevo contrato de tipo {tipo_contrato}."
    return HttpResponse(mensaje)

def editarContrato(request, idContrato):
    mensaje = f"Esta vista edita el contrato con ID {idContrato}."
    return HttpResponse(mensaje)

def verContrato(request, idContrato):
    mensaje = f"Esta vista muestra el contrato con ID {idContrato}."
    return HttpResponse(mensaje)

def aprobarContrato(request, idContrato):
    mensaje = f"Esta vista aprueba el contrato con ID {idContrato}."
    return HttpResponse(mensaje)

def eliminarContrato(request, idContrato):
    mensaje = f"Esta vista elimina el contrato con ID {idContrato}."
    return HttpResponse(mensaje)
