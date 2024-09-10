from django import forms
from .models import CasoInteresante, ImagenCasoInteresante, Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'dni']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el DNI sin puntos ni guiones'}),
        }

class CasoInteresanteForm(forms.ModelForm):
    class Meta:
        model = CasoInteresante
        fields = [
            'id_estudio', 'sede', 'fecha', 'tipo_estudio',
            'contraste_ev', 'contraste_or', 'region_anatomica',
            'sistema', 'organo', 'especialidad', 'descripcion',
            'hallazgos', 'fregmento_informe', 'etiquetas',
        ]
        widgets = {
            'id_estudio': forms.TextInput(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo_estudio': forms.Select(attrs={'class': 'form-control'}),
            'contraste_ev': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contraste_or': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'region_anatomica': forms.Select(attrs={'class': 'form-control'}),
            'sistema': forms.Select(attrs={'class': 'form-control'}),
            'organo': forms.Select(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hallazgos': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'fregmento_informe': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'etiquetas': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ImagenCasoInteresanteForm(forms.ModelForm):
    class Meta:
        model = ImagenCasoInteresante
        fields = ['imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }
