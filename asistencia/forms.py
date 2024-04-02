from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Residente, RegistroAsistencia

class ResidenteRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Residente
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso')
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'dni': 'DNI',
            'first_name': 'Nombre/s',
            'last_name': 'Apellido/s',
            'fecha_nacimiento': 'Fecha de nacimiento',
            'matricula': 'Matrícula',
            'telefono': 'Teléfono',
            'fecha_de_ingreso': 'Fecha de ingreso a la residencia'
        }
        error_messages = {
            'username': {
                'unique': 'Ya existe un residente con este nombre de usuario.'
            },
            'email': {
                'unique': 'Ya existe un residente con este correo electrónico.'
            },
            'dni': {
                'unique': 'Ya existe un residente con este DNI.'
            },
            'matricula': {
                'unique': 'Ya existe un residente con esta matrícula.'
            }
        }

class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ('latitud', 'longitud')
        