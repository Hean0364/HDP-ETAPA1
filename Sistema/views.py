from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

def ingresar(request):
    return HttpResponse("Pantalla Login")

def cerrarSesion(request):
    return HttpResponse("Pantalla Cerrar Sesion")