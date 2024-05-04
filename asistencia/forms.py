from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Residente, Docente, Administrativo, RegistroAsistencia, Sedes

class RegistroFormUsuario(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="La contraseña debe ser única, tener al menos 8 caracteres, no ser comúnmente utilizada y no estar compuesta solo por números.",
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'autocapitalize': 'none'}),
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

        help_texts = {
            'username': 'Puedes usar letras, números y @/./+/-/_ solamente. Por ejemplo: juanito123',
        }

class RegistroFormResidente(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['dni', 'fecha_nacimiento', 'matricula', 'telefono', 'fecha_de_ingreso']

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'fecha_de_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }

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
        
# Forumularios para la creación de sedes
class SedeForm(forms.ModelForm):
    class Meta:
        model = Sedes
        fields = ['nombre_sede', 'direccion', 'telefono', 'referente']
        