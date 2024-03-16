from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from django.core.files.base import ContentFile
from PIL import Image

def prueba(request):
    return HttpResponse("Hola, mundo.")

# Create your views here.

def generar_qr(request): #genera un qr con la url de la pagina de asistencia
    img = qrcode.make('http://192.168.0.71:8000/asistencia/prueba/') #se pone la url de la pagina de asistencia
    img.save('qr.png') #se guarda el qr en un archivo   
    return HttpResponse("QR generado.") #se muestra un mensaje de que el qr fue generado

