from ast import Return
import email
from os import curdir
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Usuario

def login(request):
	return render(request, 'index.html')

def iniciarSesion(request):
    email = request.POST['yourEmail']
    contrasenia = request.POST['yourPassword']
    return render(request, 'homeProyecto.html', {'email': email})

def seguridad(request, email):
    return render(request, 'seguridad.html', {'email': email})

def usuario(request, email):
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':email})

def registrarUsuario(request, email):
    print('llega aca??' + email)
    print('llega o no?')
    #codigo = request.POST.get('txtCodigo')
    nombre = request.POST.get('txtNombre')
    email1 = request.POST.get('txtEmail')
    
    usuario = Usuario.objects.create(nombre=nombre, email=email1)
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':email})
    #return render(request, 'usuario.html', {'email':email})
    #return redirect('/usuario/<email>', email)

def eliminarUsuario(request, email, emailAEliminar):
    usuario = Usuario.objects.get(email=emailAEliminar)
    usuario.delete()
    
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':email})