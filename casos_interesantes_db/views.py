from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView, View, ListView, DetailView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Paciente, CasoInteresante, ImagenCasoInteresante, MetodoEstudio
from .forms import PacienteSearchForm, PacienteForm, CasoInteresanteForm, ImagenCasoInteresanteForm, CasoInteresanteFilterForm
import cloudinary.uploader

class PacienteSearchView(LoginRequiredMixin, FormView):
    template_name = 'casos_db/paciente_search.html'
    form_class = PacienteSearchForm

    def form_valid(self, form):
        dni = form.cleaned_data['dni']
        try:
            paciente = Paciente.objects.get(dni=dni)
            return redirect('casos_interesantes_db:crear_caso_interesante', paciente_id=paciente.id)
        except Paciente.DoesNotExist:
            return redirect(f'{reverse_lazy("casos_interesantes_db:crear_paciente")}?dni={dni}')


class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'casos_db/paciente_form.html'
    success_url = reverse_lazy('casos_interesantes_db:en_construccion')

    def get_initial(self):
        initial = super().get_initial()
        initial['dni'] = self.request.GET.get('dni', '')
        return initial

    def form_valid(self, form):
        self.object = form.save()
        return redirect('casos_interesantes_db:crear_caso_interesante', paciente_id=self.object.id)

class CasoInteresanteCreateView(LoginRequiredMixin, CreateView):
    model = CasoInteresante
    form_class = CasoInteresanteForm
    template_name = 'casos_db/caso_interesante_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = get_object_or_404(Paciente, id=self.kwargs['paciente_id'])
        context['paciente'] = paciente
        if self.request.POST:
            context['imagen_form'] = ImagenCasoInteresanteForm(self.request.POST, self.request.FILES)
        else:
            context['imagen_form'] = ImagenCasoInteresanteForm()
        return context

    def form_valid(self, form):
        form.instance.usuario_carga = self.request.user  # Asigna el usuario logueado
        form.instance.paciente = get_object_or_404(Paciente, id=self.kwargs['paciente_id'])
        context = self.get_context_data()
        imagen_form = context['imagen_form']
        if imagen_form.is_valid():
            self.object = form.save()
            for imagen in self.request.FILES.getlist('imagenes'):
                # Subir la imagen a Cloudinary
                upload_result = cloudinary.uploader.upload(imagen)
                # Crear la instancia de ImagenCasoInteresante con la URL de Cloudinary
                ImagenCasoInteresante.objects.create(caso=self.object, imagen=upload_result['url'])
            return redirect(reverse('casos_interesantes_db:caso_creado_exito', kwargs={'pk': self.object.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['imagen_form'] = ImagenCasoInteresanteForm(self.request.POST, self.request.FILES)
        return self.render_to_response(context)

class CasoCreadoExitoView(LoginRequiredMixin, View):
    template_name = 'casos_db/caso_creado_exito.html'

    def get(self, request, *args, **kwargs):
        caso = get_object_or_404(CasoInteresante, pk=kwargs['pk'])
        paciente = caso.paciente
        return render(request, self.template_name, {'caso': caso, 'paciente': paciente})

class CasoInteresanteListView(LoginRequiredMixin, ListView):
    model = CasoInteresante
    template_name = 'casos_db/caso_interesante_list.html'
    context_object_name = 'casos'
    paginate_by = 10  # Opcional: para paginar la lista de casos

    def get_queryset(self):
        queryset = CasoInteresante.objects.all().order_by('-fecha')
        form = self.filter_form()
        if form.is_valid():
            if form.cleaned_data['fecha_desde']:
                queryset = queryset.filter(fecha__gte=form.cleaned_data['fecha_desde'])
            if form.cleaned_data['fecha_hasta']:
                queryset = queryset.filter(fecha__lte=form.cleaned_data['fecha_hasta'])
            if form.cleaned_data['patologia']:
                queryset = queryset.filter(hallazgos__icontains=form.cleaned_data['patologia'])
            if form.cleaned_data['organo']:
                queryset = queryset.filter(organo=form.cleaned_data['organo'])
            if form.cleaned_data['region_anatomica']:
                queryset = queryset.filter(region_anatomica=form.cleaned_data['region_anatomica'])
            if form.cleaned_data['sistema']:
                queryset = queryset.filter(sistema=form.cleaned_data['sistema'])
            if form.cleaned_data['especialidad']:
                queryset = queryset.filter(especialidad=form.cleaned_data['especialidad'])
            if form.cleaned_data['etiqueta']:
                queryset = queryset.filter(etiquetas__name__icontains=form.cleaned_data['etiqueta'])
        return queryset

    def filter_form(self):
        return CasoInteresanteFilterForm(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form()
        return context

class CasoInteresanteDetailView(LoginRequiredMixin, DetailView):
    model = CasoInteresante
    template_name = 'casos_db/caso_interesante_detail.html'
    context_object_name = 'caso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        caso = self.get_object()
        estudios_con_contraste = []
        estudios_sin_contraste = []

        for metodo in caso.metodos_estudio.all():
            if metodo.tipo_estudio.nombre == "Tomografía computada":
                if metodo.contraste_ev and metodo.contraste_or:
                    estudios_con_contraste.append("Tomografía computada con contraste oral y endovenoso")
                elif metodo.contraste_ev:
                    estudios_con_contraste.append("Tomografía computada con contraste endovenoso sin contraste oral")
                elif metodo.contraste_or:
                    estudios_con_contraste.append("Tomografía computada sin contraste endovenoso con contraste oral")
                else:
                    estudios_sin_contraste.append("Tomografía computada sin contraste endovenoso ni oral")
            elif metodo.tipo_estudio.nombre == "Resonancia magnética":
                if metodo.contraste_ev:
                    estudios_con_contraste.append("Resonancia magnética con gadolinio")
                else:
                    estudios_sin_contraste.append("Resonancia magnética sin contraste")
            elif metodo.tipo_estudio.nombre in ["Radiografía", "Ecografía"]:
                estudios_sin_contraste.append(metodo.tipo_estudio.nombre)

        def format_estudios(estudios_con_contraste, estudios_sin_contraste):
            estudios = estudios_con_contraste + estudios_sin_contraste
            if len(estudios) > 1:
                return ', '.join(estudios[:-1]) + ' y ' + estudios[-1] + '.'
            elif estudios:
                return estudios[0] + '.'
            else:
                return ''

        context['estudios_formateados'] = format_estudios(estudios_con_contraste, estudios_sin_contraste)
        return context