from django import forms
from .models import Residente, Pregunta, Respuesta

# Formulario de datos personales con validación y limpieza de datos
class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['nombre', 'apellido', 'dni', 'anio_residencia']
    
    def __init__(self, *args, **kwargs):
        super(DatosPersonalesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                # 'placeholder': field.label
            })
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        return nombre.title()  # Convierte a mayúscula la primera letra de cada palabra

    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        return apellido.title()  # Convierte a mayúscula la primera letra de cada palabra
    
    def clean_dni(self):
        dni = self.cleaned_data['dni']
        return ''.join(filter(str.isdigit, dni))  # Elimina todos los caracteres que no sean números

# Formulario del examen con preguntas estilizadas en Bootstrap
class ExamenForm(forms.Form):
    # Generar un campo para cada pregunta existente
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for pregunta in Pregunta.objects.all():
            self.fields[f"pregunta_{pregunta.id}"] = forms.CharField(
                label=pregunta.texto,
                widget=forms.Textarea(attrs={
                    'class': 'form-control mb-3',
                    'rows': 3,
                    'placeholder': pregunta.texto_ayuda
                })
            )

    # Método para guardar las respuestas
    def save(self, examen_respuesta):
        for key, value in self.cleaned_data.items():
            pregunta_id = int(key.split('_')[1])
            pregunta = Pregunta.objects.get(id=pregunta_id)
            Respuesta.objects.create(
                examen_respuesta=examen_respuesta,
                pregunta=pregunta,
                texto=value
            )