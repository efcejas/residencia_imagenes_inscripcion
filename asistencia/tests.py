from django.test import TestCase, Client
# from .models import Residente
from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your tests here.

from django.urls import reverse
from .models import Residente, RegistroAsistencia

class TestPasswordReset(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Residente.objects.create_user(username='testuser', password='12345', email='testuser@example.com', dni='12345678', first_name='Test', last_name='User', fecha_nacimiento=date.today(), matricula='123456', telefono='1234567890', fecha_de_ingreso=date.today())
        self.user.save()

    def test_password_reset_form(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')

    def test_password_reset_done(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')

    def test_password_reset_confirm(self):
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64': 'NA', 'token': 'set-password'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_confirm.html')

    def test_password_reset_complete(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_complete.html')

class RegisterResidenteViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_registration(self):
        new_user_data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('register'), new_user_data)
        self.assertEqual(response.status_code, 302)  # Redirection after successful post
        users = Residente.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'newuser')

class RegisterResidenteViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_registration(self):
        new_user_data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'newuser@example.com',
            'dni': '12345678',
            'first_name': 'New',
            'last_name': 'User',
            'fecha_nacimiento': date(1990, 1, 1),
            'matricula': '123456',
            'telefono': '1234567890',
            'fecha_de_ingreso': date(2022, 1, 1),
        }
        response = self.client.post(reverse('register'), new_user_data)
        self.assertEqual(response.status_code, 302)  # Redirection after successful post
        users = Residente.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'newuser')
