from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import FiltroContratosForm, ContratoForm, EmpleadoForm, EmpresaForm, LocalForm
from django.http import HttpResponse
from .models import Contrato, ContratoArrendamiento, ContratoEmpleado, ContratoEmpresa
from Sistema.models import Empresa, Empleado, Local, Persona, Domicilio
from GestionCentroComercial.utils import TipoContrato, checkAdmin, requiereLogin, requiereAdmin, guardarContratoBase, guardarContratoArrendamiento, guardarEmpresa, test,guardarEmpleado,guardarContratoServicio,guardarContratoPersonal, hacerFormularioReadonly
from .utils import contratoTipoDesdeContratoBase
from GestionCentroComercial.utils import definirCamposContratoBase, definirCamposEmpresa, definirCamposEmpleado, definirCamposContratoArrendamiento, definirCamposContratoServicio, definirCamposContratoPersonal, asignacionContratoArrendamiento, asignacionContratoPersonal, asignacionContratoServicio

def contratos(request):
    return redirect('contratosArrendamiento')

@requiereLogin
def contratosArrendamiento(request):

    # Obtener todos los contratos de arrendamiento
    contratosA = ContratoArrendamiento.objects.all().order_by('-id')

    # Crear el formulario
    form = FiltroContratosForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        desde = form.cleaned_data["desde"]
        hasta = form.cleaned_data["hasta"]
        contratante = form.cleaned_data["contratante"]
        vigencia = form.cleaned_data["vigencia"]

        # Aplicar filtros
        if desde:
            contratosA = contratosA.filter(contrato__fechaInicio__gte=desde)
        if hasta:
            contratosA = contratosA.filter(contrato__fechaFin__lte=hasta)
        if contratante:
            contratosA = contratosA.filter(contratante__nombre__icontains=contratante)
        if vigencia != "":
            contratosA = contratosA.filter(contrato__vigente=vigencia)

    return render(request, "contratosBase.html", {
        "contratos": contratosA,
        "form": form,
        'esAdministrador': checkAdmin(request),
        "userActual": request.user
    })

@requiereLogin
def contratosServicio(request):
    # Obtener todas las empresas para añadirlo al formulario

    # Obtener todos los contratos de servicio
    contratosA = ContratoEmpresa.objects.all().order_by('-id')

    # Crear el formulario
    form = FiltroContratosForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        desde = form.cleaned_data["desde"]
        hasta = form.cleaned_data["hasta"]
        contratante = form.cleaned_data["contratante"]
        vigencia = form.cleaned_data["vigencia"]

        # Aplicar filtros
        if desde:
            contratosA = contratosA.filter(contrato__fechaInicio__gte=desde)
        if hasta:
            contratosA = contratosA.filter(contrato__fechaFin__lte=hasta)
        if contratante:
            contratosA = contratosA.filter(contratante__nombre__icontains=contratante)
        if vigencia != "":
            contratosA = contratosA.filter(contrato__vigente=vigencia)

    return render(request, "contratosBase.html", {
        "contratos": contratosA,
        "form": form,
        'esAdministrador': checkAdmin(request),
        "userActual": request.user
    })

@requiereLogin
def contratosPersonal(request):
    
    # Obtener todos los contratos de personal
    contratosA = ContratoEmpleado.objects.all().order_by('-id')

    # Crear el formulario
    form = FiltroContratosForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        desde = form.cleaned_data["desde"]
        hasta = form.cleaned_data["hasta"]
        contratante = form.cleaned_data["contratante"]
        vigencia = form.cleaned_data["vigencia"]

        # Aplicar filtros
        if desde:
            contratosA = contratosA.filter(contrato__fechaInicio__gte=desde)
        if hasta:
            contratosA = contratosA.filter(contrato__fechaFin__lte=hasta)
        if contratante:
            contratosA = contratosA.filter(contratante__persona__nombre__icontains=contratante)
        if vigencia != "":
            contratosA = contratosA.filter(contrato__vigente=vigencia)
    

    return render(request, "contratosBase.html", {
        "contratos": contratosA,
        "form": form,
        'esAdministrador': checkAdmin(request),
        "userActual": request.user
    })
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
            return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin, "titulo": "Crear contrato"})
        
        elif tipoContrato==TipoContrato.SERVICIO_EMPRESA.value.lower():
            formularioEmpresa = EmpresaForm(request.POST)
            return render(request,"formularioContratoServicio.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa, "esAdministrador": esAdmin, "titulo": "Crear contrato"})
        
        elif tipoContrato==TipoContrato.PERSONAL_EMPLEADO.value.lower():
            formularioEmpleado = EmpleadoForm(request.POST)
            return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin, "titulo": "Crear contrato"})
        
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
                return redirect('contratosArrendamiento') 
            else:
                mensaje = "Alguno de los datos ingresados no son válidos."
                return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin, "error":mensaje,"titulo": "Crear contrato"})


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
                asignacionContratoServicio(**asignacion)

                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect('contratosServicio')             
            else:
                mensaje = "Alguno de los datos ingresados no son válidos."
                return render(request,"formularioContratoServicio.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa, "esAdministrador": esAdmin, "error":mensaje, "titulo": "Crear contrato"})

            
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

                asignacionContratoPersonal(**asignacion)

                referer = request.META.get('HTTP_REFERER', reverse('home'))
                return redirect('contratosPersonal') 
            else:
                mensaje = "Alguno de los datos ingresados no son válidos."
                return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin, "error":mensaje, "titulo": "Crear contrato"})
        
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
        formularioBase = ContratoForm()
        print(contrato)
        # Metodos de control
        if esAdmin:
            formularioBase.fields['vigente'].disabled = False    
        print(contrato.tipo)
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
                return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin, "titulo": "Editar contrato"})
            
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
                    return redirect('contratosArrendamiento') 

                else:
                    mensaje = "Alguno de los datos ingresados no son válidos."
                    return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin, "error":mensaje, "titulo": "Editar contrato"})
        
        elif contrato.tipo==TipoContrato.EMPLEADO.value:
            # Creamos formularios
            formularioEmpleado = EmpleadoForm()
            
            # Operaciones adicionales

            # Definimos instancias 
            actualContratoBase = contratoBase # todos
            actualContratoPersonal = contrato
            actualEmpleado = contrato.contratante

            # Llenamos formularios
            formularioBase = definirCamposContratoBase(actualContratoBase, formularioBase)
            formularioEmpleado = definirCamposEmpleado(actualEmpleado, formularioEmpleado)

            formularioBase.fields["contratista"].initial = actualContratoBase.contratista
            
            if request.method == "GET":
                return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin, "titulo": "Editar contrato"})
            else:
                formularioBase = ContratoForm(request.POST)
                formularioEmpleado = EmpleadoForm(request.POST)

                # Control
                formularioBase.fields["contratista"].initial = actualContratoBase.contratista

                if formularioBase.is_valid() and formularioEmpleado.is_valid():
                    # Diccionario de asignación
                    asignacion = {
                        "formularioBase": formularioBase,
                        "formularioEmpleado": formularioEmpleado,
                        "nuevoContratoBase": actualContratoBase,
                        "nuevoContratoPersonal": actualContratoPersonal,
                        "nuevaPersona": actualEmpleado.persona,
                        "nuevoDomicilio": actualEmpleado.domicilio,
                        "nuevoEmpleado": actualEmpleado
                    }

                    asignacionContratoPersonal(**asignacion)

                    return redirect('contratosPersonal') 
                else:
                    mensaje = "Alguno de los datos ingresados no son válidos."
                    return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin, "error":mensaje, "titulo": "Editar contrato"})

        elif contrato.tipo==TipoContrato.EMPRESA.value:

            # Creamos formularios
            formularioEmpresa = EmpresaForm()
            
            # Operaciones adicionales

            # Definimos instancias 
            actualContratoBase = contratoBase # todos
            actualContratoServicio = contrato
            actualEmpresa = contrato.contratante

            formularioBase = definirCamposContratoBase(actualContratoBase, formularioBase)
            formularioEmpresa = definirCamposEmpresa(actualEmpresa, formularioEmpresa)

            formularioBase.fields["contratista"].initial = actualContratoBase.contratista

            if request.method == "GET":
                return render(request,"formularioContratoServicio.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa, "esAdministrador": esAdmin, "titulo": "Editar contrato"})
            
            else:
                formularioBase = ContratoForm(request.POST)
                formularioEmpresa = EmpresaForm(request.POST)

                # Control
                formularioBase.fields["contratista"].initial = actualContratoBase.contratista

                if formularioBase.is_valid() and formularioEmpresa.is_valid():
                    #TODO:
                    asignacion = {
                        "formularioBase": formularioBase,
                        "formularioEmpresa": formularioEmpresa,
                        "nuevoContratoBase": actualContratoBase,
                        "nuevoContratoServicio": actualContratoServicio,
                        "nuevaPersona": actualEmpresa.representante,
                        "nuevaEmpresa": actualEmpresa
                    }

                    # Llamada al método con el diccionario de asignación
                    asignacionContratoServicio(**asignacion)
    
                    referer = request.META.get('HTTP_REFERER', reverse('home'))
                    return redirect('contratosServicio') 

                else:
                    mensaje = "Alguno de los datos ingresados no son válidos."
                    return render(request,"formularioContratoServicio.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa, "esAdministrador": esAdmin, "error":mensaje, "titulo": "Editar contrato"})
        
        else:
            return HttpResponse("Error inesperado.")


        # FIXME: Fin
        mensaje = f"Esta vista edita el contrato con ID {contratoId}."
        return HttpResponse(mensaje)

# SIN IMPLEMENTAR
@requiereLogin
def verContrato(request, contratoId):
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
    
    permisos = True

    if not permisos:
        return redirect('contratos')        
    else:
        formularioBase = ContratoForm()
        print(contrato)
        # Metodos de control
        if esAdmin:
            formularioBase.fields['vigente'].disabled = False    
        print(contrato.tipo)
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

            formularioBase = hacerFormularioReadonly(formularioBase)
            formularioEmpresa = hacerFormularioReadonly(formularioEmpresa)
            formularioLocal = hacerFormularioReadonly(formularioLocal)

            if request.method == "GET":
                return render(request,"formularioContratoArrendamiento.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa,"formLocal":formularioLocal, "esAdministrador": esAdmin, "readOnly":True, "titulo": "Ver contrato"})
            
        elif contrato.tipo==TipoContrato.EMPLEADO.value:
            # Creamos formularios
            formularioEmpleado = EmpleadoForm()
            
            # Operaciones adicionales

            # Definimos instancias 
            actualContratoBase = contratoBase # todos
            actualContratoPersonal = contrato
            actualEmpleado = contrato.contratante

            # Llenamos formularios
            formularioBase = definirCamposContratoBase(actualContratoBase, formularioBase)
            formularioEmpleado = definirCamposEmpleado(actualEmpleado, formularioEmpleado)

            formularioBase.fields["contratista"].initial = actualContratoBase.contratista

            formularioBase = hacerFormularioReadonly(formularioBase)
            formularioEmpleado = hacerFormularioReadonly(formularioEmpleado)

            if request.method == "GET":
                return render(request,"formularioContratoEmpleado.html",{"formBase":formularioBase,"formEmpleado":formularioEmpleado,'esAdministrador': esAdmin, "readOnly":True, "titulo": "Ver contrato"})

        elif contrato.tipo==TipoContrato.EMPRESA.value:

            # Creamos formularios
            formularioEmpresa = EmpresaForm()
            
            # Operaciones adicionales

            # Definimos instancias 
            actualContratoBase = contratoBase # todos
            actualContratoServicio = contrato
            actualEmpresa = contrato.contratante

            formularioBase = definirCamposContratoBase(actualContratoBase, formularioBase)
            formularioEmpresa = definirCamposEmpresa(actualEmpresa, formularioEmpresa)

            formularioBase.fields["contratista"].initial = actualContratoBase.contratista

            formularioBase = hacerFormularioReadonly(formularioBase)
            formularioEmpresa = hacerFormularioReadonly(formularioEmpresa)

            if request.method == "GET":
                return render(request,"formularioContratoServicio.html",{"formBase":formularioBase,"formEmpresa":formularioEmpresa, "esAdministrador": esAdmin, "readOnly":True, "titulo": "Ver contrato"})
            
        else:
            return HttpResponse("Error inesperado.")



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
            if contrato.tipo==TipoContrato.ARRENDAMIENTO_ARRENDAMIENTO.value:
                # Elimina el contrato de la base de datos
                test()
            elif contrato.tipo==TipoContrato.EMPLEADO.value:
                test()
            elif contrato.tipo==TipoContrato.EMPRESA.value:
                test()
            else:
                raise  Exception("Contrato no coincide con su definición.")
            contratoBase.delete()
            exito = True
            return render(request, 'confirmarEliminacion.html', {'objeto': contrato, "mensajeExito": exito, 'esAdministrador': True})

        
        except Exception as ex:
            # Renderiza la plantilla de confirmación de eliminación con el mensaje de error
            return render(request, 'confirmarEliminacion.html', {'objeto': contrato, "mensajeExito": exito,'error': str(ex), 'esAdministrador': True})
