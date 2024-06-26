from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Residente, Docente, Administrativo, RegistroAsistencia, Sedes, EvaluacionPeriodica

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

# Formularios relacionados con la asistencia

class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ('latitud', 'longitud')

# Formularios relacionados con la evaluación periódica

class EvaluacionPeriodicaForm(forms.ModelForm):
    class Meta:
        model = EvaluacionPeriodica
        fields = ['residente', 'aspecto_positivo', 'aspecto_negativo', 'nota']
        labels = {
            'aspecto_positivo': 'Aspecto positivo',
            'aspecto_negativo': 'Aspecto negativo',
            'nota': 'Nota',
        }
        exclude = ['evaluador', 'fecha']
        help_texts = {
            'aspecto_positivo': 'Ingrese un aspecto positivo del residente.',
            'aspecto_negativo': 'Ingrese un aspecto negativo del residente.',
            'nota': 'Ingrese una nota del 0 al 10.',
        }
        widgets = {
            'aspecto_positivo': forms.Textarea(attrs={'rows': 3}),
            'aspecto_negativo': forms.Textarea(attrs={'rows': 3}),
        }
        
# Formularios relacionados con la gestión de residentes

# Formularios relacionados con herramientas útiles para los residentes

class WashoutSuprarrenalForm(forms.Form):
    HU_sin_contraste = forms.FloatField(label='HU - fase sin contraste', required=False, help_text='Ingrese el valor de HU en la fase sin contraste.')
    HU_contraste_minuto = forms.FloatField(label='HU - fase portal', required=True, help_text='Ingrese el valor de HU en la fase portal.')
    HU_contraste_retraso = forms.FloatField(label='HU - fase retardada', required=True, help_text='Ingrese el valor de HU en la fase retardada (a los 15 min).')

    class Meta:
        widgets = {
            'HU_sin_contraste': forms.NumberInput(attrs={'step': '0.1'}),
            'HU_contraste_minuto': forms.NumberInput(attrs={'step': '0.1'}),
            'HU_contraste_retraso': forms.NumberInput(attrs={'step': '0.1'}),
        }

# Forumularios para la creación de sedes
class SedeForm(forms.ModelForm):
    class Meta:
        model = Sedes
        fields = ['nombre_sede', 'direccion', 'telefono', 'referente']

        help_texts = {
            'nombre_sede': 'El nombre de la sede debe ser único, generalmente correspondiente al barrio, zona o calle de ubicación. Ejemplo: "Junín".',
            'referente': 'Anteponga "Dr." o "Dra." al nombre del referente según corresponda.',
        }
        