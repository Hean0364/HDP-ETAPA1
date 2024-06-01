from .models import Contrato, ContratoEmpleado, ContratoEmpresa, ContratoArrendamiento
from django.http import HttpResponse


def contratoTipoDesdeContratoBase(contratoBase):
    tipoPersonal = None
    tipoServicio = None
    tipoArrendamiento = None

    try:
        tipoPersonal = ContratoEmpleado.objects.get(contrato=contratoBase)
    except ContratoEmpleado.DoesNotExist:
        pass

    try:
        tipoServicio = ContratoEmpresa.objects.get(contrato=contratoBase)
    except ContratoEmpresa.DoesNotExist:
        pass

    try:
        tipoArrendamiento = ContratoArrendamiento.objects.get(contrato=contratoBase)
    except ContratoArrendamiento.DoesNotExist:
        pass

    contratoEspecifico = None

    if tipoArrendamiento:
        contratoEspecifico = tipoArrendamiento
    elif tipoServicio:
        contratoEspecifico = tipoServicio
    elif tipoPersonal:
        contratoEspecifico = tipoPersonal
    else:
        raise Exception("Tipo no definido")

    return contratoEspecifico