from django.urls import path
from . import views

urlpatterns = [
    path('', views.contratosArrendamiento, name='contratosArrendamiento'),  # Vista por defecto para contratos de arrendamiento
    path('arrendamiento/', views.contratosArrendamiento, name='contratosArrendamiento'),  # Vista para contratos de arrendamiento
    path('servicio/', views.contratosServicio, name='contratosServicio'),  # Vista para contratos de servicio
    path('personal/', views.contratosPersonal, name='contratosPersonal'),  # Vista para contratos de personal
    
    # URLs filtradas
    path('<tipoContrato>/<filtroEmpresa>/<desdeFecha>/<vigente>/', views.contratosFiltrados, name='contratosFiltrados'),
    path('personal/<filtroPersona>/<desdeFecha>/<vigente>/', views.contratosPersonalFiltrados, name='contratosPersonalFiltrados'),

    path('crear/', views.nuevoContrato, name='nuevoContrato'),  # Vista para crear un nuevo contrato

    path('crear/<tipoContrato>/', views.nuevoContrato, name='nuevoContrato'),  # Vista para crear un nuevo contrato
    path('<int:idContrato>/editar/', views.editarContrato, name='editarContrato'),  # Vista para editar un contrato existente
    path('<int:idContrato>/ver/', views.verContrato, name='verContrato'),  # Vista para ver un contrato existente
    path('<int:idContrato>/aprobar/', views.aprobarContrato, name='aprobarContrato'),  # Vista para aprobar un contrato
    path('<int:idContrato>/eliminar/', views.eliminarContrato, name='eliminarContrato'),  # Vista para eliminar un contrato
]
