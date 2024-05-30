from django.urls import path
from . import views

urlpatterns = [
    path('', views.contratosArrendamiento, name='contratos'),  # Vista por defecto para contratos de arrendamiento
    path('arrendamiento/', views.contratosArrendamiento, name='contratosArrendamiento'),  # Vista para contratos de arrendamiento
    path('servicio/', views.contratosServicio, name='contratosServicio'),  # Vista para contratos de servicio
    path('personal/', views.contratosPersonal, name='contratosPersonal'),  # Vista para contratos de personal
    
    # URLs filtradas
    path('/<contratante>/<desdeFecha>/<hastaFecha>/<vigente>/', views.contratosFiltrados, name='contratosFiltrados'),
    path('personal/<filtroPersona>/<desdeFecha>/<vigente>/', views.contratosPersonalFiltrados, name='contratosPersonalFiltrados'),

    path('crear/', views.nuevoContrato, name='nuevoContrato'),  # Vista para crear un nuevo contrato

    path('crear/<tipoContrato>/', views.nuevoContrato, name='nuevoContrato'),  # Vista para crear un nuevo contrato
    path('<int:contratoId>/editar/', views.editarContrato, name='editarContrato'),  # Vista para editar un contrato existente
    path('<int:contratoId>/ver/', views.verContrato, name='verContrato'),  # Vista para ver un contrato existente
    path('<int:contratoId>/aprobar/', views.aprobarContrato, name='aprobarContrato'),  # Vista para aprobar un contrato
    path('<int:contratoId>/eliminar/', views.eliminarContrato, name='eliminarContrato'),  # Vista para eliminar un contrato
]
