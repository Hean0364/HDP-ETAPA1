from django import forms
from django.forms import ModelForm
from .models import Contrato, ContratoEmpresa, ContratoArrendamiento, ContratoEmpleado
from Sistema.models import Empleado, Persona, Empresa, Domicilio


class FiltroContratosForm(forms.Form):
    desde = forms.DateField(label='Desde', required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}))
    hasta = forms.DateField(label='Hasta', required=False, widget=forms.DateInput(attrs={'class': 'datepicker'}))
    contratante = forms.ChoiceField(label='Contratante', choices=[], required=False)
    vigencia = forms.ChoiceField(label='Estado de vigencia', choices=[('', 'Todos'), (True, 'Vigentes'), (False, 'No Vigentes')], required=False)

class EmpleadoForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    dui = forms.CharField(max_length=10)
    profesion = forms.CharField(max_length=50)
    pais = forms.CharField(max_length=50)
    departamento = forms.CharField(max_length=50)
    ciudad = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=100)

class EmpresaForm(forms.Form):
    empresaNombre = forms.CharField(max_length=100, label="Nombre de la Empresa")
    representanteNombre = forms.CharField(max_length=50, label="Nombre del Representante")
    representanteApellido = forms.CharField(max_length=50, label="Apellido del Representante")
    representanteDui = forms.CharField(max_length=10, label="DUI del Representante")

class ContratoForm(forms.Form):
    contratista = forms.ModelChoiceField(queryset=Empleado.objects.all(), label="Contratista", disabled=True)
    fechaInicio = forms.DateField(label="Fecha de Inicio", widget=forms.DateInput(attrs={'class': 'datepicker'}))
    fechaFin = forms.DateField(label="Fecha de Fin", widget=forms.DateInput(attrs={'class': 'datepicker'}))
    vigente = forms.BooleanField(initial=False, required=False, disabled=True, label="Vigente")
    contenido = forms.CharField(widget=forms.Textarea, label="Contenido")
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fechaInicio")
        fecha_fin = cleaned_data.get("fechaFin")

        if fecha_inicio and fecha_fin:
            if fecha_inicio >= fecha_fin:
                raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")
        return cleaned_data


class LocalForm(forms.Form):
    locales = forms.ChoiceField(label='Local', choices=[], required=False)
