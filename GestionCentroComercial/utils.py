from enum import Enum
from django.shortcuts import redirect
from django.urls import reverse

class TipoContrato(Enum):
    EMPRESA = 'Empresa'
    ARRENDAMIENTO = 'Arrendamiento'
    EMPLEADO = 'Empleado'

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
