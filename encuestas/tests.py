from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Pregunta
import datetime

class PreguntaModelTests(TestCase):
    def test_publicacion_reciente_con_pregunta_futura(self):
        """
        publicacion_reciente() devuelve False para preguntas cuya fecha de publicación
        es en el futuro.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        pregunta_futura = Pregunta(fecha_publicacion=time)
        self.assertIs(pregunta_futura.fue_publicada_recientemente(), False)

    def test_publicacion_reciente_con_pregunta_antigua(self):
        """
        publicacion_reciente() devuelve False para preguntas cuya fecha de publicación
        es mayor a un día.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pregunta_antigua = Pregunta(fecha_publicacion=time)
        self.assertIs(pregunta_antigua.fue_publicada_recientemente(), False)

    def test_publicacion_reciente_con_pregunta_reciente(self):
        """
        publicacion_reciente() devuelve True para preguntas cuya fecha de publicación
        es menor a un día.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pregunta_reciente = Pregunta(fecha_publicacion=time)
        self.assertIs(pregunta_reciente.fue_publicada_recientemente(), True)
        
def crear_pregunta(pregunta_texto, dias):
    """
    Crea una pregunta con el `texto` dado y publicada el número de `dias` de diferencia
    con respecto a la fecha actual (positivo para preguntas en el pasado, negativo para
    preguntas en el futuro).
    """
    time = timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.objects.create(pregunta_texto=pregunta_texto, fecha_publicacion=time)

class PreguntaIndexViewTests(TestCase):
    def test_sin_preguntas(self):
        """
        Si no existen preguntas, se muestra un mensaje apropiado.
        """
        response = self.client.get(reverse("encuestas:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay preguntas disponibles.")
        self.assertQuerysetEqual(response.context["ultima_pregunta_lista"], [])

    def test_preguntas_pasadas(self):
        """
        Las preguntas con fecha de publicación en el pasado se muestran en la página de índice.
        """
        pregunta = crear_pregunta(pregunta_texto="Pregunta pasada.", dias=-30)
        response = self.client.get(reverse("encuestas:index"))
        self.assertQuerysetEqual(
            response.context["ultima_pregunta_lista"],
            [pregunta]
        )

    def test_preguntas_futuras(self):
        """
        Las preguntas con fecha de publicación en el futuro no se muestran en la página de índice.
        """
        crear_pregunta(pregunta_texto="Pregunta futura.", dias=30)
        response = self.client.get(reverse("encuestas:index"))
        self.assertContains(response, "No hay preguntas disponibles.")
        self.assertQuerysetEqual(response.context["ultima_pregunta_lista"], [])

    def test_preguntas_pasadas_y_futuras(self):
        """
        Incluso si existen preguntas pasadas y futuras, solo se muestran las preguntas pasadas.
        """
        pregunta = crear_pregunta(pregunta_texto="Pregunta pasada.", dias=-30)
        crear_pregunta(pregunta_texto="Pregunta futura.", dias=30)
        response = self.client.get(reverse("encuestas:index"))
        self.assertQuerysetEqual(
            response.context["ultima_pregunta_lista"],
            [pregunta]
        )

    def test_dos_preguntas_pasadas(self):
        """
        La página de índice puede mostrar múltiples preguntas.
        """
        pregunta1 = crear_pregunta(pregunta_texto="Pregunta pasada 1.", dias=-30)
        pregunta2 = crear_pregunta(pregunta_texto="Pregunta pasada 2.", dias=-5)
        response = self.client.get(reverse("encuestas:index"))
        self.assertQuerysetEqual(
            response.context["ultima_pregunta_lista"],
            [pregunta2, pregunta1]
        )

class PreguntaDetailViewTests(TestCase):
    def test_pregunta_futura(self):
        """
        La vista de detalle de una pregunta con fecha de publicación en el futuro devuelve un error 404.
        """
        pregunta_futura = crear_pregunta(pregunta_texto="Pregunta futura.", dias=5)
        url = reverse("encuestas:detalle", args=(pregunta_futura.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_pregunta_pasada(self):
        """
        La vista de detalle de una pregunta con fecha de publicación en el pasado muestra el texto de la pregunta.
        """
        pregunta_pasada = crear_pregunta(pregunta_texto="Pregunta pasada.", dias=-5)
        url = reverse("encuestas:detalle", args=(pregunta_pasada.id,))
        response = self.client.get(url)
        self.assertContains(response, pregunta_pasada.pregunta_texto)