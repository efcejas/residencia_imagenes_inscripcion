from django import forms
from .models import CasoInteresante, ImagenCasoInteresante, Paciente, Organo, Region, Sistema, Especialidad

class CasoInteresanteFilterForm(forms.Form):
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Fecha desde'
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Fecha hasta'
    )
    patologia = forms.ChoiceField(
        required=False,
        choices=[('', 'Seleccione')] + [(hallazgo, hallazgo) for hallazgo in CasoInteresante.objects.values_list('hallazgos', flat=True).distinct()],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Patología'
    )
    organo = forms.ModelChoiceField(
        required=False,
        queryset=Organo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Órgano',
        empty_label='Seleccione'
    )
    region_anatomica = forms.ModelChoiceField(
        required=False,
        queryset=Region.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Región anatómica',
        empty_label='Seleccione'
    )
    sistema = forms.ModelChoiceField(
        required=False,
        queryset=Sistema.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sistema',
        empty_label='Seleccione'
    )
    especialidad = forms.ModelChoiceField(
        required=False,
        queryset=Especialidad.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Especialidad',
        empty_label='Seleccione'
    )
    etiqueta = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Etiqueta'
    )

class PacienteSearchForm(forms.Form):
    dni = forms.CharField(
        label='',
        max_length=20,
        help_text='Veamos primero si ya existe un registro para el paciente al cual se desea crear el nuevo caso, ingresando su DNI sin puntos.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'DNI'
            }
        )
    )

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        # Eliminar todos los caracteres que no sean dígitos
        dni_normalizado = ''.join(filter(str.isdigit, dni))
        return dni_normalizado

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'dni',
            'nombre',
            'apellido',
            # Añade otros campos relevantes
        ]
        widgets = {
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'DNI',
                'help_text': 'Ingrese el DNI sin puntos.'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            # Añade otros campos relevantes con sus widgets
        }

class CasoInteresanteForm(forms.ModelForm):
    class Meta:
        model = CasoInteresante
        fields = [
            'id_estudio',
            'fecha',
            'sede',
            'tipo_estudio',
            'contraste_ev',
            'contraste_or',
            'region_anatomica',
            'sistema',
            'organo',
            'especialidad',
            'descripcion',
            'hallazgos',
            'fragmento_informe',
            'etiquetas',
        ]
        widgets = {
            'id_estudio': forms.NumberInput(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_estudio': forms.CheckboxSelectMultiple(),
            'contraste_ev': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contraste_or': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'region_anatomica': forms.Select(attrs={'class': 'form-control'}),
            'sistema': forms.Select(attrs={'class': 'form-control'}),
            'organo': forms.Select(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hallazgos': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'fragmento_informe': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'etiquetas': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control', 'multiple': True}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class ImagenCasoInteresanteForm(forms.ModelForm):
    imagenes = MultipleFileField()

    class Meta:
        model = ImagenCasoInteresante
        fields = ['imagenes']
