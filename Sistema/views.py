from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
#from .forms import TaskForm
# Create your views here.

def home(request):
    is_admin = request.user.groups.filter(name='Administrador').exists()
    return render(request, 'home.html', {'is_admin': is_admin})

def ingresar(request):
    # Si el método de solicitud es GET, muestra el formulario de inicio de sesión
    if request.method == "GET":
        return render(request, "login.html", {
            "form": AuthenticationForm  # Pasar el formulario de autenticación al contexto del template
        })
    else:
        # Si el método de solicitud es POST, intenta autenticar al usuario
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            # Si la autenticación falla, vuelve a mostrar el formulario con un mensaje de error
            return render(request, "login.html", {
                "form": AuthenticationForm,  # Pasar el formulario de autenticación al contexto del template
                "error": "Contraseña o usuario incorrecto."  # Mensaje de error para mostrar en el formulario
            })
        else:
            # Si la autenticación es exitosa, inicia sesión y redirige al usuario a la página de tareas
            login(request, user)
            return redirect("home")
        

def cerrarSesion(request):
    logout(request)
    return redirect("home")