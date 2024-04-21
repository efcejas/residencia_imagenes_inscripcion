from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Residente, Docente, Administrativo, RegistroAsistencia

class RegistroFormUsuario(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class RegistroFormResidente(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso']

class RegistroFormDocente(forms.ModelForm):
    class Meta:
        model = Docente
        fields = []

class RegistroFormAdministrativo(forms.ModelForm):
    class Meta:
        model = Administrativo
        fields = ['telefono']

class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ('latitud', 'longitud')
        