# Django imports
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import CharField, Value as V
from django.db.models.functions import Concat, TruncMonth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from datetime import datetime

# Librerías de terceros
import qrcode
from django.db.models import Q, Max # Para hacer consultas más complejas

# Local imports
from .forms import (RegistroAsistenciaForm, RegistroFormAdministrativo,
                    RegistroFormDocente, RegistroFormResidente, RegistroFormUsuario, SedeForm, WashoutSuprarrenalForm, EvaluacionPeriodicaForm)
from .models import RegistroAsistencia, Residente, Usuario, Sedes, Docente, Administrativo, GruposResidentes, EvaluacionPeriodica

# Vistas relacionadas con el registro, login y logout de usuarios, además de la autenticación.abs

class RegistroView(CreateView):
    template_name = 'registration/register.html'
    # Redirige a la página de registro exitoso
    success_url = reverse_lazy('registro_exitoso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_usuario = self.kwargs.get('tipo_usuario')
        context['user_form'] = RegistroFormUsuario(self.request.POST or None)
        # Pasamos el tipo de usuario al contexto
        context['tipo_usuario'] = tipo_usuario
        return context

    def get_form_class(self):
        tipo_usuario = self.kwargs.get('tipo_usuario')
        if tipo_usuario == 'residente':
            return RegistroFormResidente
        elif tipo_usuario == 'docente':
            return RegistroFormDocente
        else:  # asumimos que el usuario es Administrativo
            return RegistroFormAdministrativo

    def form_valid(self, form):
        tipo_usuario = self.kwargs.get('tipo_usuario')
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        # El formulario no es válido, vuelve a renderizar la página de registro con el formulario y los errores de validación
        return self.render_to_response(self.get_context_data(form=form))

class SuccessView(TemplateView):
    template_name = 'registration/success.html'

# Vistas relacionadas con los perfiles de usuario

class PerfilView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email']  # Ajusta los campos según tus necesidades
    template_name = 'presentes/perfil.html'
    success_url = reverse_lazy('asistencia:perfil')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()

        if hasattr(user, 'residente_profile'):
            context['form_residente'] = RegistroFormResidente(instance=user.residente_profile)
        elif hasattr(user, 'docente_profile'):
            context['form_docente'] = RegistroFormDocente(instance=user.docente_profile)
        elif hasattr(user, 'administrativo_profile'):
            context['form_administrativo'] = RegistroFormAdministrativo(instance=user.administrativo_profile)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
    
        if form.has_changed():
            if form.is_valid():
                form.save()
                messages.success(request, 'Tus datos se han actualizado correctamente.')
                request.session['data_changed'] = True
            else:
                messages.error(request, 'Hubo un error al actualizar tus datos.')
                request.session['data_changed'] = False
        # ...
        user = self.get_object()

        if hasattr(user, 'residente_profile'):
            form_residente = RegistroFormResidente(request.POST, instance=user.residente_profile)
            if form_residente.is_valid():
                form_residente.save()
            else:
                messages.error(request, 'Hubo un error al actualizar el perfil de residente.')
        elif hasattr(user, 'docente_profile'):
            form_docente = RegistroFormDocente(request.POST, instance=user.docente_profile)
            if form_docente.is_valid():
                form_docente.save()
            else:
                messages.error(request, 'Hubo un error al actualizar el perfil de docente.')
        elif hasattr(user, 'administrativo_profile'):
            form_administrativo = RegistroFormAdministrativo(request.POST, instance=user.administrativo_profile)
            if form_administrativo.is_valid():
                form_administrativo.save()
            else:
                messages.error(request, 'Hubo un error al actualizar el perfil de administrativo.')

        return super().form_valid(form)

# Vistas relacionadas con la página de asistencia.

class RegistroAsistenciaView(LoginRequiredMixin, View):
    def get(self, request):
        form = RegistroAsistenciaForm()
        return render(request, 'presentes/registro_asistencia.html', {'form': form})

    def post(self, request):
        # Verificar si el usuario tiene un perfil de residente asociado
        if hasattr(request.user, 'residente_profile'):
            # El usuario tiene un perfil de residente asociado
            form = RegistroAsistenciaForm(request.POST)
            if form.is_valid():
                ahora = timezone.localtime()

                residente = request.user.residente_profile
                ya_registrado_hoy = RegistroAsistencia.objects.filter(
                    residente=residente, fecha=ahora.date()).exists()

                if ya_registrado_hoy:
                    error_message = '¡{}, ya has registrado tu asistencia hoy!'.format(
                        request.user.first_name)
                    return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

                latitud = form.cleaned_data.get('latitud')
                longitud = form.cleaned_data.get('longitud')

                # Coordenadas de la sede pichincha de Investigaciones Médicas.
                latitud_permitida1 = -34.61068
                longitud_permitida1 = -58.39927

                # Coordenadas de la sede Junín de Diagnóstico Médico.
                latitud_permitida2 = -34.59685  # Reemplaza estos valores con las coordenadas reales
                longitud_permitida2 = -58.39732  # Reemplaza estos valores con las coordenadas reales

                rango_permitido = 0.0005

                # Verificar si el usuario está dentro del rango permitido de alguna de las ubicaciones permitidas
                if not ((latitud_permitida1 - rango_permitido <= latitud <= latitud_permitida1 + rango_permitido and
                        longitud_permitida1 - rango_permitido <= longitud <= longitud_permitida1 + rango_permitido) or
                        (latitud_permitida2 - rango_permitido <= latitud <= latitud_permitida2 + rango_permitido and
                        longitud_permitida2 - rango_permitido <= longitud <= longitud_permitida2 + rango_permitido)):
                    error_message = '¡{}, debes estar dentro del rango permitido para registrar tu asistencia!'.format(
                        request.user.first_name)
                    return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

                hora_inicio_entrada = ahora.replace(hour=6, minute=30, second=0)
                hora_fin_entrada = ahora.replace(hour=7, minute=0, second=0)
                hora_inicio_clase = ahora.replace(hour=7, minute=0, second=0)
                hora_fin_clase = ahora.replace(hour=8, minute=0, second=0)

                if not (hora_inicio_entrada <= ahora <= hora_fin_entrada) and not (hora_inicio_clase <= ahora <= hora_fin_clase):
                    error_message = '¡{}, no es posible registrar asistencias fuera del horario permitido!'.format(
                        request.user.first_name)
                    return render(request, 'presentes/registro_asistencia.html', {'form': form, 'error_message': error_message, 'error_url': reverse('asistencia:asistencias_registradas')})

                if hora_fin_entrada < ahora <= hora_fin_clase:
                    llegada_tarde = True
                    llegada_a_tiempo = False
                else:
                    llegada_a_tiempo = hora_inicio_entrada <= ahora <= hora_fin_entrada
                    llegada_tarde = ahora > hora_fin_entrada

                registro_asistencia = form.save(commit=False)
                registro_asistencia.residente = residente
                registro_asistencia.fecha = ahora.date()
                registro_asistencia.hora = ahora.time()
                registro_asistencia.llegada_a_tiempo = llegada_a_tiempo
                registro_asistencia.llegada_tarde = llegada_tarde
                registro_asistencia.save()

                if llegada_tarde:
                    messages.error(request, '¡{}, registraste tu asistencia con tardanza!'.format(
                        request.user.first_name))
                else:
                    messages.success(request, '¡{}, registraste tu asistencia exitosamente!'.format(
                        request.user.first_name))

                return redirect('asistencia:asistencias_registradas')

            return render(request, 'presentes/registro_asistencia.html', {'form': form})

        # Si el usuario no tiene un perfil de residente asociado, maneja este caso según sea necesario
        else:
            error_message = 'Para acceder a esta funcionalidad, primero debes tener un perfil de residente asociado. Comunícate con el administrador del sistema.'
            request.session['error_message'] = error_message
            return redirect('asistencia:error_sin_perfil_residente')

class ListaAsistenciaView(LoginRequiredMixin, TemplateView):
    template_name = 'presentes/lista_asistencias_registradas.html'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'residente_profile'):
            return redirect('asistencia:error_sin_perfil_residente')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene el perfil asociado al usuario actual
        perfil_usuario = self.request.user.residente_profile
        # Obtiene todos los registros de asistencia del residente asociado
        context['attendance_records'] = RegistroAsistencia.objects.filter(
            residente=perfil_usuario).order_by('-fecha', '-hora')
        return context

# Vista para mostrar los registros de asistencia de un residente o de todos los residentes

class RegistroAsistenciaFiltradoListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RegistroAsistencia
    template_name = 'presentes/lista_control_asistencia.html'
    context_object_name = 'control_asistencia'

    def get_queryset(self):
        # Obtiene el queryset base
        queryset = RegistroAsistencia.objects.all()

        # Filtra por día si se proporciona el parámetro 'dia'
        dia = self.request.GET.get('dia')
        if dia:
            queryset = queryset.filter(fecha=dia)
        else:
            # Si no se proporciona un parámetro 'dia', muestra los registros del día más reciente
            fecha_mas_reciente = queryset.aggregate(Max('fecha'))['fecha__max']
            if fecha_mas_reciente:
                queryset = queryset.filter(fecha=fecha_mas_reciente)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtiene el queryset base
        queryset = RegistroAsistencia.objects.all()

        # Filtra por día si se proporciona el parámetro 'dia'
        dia = self.request.GET.get('dia')
        if dia:
            dia = datetime.strptime(dia, "%Y-%m-%d").date()  # Convierte el string a fecha
            queryset = queryset.filter(fecha=dia)
        else:
            # Si no se proporciona un parámetro 'dia', muestra los registros del día más reciente
            fecha_mas_reciente = queryset.aggregate(Max('fecha'))['fecha__max']
            if fecha_mas_reciente:
                queryset = queryset.filter(fecha=fecha_mas_reciente)
                dia = fecha_mas_reciente  # Usa la fecha más reciente

        context['control_asistencia'] = queryset
        context['dia'] = dia  # Añade la fecha al contexto
        return context

    def test_func(self):
        return hasattr(self.request.user, 'docente_profile') or hasattr(self.request.user, 'administrativo_profile') or self.request.user.is_superuser

    def handle_no_permission(self):
        # redirige a la página de inicio o a una página de error si el usuario no tiene permiso
        return redirect('home')

# Vistas relacionadas con la evaluación periódica

class EvaluacionPeriodicaCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = EvaluacionPeriodica
    form_class = EvaluacionPeriodicaForm
    template_name = 'presentes/evaluacion_periodica_form.html'
    success_url = reverse_lazy('home')
    success_message = '¡La evaluación periódica se ha creado exitosamente!'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.method == 'POST':
            return render(self.request, self.template_name, {'form': form})
        return response

    def form_valid(self, form):
        form.instance.evaluador = self.request.user  # Asigna el usuario actual como evaluador
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'docente_profile') or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')

# Vistas relacionadas con la gestión de usuarios residentes

class ResidentesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Residente
    template_name = 'presentes/residentes_list.html'
    context_object_name = 'residentes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_residentes'] = Residente.objects.count()
        return context

    def test_func(self):
        # Agregué perfil docente y superuser.
        return hasattr(self.request.user, 'administrativo_profile') or hasattr(self.request.user, 'docente_profile') or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')

# Vistas relacionadas con la gestion de sedes

class SedesCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Sedes
    form_class = SedeForm
    template_name = 'presentes/sede_form.html'
    success_url = reverse_lazy('asistencia:sedes_list')
    success_message = '¡La sede se ha creado exitosamente!'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.method == 'POST':
            return render(self.request, self.template_name, {'form': form})
        return response

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile')

    def handle_no_permission(self):
        return redirect('home')

class SedesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Sedes
    template_name = 'presentes/sedes_list.html'
    context_object_name = 'sedes'

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile') or self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')

class SedeUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Sedes
    fields = ['nombre_sede', 'direccion', 'telefono', 'referente']
    template_name = 'presentes/sede_form.html'
    success_url = reverse_lazy('asistencia:sedes_list')
    success_message = '¡La sede se ha actualizado exitosamente!'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.method == 'POST':
            return render(self.request, self.template_name, {'form': form})
        return response

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile')

    def handle_no_permission(self):
        return redirect('home')

class SedeDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Sedes
    template_name = 'presentes/sede_confirm_delete.html'
    success_url = reverse_lazy('asistencia:sedes_list')
    success_message = '¡La sede se ha eliminado exitosamente!'

    def test_func(self):
        return hasattr(self.request.user, 'administrativo_profile')

    def handle_no_permission(self):
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sede'] = self.object
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Vistas relacionadas con herramientas útiles para los residentes

class CalcularWashoutView(View):
    template_name = 'presentes/calculo_lavado_suprarrenal.html'

    def get(self, request):
        form = WashoutSuprarrenalForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = WashoutSuprarrenalForm(request.POST)
        if form.is_valid():
            HU_sin_contraste = form.cleaned_data['HU_sin_contraste']
            HU_contraste_minuto = form.cleaned_data['HU_contraste_minuto']
            HU_contraste_retraso = form.cleaned_data['HU_contraste_retraso']

            # Calcula el lavado absoluto si HU_sin_contraste es proporcionado
            if HU_sin_contraste is not None:
                lavado_absoluto = ((HU_contraste_minuto - HU_contraste_retraso) / (HU_contraste_minuto - HU_sin_contraste)) * 100
            else:
                lavado_absoluto = None

            # Calcula el lavado relativo usando las fórmulas de washout suprarrenal
            lavado_relativo = (HU_contraste_minuto - HU_contraste_retraso) / HU_contraste_minuto * 100

            # Determina si la lesión es altamente sugestiva de adenoma
            if lavado_absoluto is not None and lavado_absoluto >= 60 and lavado_relativo >= 40:
                es_adenoma = True
            else:
                es_adenoma = False

            return render(request, self.template_name, {
                'form': form,
                'lavado_absoluto': lavado_absoluto,
                'lavado_relativo': lavado_relativo,
                'es_adenoma': es_adenoma,
            })
        else:
            # Si el formulario no es válido, simplemente renderiza el template con el formulario que contiene los errores
            return render(request, self.template_name, {'form': form})

# Create your views here.

def generar_qr(request):  # genera un qr con la url de la pagina de asistencia
    # se pone la url de la pagina de asistencia
    img = qrcode.make(
        'https://residentes-dm-9833103dde7d.herokuapp.com/asistencia/registro_asistencia/')
    img.save('qr.png')  # se guarda el qr en un archivo
    # se muestra un mensaje de que el qr fue generado
    return HttpResponse("QR generado.")
