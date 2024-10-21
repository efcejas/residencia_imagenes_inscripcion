from django import forms
from .models import Paciente, PacienteRegion, RegionEcografia

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'dni',
            'nombre',
            'apellido',
            # Otros campos si es necesario
        ]
        widgets = {
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el DNI sin puntos',
                'aria-describedby': 'dniHelp',  # Accesibilidad Bootstrap
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        # Eliminar puntos y espacios
        dni = dni.replace('.', '').replace(' ', '')
        # Verificar que el DNI sea un número y tenga exactamente 8 dígitos
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError("El DNI debe ser un número de 8 dígitos sin puntos ni espacios.")
        return dni


class PacienteRegionForm(forms.ModelForm):
    regiones = forms.ModelMultipleChoiceField(
        queryset=RegionEcografia.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Regiones'
    )
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Cantidad',
        help_text='Cantidad de veces que se repite esta región (por ejemplo, rodillas x2).'
    )

    class Meta:
        model = PacienteRegion
        fields = ['regiones', 'empresa', 'cantidad']
