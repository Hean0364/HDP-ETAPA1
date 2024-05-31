from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import FiltroContratosForm, ContratoForm, EmpleadoForm, EmpresaForm, LocalForm
from django.http import HttpResponse
from .models import Contrato, ContratoArrendamiento, ContratoEmpleado, ContratoEmpresa
from Sistema.models import Empresa, Empleado, Local, Persona, Domicilio
from GestionCentroComercial.utils import TipoContrato, checkAdmin, requiereLogin, requiereAdmin, guardarContratoBase, guardarContratoArrendamiento, guardarEmpresa, test,guardarEmpleado,guardarContratoServicio,guardarContratoPersonal
from .utils import contratoTipoDesdeContratoBase
from GestionCentroComercial.utils import definirCamposContratoBase, definirCamposEmpresa, definirCamposEmpleado, definirCamposContratoArrendamiento, definirCamposContratoServicio, definirCamposContratoPersonal, asignacionContratoArrendamiento, asignacionContratoPersonal, asignacionContratoServicio

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

        return render(request, "contratosBase.html", {"contratos": contratosA, "form": form,'esAdministrador': checkAdmin(request), "userActual":request.user})

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

        return render(request, "contratosBase.html", {"contratos": contratosA, "form": form,'esAdministrador': checkAdmin(request), "userActual":request.user})

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

        return render(request, "contratosBase.html", {"contratos": contratosA, "form": form,'esAdministrador': checkAdmin(request), "userActual":request.user})

@requiereLogin
def nuevoContrato(request, tipoContrato="arrendamiento"):
    esAdmin = checkAdmin(request)

    if request.method == "GET":
        formularioBase = ContratoForm()
        
        if esAdmin:
            formularioBase.fields['vigente'].disabled = False

        formularioBase.fields['contratista'].initial = Empleado.objects.get(user=request.user)

        if tipoContrato==TipoContrato.ARRENDAMIENTO_ARRENDAMIENTO.value.lower():
            formularioEmpresa = EmpresaForm()
            formularioLocal = LocalForm()
            
            locales = Local.objects.all()
            localesOpciones = [(local.localId, local) for local in locales]
            formularioLocal.fields["locales"].choices = localesOpciones
            
            print(formularioLocal.fields["locales"].choices)
            print(formularioEmpresa.is_valid())
            return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin})
        
        elif tipoContrato==TipoContrato.SERVICIO_EMPRESA.value.lower():
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
    
            if formularioBase.is_valid() and formularioEmpresa.is_valid() and formularioLocal.is_valid():
                
                # Modelo contrato particular
                nuevoContratoBase = Contrato()
                nuevoContratoArrendamiento = ContratoArrendamiento(contrato=nuevoContratoBase)
                nuevaPersona = Persona()
                nuevaEmpresa = Empresa(representante=nuevaPersona)

                asignaciones = {
                    "formularioBase": formularioBase,
                    "formularioEmpresa": formularioEmpresa,
                    "formularioLocal": formularioLocal,
                    "nuevoContratoBase": nuevoContratoBase,
                    "nuevoContratoArrendamiento": nuevoContratoArrendamiento,
                    "nuevaPersona": nuevaPersona,
                    "nuevaEmpresa": nuevaEmpresa
                }

                asignacionContratoArrendamiento(**asignaciones)

                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect('contratos') 
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

            if formularioBase.is_valid() and formularioEmpresa.is_valid():
                # Modelo contrato particular
                nuevoContratoBase = Contrato()
                nuevoContratoServicio = ContratoEmpresa(contrato=nuevoContratoBase)
                nuevaPersona = Persona()
                nuevaEmpresa = Empresa(representante=nuevaPersona)
                
                #TODO:
                asignacion = {
                    "formularioBase": formularioBase,
                    "formularioEmpresa": formularioEmpresa,
                    "nuevoContratoBase": nuevoContratoBase,
                    "nuevoContratoServicio": nuevoContratoServicio,
                    "nuevaPersona": nuevaPersona,
                    "nuevaEmpresa": nuevaEmpresa
                }

                # Llamada al método con el diccionario de asignación
                asignacionContratoPersonal(**asignacion)

                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect('contratos')             
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
            if formularioBase.is_valid() and formularioEmpleado.is_valid():
                # Modelo contrato particular
                nuevoContratoBase = Contrato()
                nuevoContratoPersonal = ContratoEmpleado(contrato=nuevoContratoBase)
                nuevaPersona = Persona()
                nuevoDomicilio = Domicilio()
                nuevoEmpleado = Empleado(persona=nuevaPersona, domicilio=nuevoDomicilio)

                asignacion = {
                    "formularioBase": formularioBase,
                    "formularioEmpleado": formularioEmpleado,
                    "nuevoContratoBase": nuevoContratoBase,
                    "nuevoContratoPersonal": nuevoContratoPersonal,
                    "nuevaPersona": nuevaPersona,
                    "nuevoDomicilio": nuevoDomicilio,
                    "nuevoEmpleado": nuevoEmpleado
                }

                asignacionContratoServicio(**asignacion)

                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect('contratos') 
            else:
                mensaje = "Alguno de los datos ingresados no son válidos."
                return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin, "error":mensaje})
        
        else:
            # Regresar
            return HttpResponse("Error")
            


@requiereLogin
def editarContrato(request, contratoId):
    # Validar permiso de acceso
    esAdmin = checkAdmin(request)
    
    # Obtener Contrato por contratoId
    try:
        contratoBase = Contrato.objects.get(contratoId=contratoId)
        # TsODO: eliminar este comentario 
        contrato = contratoTipoDesdeContratoBase(contratoBase)

        #contrato = ContratoArrendamiento()
    except:
        return redirect('contratos')

    permisos = esAdmin or contratoBase.contratista.user == request.user
    if not permisos:
        return redirect('contratos')        
    else:
        print("LLego a Inicio Algoritmo")
        formularioBase = ContratoForm()
        print(contrato)
        # Metodos de control
        if esAdmin:
            formularioBase.fields['vigente'].disabled = False    
        if contrato.tipo==TipoContrato.ARRENDAMIENTO_ARRENDAMIENTO.value:

            # Creamos formularios
            formularioEmpresa = EmpresaForm()
            formularioLocal = LocalForm()
            
            # Operaciones adicionales
            locales = Local.objects.all()
            localesOpciones = [(local.localId, local) for local in locales]
            formularioLocal.fields["locales"].choices = localesOpciones

            # Definimos instancias 
            actualContratoBase = contratoBase # todos
            actualContratoArrendamiento = contrato
            actualEmpresa = contrato.contratante

            formularioBase = definirCamposContratoBase(actualContratoBase, formularioBase)
            formularioEmpresa = definirCamposEmpresa(actualEmpresa, formularioEmpresa)
            formularioLocal = definirCamposContratoArrendamiento(actualContratoArrendamiento, formularioLocal)

            formularioBase.fields["contratista"].initial = actualContratoBase.contratista


            if request.method == "GET":
                return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin})
            
            else:
                formularioBase = ContratoForm(request.POST)
                formularioEmpresa = EmpresaForm(request.POST)
                formularioLocal = LocalForm(request.POST)

                # Control
                formularioBase.fields["contratista"].initial = actualContratoBase.contratista
                formularioLocal.reserva = actualContratoArrendamiento.reserva
                localesOpciones = [(local.localId, local) for local in locales]
                formularioLocal.fields["locales"].choices = localesOpciones
                
                if formularioBase.is_valid() and formularioEmpresa.is_valid() and formularioLocal.is_valid():
                    asignaciones = {
                        "formularioBase": formularioBase,
                        "formularioEmpresa": formularioEmpresa,
                        "formularioLocal": formularioLocal,
                        "nuevoContratoBase": actualContratoBase,
                        "nuevoContratoArrendamiento": actualContratoArrendamiento,
                        "nuevaPersona": actualEmpresa.representante,
                        "nuevaEmpresa": actualEmpresa
                    }

                    asignacionContratoArrendamiento(**asignaciones)
    
                    referer = request.META.get('HTTP_REFERER', reverse('home'))
                    return redirect('contratos') 

                else:
                    mensaje = "Alguno de los datos ingresados no son válidos."
                    return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin, "error":mensaje})
        
        elif contrato.tipo==TipoContrato.EMPRESA.value:
            # TODO:
            test()


        elif contrato.tipo==TipoContrato.EMPLEADO.value:
            # TODO:
            test()

        else:
            return HttpResponse("Error inesperado.")


        # FIXME: Fin
        mensaje = f"Esta vista edita el contrato con ID {contratoId}."
        return HttpResponse(mensaje)

# SIN IMPLEMENTAR
@requiereLogin
def verContrato(request, contratoId):
    mensaje = f"Esta vista muestra el contrato con ID {contratoId}."
    return HttpResponse(mensaje)

@requiereLogin
@requiereAdmin
def aprobarContrato(request, contratoId):
    try:
        contratoBase = Contrato.objects.get(contratoId=contratoId)
        contratoBase.vigente = True
        contratoBase.save()
        referer = request.META.get('HTTP_REFERER', reverse('home'))
        return redirect(referer) 
    except:
        return redirect('contratos')
    
@requiereLogin
@requiereAdmin
def desaprobarContrato(request, contratoId):
    try:
        contratoBase = Contrato.objects.get(contratoId=contratoId)
        contratoBase.vigente = False
        contratoBase.save()
        
        referer = request.META.get('HTTP_REFERER', reverse('home'))
        return redirect(referer) 
    except:
        return redirect('contratos')

@requiereLogin
@requiereAdmin
def eliminarContrato(request, contratoId):
    try:
        contratoBase = Contrato.objects.get(contratoId=contratoId)
        contrato = contratoTipoDesdeContratoBase(contratoBase)
    except:
        return redirect('contratos')
    
    exito = False

    if request.method == "GET":
        # Renderiza la plantilla de confirmación de eliminación con los datos del contrato
        return render(request, 'confirmarEliminacion.html', {'objeto': contrato, 'esAdministrador': True})
    
    else:  # Significa que se recibe una solicitud "POST" confirmando la eliminación
        try:
            contrato.delete()  # Elimina el contrato de la base de datos
            exito = True
            return render(request, 'confirmarEliminacion.html', {'objeto': contrato, "mensajeExito": exito, 'esAdministrador': True})

        
        except Exception as ex:
            # Renderiza la plantilla de confirmación de eliminación con el mensaje de error
            return render(request, 'confirmarEliminacion.html', {'objeto': contrato, "mensajeExito": exito,'error': str(ex), 'esAdministrador': True})
