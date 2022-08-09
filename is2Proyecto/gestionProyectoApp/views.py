from ast import Return
from os import curdir
from django.shortcuts import redirect, render
from django.http import HttpResponse


def login(request):
	return render(request, 'index.html')

def iniciarSesion(request):
    email = request.POST['yourEmail']
    contrasenia = request.POST['yourPassword']
    return render(request, 'homeProyecto.html', {'email': email})