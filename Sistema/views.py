from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
#from .forms import TaskForm
# Create your views here.
from GestionCentroComercial.utils import checkAdmin

def home(request):
    return render(request, 'home.html', {'esAdministrador': checkAdmin(request)})

def ingresar(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm()})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "login.html", {"form": AuthenticationForm(), "error": "Contraseña o usuario incorrecto."})
        else:
            login(request, user)
            return redirect("home")
        

def cerrarSesion(request):
    logout(request)
    return redirect("home")