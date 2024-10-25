from django import forms
from django.utils import timezone
from .models import Paciente, PacienteRegion, RegionEcografia, Empresa

class EmpresaForm(forms.Form):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(), 
        label="Seleccione la Empresa", 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['dni', 'nombre', 'apellido']
        widgets = {
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PacienteRegionForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.none(),
        label='Empresa',
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    regiones = forms.ModelMultipleChoiceField(
        queryset=RegionEcografia.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Regiones'
    )
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Cantidad',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PacienteRegion
        fields = ['regiones', 'empresa', 'cantidad', 'fecha']