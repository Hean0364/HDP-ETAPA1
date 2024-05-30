"""
URL configuration for GestionCentroComercial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from Sistema import views as SistemaViews

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para el panel de administración
    path('login/', SistemaViews.ingresar, name='login'),  # URL para el inicio de sesión
    path('logout/', SistemaViews.cerrarSesion, name='logout'),  # URL para cerrar sesión y redireccionar al inicio
    path('contratos/', include('GestionContratos.urls')),  # URLs para la aplicación "Contratos"
]