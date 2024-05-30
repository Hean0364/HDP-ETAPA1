from django import forms

class FiltroContratosForm(forms.Form):
    desde = forms.DateField(label='Desde', required=False)
    hasta = forms.DateField(label='Hasta', required=False)
    contratante = forms.ChoiceField(label='Contratante', choices=[], required=False)
    vigencia = forms.ChoiceField(label='Estado de vigencia', choices=[('', 'Todos'), ('vigentes', 'Vigentes'), ('no_vigentes', 'No Vigentes')], required=False)

