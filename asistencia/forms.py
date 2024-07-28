from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Residente, Docente, Administrativo, RegistroAsistencia, Sedes, EvaluacionPeriodica, GruposResidentes, DisertantesClases, ClasificacionTematica

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

class AsistenciaFiltroForm(forms.Form):
    dia = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label='Seleccionar'
    )
    año = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('R1', 'R1'),
            ('R2', 'R2'),
            ('R3', 'R3'),
            ('R4', 'R4'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Año'
    )

# Formularios relacionados con la evaluación periódica

class SeleccionarAnoForm(forms.Form):
    OPCIONES_AÑO_CON_DEFECTO = [('', 'Todos')] + GruposResidentes.OPCIONES_AÑO
    año = forms.ChoiceField(
        choices=OPCIONES_AÑO_CON_DEFECTO, 
        required=False, 
        label='Año',
        help_text='Seleccione el año que desea evaluar.',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class EvaluacionPeriodicaForm(forms.ModelForm):
    class Meta:
        model = EvaluacionPeriodica
        fields = ['residente', 'aspecto_positivo', 'aspecto_negativo', 'nota']
        labels = {
            'aspecto_positivo': 'Aspecto positivo',
            'aspecto_negativo': 'Aspecto negativo',
            'nota': 'Nota',
        }
        widgets = {
            'residente': forms.Select(attrs={'class': 'form-select'}),
            'aspecto_positivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aspecto_negativo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nota': forms.Select(attrs={'class': 'form-select'}),
        }

# Formularios relacionados con el manejo de videos de clases

class VideoFilterForm(forms.Form):
    fecha_desde = forms.DateField(
        label='Desde',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    fecha_hasta = forms.DateField(
        label='Hasta',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    disertante = forms.ModelChoiceField(
        queryset=DisertantesClases.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    clasificacion_tematica = forms.ModelChoiceField(
        queryset=ClasificacionTematica.objects.all(),
        label='Área temática',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        fields = ['fecha_desde', 'fecha_hasta', 'disertante', 'clasificacion_tematica']

# Formularios relacionados con la gestión de residentes

class GruposResidentesForm(forms.ModelForm):
    año = forms.ChoiceField(choices=GruposResidentes.OPCIONES_AÑO, label='Año', widget=forms.Select())

    class Meta:
        model = GruposResidentes
        fields = ['residente', 'residencia', 'año']

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
        