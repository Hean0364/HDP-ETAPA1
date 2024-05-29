from django.shortcuts import render
from django.http import HttpResponse

def contratosArrendamiento(request):
    return HttpResponse("Esta vista maneja los contratos de arrendamiento.")

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

def editarContrato(request, id_contrato):
    mensaje = f"Esta vista edita el contrato con ID {id_contrato}."
    return HttpResponse(mensaje)

def verContrato(request, id_contrato):
    mensaje = f"Esta vista muestra el contrato con ID {id_contrato}."
    return HttpResponse(mensaje)

def aprobarContrato(request, id_contrato):
    mensaje = f"Esta vista aprueba el contrato con ID {id_contrato}."
    return HttpResponse(mensaje)

def eliminarContrato(request, id_contrato):
    mensaje = f"Esta vista elimina el contrato con ID {id_contrato}."
    return HttpResponse(mensaje)
