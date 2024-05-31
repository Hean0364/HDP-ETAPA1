from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import FiltroContratosForm, ContratoForm, EmpleadoForm, EmpresaForm, LocalForm
from django.http import HttpResponse
from .models import Contrato, ContratoArrendamiento, ContratoEmpleado, ContratoEmpresa
from Sistema.models import Empresa, Empleado, Local, Persona, Domicilio
from GestionCentroComercial.utils import TipoContrato, checkAdmin, requiereLogin, requiereAdmin, guardarContratoBase, guardarContratoArrendamiento, guardarEmpresa, test,guardarEmpleado,guardarContratoServicio,guardarContratoPersonal


def contratos(request):
    return redirect(contratosArrendamiento)

@requiereLogin
def contratosArrendamiento(request):
        # Obtener empresas para añadirlo al formulario
        empresas = Empresa.objects.all()

        contratanteOpciones = [(None, 'Todos')]  # Opción manual 'Todos'
        contratanteOpciones += [(empresa.empresaId, empresa.nombre) for empresa in empresas]

        # Obtener todos los contratos de arrendamiento
        contratosA = ContratoArrendamiento.objects.all()

        # Crear el formulario y asignar opciones al campo contratante
        form = FiltroContratosForm(request.POST)
        form.fields["contratante"].choices = contratanteOpciones

        if request.method == "POST":
            if form.is_valid():
                desde = form.cleaned_data["desde"]
                hasta = form.cleaned_data["hasta"]
                contratante = form.cleaned_data["contratante"]
                vigencia = form.cleaned_data["vigencia"]
                
                # Aplicamos filtros

                if desde:
                    contratosA = contratosA.filter(contrato__fechaInicio__gte=desde)
                if hasta:
                    contratosA = contratosA.filter(contrato__fechaFin__lte=hasta)
                if contratante:
                    contratosA = contratosA.filter(contratante__empresaId=contratante)
                if vigencia != "":
                    contratosA = contratosA.filter(contrato__vigente = vigencia)

        return render(request, "contratosBase.html", {"contratos": contratosA, "form": form,'esAdministrador': checkAdmin(request)})

@requiereLogin
def contratosServicio(request):
        # Obtener empresas para añadirlo al formulario
        empresas = Empresa.objects.all()

        contratanteOpciones = [(None, 'Todos')]  # Opción manual 'Todos'
        contratanteOpciones += [(empresa.empresaId, empresa.nombre) for empresa in empresas]

        # Obtener todos los contratos de arrendamiento
        contratosA = ContratoEmpresa.objects.all()

        # Crear el formulario y asignar opciones al campo contratante
        form = FiltroContratosForm(request.POST)
        form.fields["contratante"].choices = contratanteOpciones

        if request.method == "POST":
            if form.is_valid():
                desde = form.cleaned_data["desde"]
                hasta = form.cleaned_data["hasta"]
                contratante = form.cleaned_data["contratante"]
                vigencia = form.cleaned_data["vigencia"]
                
                # Aplicamos filtros

                if desde:
                    contratosA = contratosA.filter(contrato__fechaInicio__gte=desde)
                if hasta:
                    contratosA = contratosA.filter(contrato__fechaFin__lte=hasta)
                if contratante:
                    contratosA = contratosA.filter(contratante__empresaId=contratante)
                if vigencia != "":
                    contratosA = contratosA.filter(contrato__vigente = vigencia)

        return render(request, "contratosBase.html", {"contratos": contratosA, "form": form,'esAdministrador': checkAdmin(request)})

@requiereLogin
def contratosPersonal(request):
        # Obtener empresas para añadirlo al formulario
        empleados = Empleado.objects.all()

        contratanteOpciones = [(None, 'Todos')]  # Opción manual 'Todos'
        contratanteOpciones += [(empleado.empleadoId, empleado.persona.nombre) for empleado in empleados]

        # Obtener todos los contratos de arrendamiento
        contratosA = ContratoEmpleado.objects.all()

        # Crear el formulario y asignar opciones al campo contratante
        form = FiltroContratosForm(request.POST)
        form.fields["contratante"].choices = contratanteOpciones

        if request.method == "POST":
            if form.is_valid():
                desde = form.cleaned_data["desde"]
                hasta = form.cleaned_data["hasta"]
                contratante = form.cleaned_data["contratante"]
                vigencia = form.cleaned_data["vigencia"]
                
                # Aplicamos filtros

                if desde:
                    contratosA = contratosA.filter(contrato__fechaInicio__gte=desde)
                if hasta:
                    contratosA = contratosA.filter(contrato__fechaFin__lte=hasta)
                if contratante:
                    contratosA = contratosA.filter(contratante__empleadoId=contratante)
                if vigencia != "":
                    contratosA = contratosA.filter(contrato__vigente = vigencia)

        return render(request, "contratosBase.html", {"contratos": contratosA, "form": form,'esAdministrador': checkAdmin(request)})

@requiereLogin
def contratosFiltrados(request, tipo_contrato, filtro_empresa, desde_fecha, vigente):
    mensaje = f"Esta vista maneja los contratos filtrados por tipo de contrato: {tipo_contrato}, empresa: {filtro_empresa}, desde fecha: {desde_fecha}, y vigente: {vigente}."
    return HttpResponse(mensaje)

@requiereLogin
def contratosPersonalFiltrados(request, filtro_persona, desde_fecha, vigente):
    mensaje = f"Esta vista maneja los contratos de personal filtrados por persona: {filtro_persona}, desde fecha: {desde_fecha}, y vigente: {vigente}."
    return HttpResponse(mensaje)



def guardarModeloFormularioContratoBase(contratoBase, contratista, fechaInicio, fechaFin, Vigente, Contenido):
    contratoBase

@requiereLogin
def nuevoContrato(request, tipoContrato="arrendamiento"):
    esAdmin = checkAdmin(request)

    if request.method == "GET":
        formularioBase = ContratoForm()
        
        if esAdmin:
            formularioBase.fields['vigente'].disabled = False

        formularioBase.fields['contratista'].initial = Empleado.objects.get(user=request.user)

        if tipoContrato==TipoContrato.ARRENDAMIENTO_ARRENDAMIENTO.value.lower():
            #formularioContratoArrendamiento(request, formularioBase, esAdmin)
            formularioEmpresa = EmpresaForm()
            formularioLocal = LocalForm()
            
            locales = Local.objects.all()
            localesOpciones = [(local.localId, local) for local in locales]
            formularioLocal.fields["locales"].choices = localesOpciones
            
            print(formularioLocal.fields["locales"].choices)
            print(localesOpciones)
            return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin})
            
        elif tipoContrato==TipoContrato.SERVICIO_EMPRESA.value.lower():
            print("SE EJECUTO")
            formularioEmpresa = EmpresaForm(request.POST)
            return render(request,"formularioContratoServicio.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa, "esAdministrador": esAdmin})
        
        elif tipoContrato==TipoContrato.PERSONAL_EMPLEADO.value.lower():
            formularioEmpleado = EmpleadoForm(request.POST)
            return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin})
        else: # nunca debería de suceder
            return HttpResponse("Error")
    else: # es un request en método "POST"

        if tipoContrato==TipoContrato.ARRENDAMIENTO_ARRENDAMIENTO.value.lower():
            
            # Formularios
            # Datos de todos los contratos
            formularioBase = ContratoForm(request.POST) 
            formularioEmpresa = EmpresaForm(request.POST)
            formularioLocal = LocalForm(request.POST)

            # Control
            if esAdmin:
                formularioBase.fields['vigente'].disabled = False

            formularioBase.fields['contratista'].initial = Empleado.objects.get(user=request.user)

            locales = Local.objects.all()
            localesOpciones = [(local.localId, local) for local in locales]
            formularioLocal.fields["locales"].choices = localesOpciones
            
            # Datos del contrato particular
    
            if formularioBase.is_valid() & formularioEmpresa.is_valid() & formularioLocal.is_valid():
                # Modelo contrato particular
                nuevoContratoBase = Contrato()
                nuevoContratoArrendamiento = ContratoArrendamiento(contrato=nuevoContratoBase)
                nuevaPersona = Persona()
                nuevaEmpresa = Empresa(representante=nuevaPersona)

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

                
                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect(referer) 
            else:
                mensaje = "Alguno de los datos ingresados no son válidos."
                return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin, "error":mensaje})


        elif tipoContrato==TipoContrato.SERVICIO_EMPRESA.value.lower():
            # Formularios
            # Datos de todos los contratos
            formularioBase = ContratoForm(request.POST) 
            formularioEmpresa = EmpresaForm(request.POST)

            # Control
            if esAdmin:
                formularioBase.fields['vigente'].disabled = False

            formularioBase.fields['contratista'].initial = Empleado.objects.get(user=request.user)

            if formularioBase.is_valid() & formularioEmpresa.is_valid():
                # Modelo contrato particular
                nuevoContratoBase = Contrato()
                nuevoContratoServicio = ContratoEmpresa(contrato=nuevoContratoBase)
                nuevaPersona = Persona()
                nuevaEmpresa = Empresa(representante=nuevaPersona)
                
                # Limpiamos datos obtenidos en los formularios
                datosContratoBase = formularioBase.cleaned_data
                datosEmpresa = formularioEmpresa.cleaned_data

                # Guardar contrato base
                guardarContratoBase(nuevoContratoBase, datosContratoBase)

                # Guardar empresa y representante
                guardarEmpresa(nuevaEmpresa, nuevaPersona, datosEmpresa)

                # Guardar contrato de arrendamiento
                guardarContratoServicio(nuevoContratoServicio, nuevaEmpresa)

                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect(referer) 
            
            else:
                mensaje = "Alguno de los datos ingresados no son válidos."
                return render(request,"formularioContratoServicio.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa, "esAdministrador": esAdmin, "error":mensaje})

            
        elif tipoContrato==TipoContrato.PERSONAL_EMPLEADO.value.lower():
            
            # Formularios
            # Datos de todos los contratos
            formularioBase = ContratoForm(request.POST) 
            formularioEmpleado = EmpleadoForm(request.POST)

            # Control
            if esAdmin:
                formularioBase.fields['vigente'].disabled = False

            formularioBase.fields['contratista'].initial = Empleado.objects.get(user=request.user)
            
            # Datos del contrato particular
            if formularioBase.is_valid() & formularioEmpleado.is_valid():
                # Modelo contrato particular
                nuevoContratoBase = Contrato()
                nuevoContratoPersonal = ContratoEmpleado(contrato=nuevoContratoBase)
                nuevaPersona = Persona()
                nuevoDomicilio = Domicilio()
                nuevoEmpleado = Empleado(persona=nuevaPersona, domicilio=nuevoDomicilio)

                # Limpiamos datos obtenidos en los formularios
                datosContratoBase = formularioBase.cleaned_data
                datosEmpleado = formularioEmpleado.cleaned_data
                
                # Metodos de guardado
                guardarContratoBase(nuevoContratoBase, datosContratoBase)
                guardarEmpleado(nuevoEmpleado, nuevaPersona, nuevoDomicilio, datosEmpleado)
                guardarContratoPersonal(nuevoContratoPersonal, nuevoEmpleado)

                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect(referer) 

            else:
                mensaje = "Alguno de los datos ingresados no son válidos."
                return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin, "error":mensaje})
        
        else:
            # Regresar
            return HttpResponse("Error")
            


        

# ******************************************************************************************************************    

def formularioContratoArrendamiento(request, formularioBase, esAdmin):
    formularioEmpresa = EmpresaForm(request.POST)
    formularioLocal = LocalForm(request.POST)
    return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin})

def formularioContratoEmpleado(request, formularioBase, esAdmin):
    
    formularioEmpleado = EmpleadoForm(request.POST)
    return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin})

def formularioContratoServicio(request, formularioBase, esAdmin):
    formularioEmpresa = EmpresaForm(request.POST)
    return render(request,"formularioContratoServicio.html",{"formBase":formularioBase, "formEmpresa":formularioEmpresa, "esAdministrador": esAdmin})

@requiereLogin
def editarContrato(request, contratoId):
    mensaje = f"Esta vista edita el contrato con ID {contratoId}."
    return HttpResponse(mensaje)

@requiereLogin
def verContrato(request, contratoId):
    mensaje = f"Esta vista muestra el contrato con ID {contratoId}."
    return HttpResponse(mensaje)

@requiereLogin
@requiereAdmin
def aprobarContrato(request, contratoId):
    mensaje = f"Esta vista aprueba el contrato con ID {contratoId}."
    return HttpResponse(mensaje)

@requiereLogin
@requiereAdmin
def eliminarContrato(request, contratoId):
    mensaje = f"Esta vista elimina el contrato con ID {contratoId}."
    return HttpResponse(mensaje)
