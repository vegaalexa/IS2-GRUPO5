from ast import Return
import email
from os import curdir
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Rol, Usuario
from .models import Permiso

def login(request):
	return render(request, 'index.html')

def iniciarSesion(request):
    email = request.POST['yourEmail']
    contrasenia = request.POST['yourPassword']
    return render(request, 'homeProyecto.html', {'email': email})

def seguridad(request, emailAdmin):
    return render(request, 'seguridad.html', {'email': emailAdmin})

def usuario(request, emailAdmin):
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin})


def registrarUsuario(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    email = request.POST.get('txtEmail')
    
    usuario = Usuario.objects.create(nombre=nombre, email=email)
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin})


def eliminarUsuario(request, emailAdmin, emailAEliminar):
    usuario = Usuario.objects.get(email=emailAEliminar)
    usuario.delete()
    
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin})


def edicionUsuario(request, emailAdmin, emailAEditar):
    usuario = Usuario.objects.get(email=emailAEditar)
    
    return render(request, 'edicionUsuario.html', {'usuario': usuario,
                                            'email':emailAdmin})


def editarUsuario(request, emailAdmin, emailAEditar):
    nombre = request.POST.get('txtNombre')
    email = request.POST.get('txtEmail')
    
    usuario = Usuario.objects.get(email=emailAEditar)
    usuario.nombre = nombre
    usuario.email = email
    usuario.save()
    
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin})
    
    
#********************************************

#Agregamos las vistas para ABM de los permisos

#********************************************
def permiso(request, emailAdmin):
    listaPermisos = Permiso.objects.all()
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin})
    
def registrarPermiso(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    descripcion = request.POST.get('txtDescripcion')
    tipo = request.POST.get('txtTipo')
    
    permiso = Permiso.objects.create(nombre=nombre, descripcion=descripcion,
                                     tipo=tipo, )
    listaPermisos = Permiso.objects.all()
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin})
    
    

def eliminarPermiso(request, emailAdmin, idPermisoAEliminar):
    permiso = Permiso.objects.get(idPermiso=idPermisoAEliminar)
    permiso.delete()
    
    listaPermiso = Permiso.objects.all()
    return render(request, 'permiso.html', {'permisos': listaPermiso,
                                            'email':emailAdmin})
    
    
def edicionPermiso(request, emailAdmin, idPermisoAEditar):
    permiso = Permiso.objects.get(idPermiso=idPermisoAEditar)
    
    return render(request, 'edicionPermiso.html', {'permiso': permiso,
                                            'email':emailAdmin})
    
    
def editarPermiso(request, emailAdmin, idPermisoAEditar):
    nombre = request.POST.get('txtNombre')
    tipo = request.POST.get('txtTipo')
    descripcion = request.POST.get('txtDescripcion')
    
    permiso = Permiso.objects.get(idPermiso=idPermisoAEditar)
    
    permiso.nombre = nombre
    permiso.tipo = tipo
    permiso.descripcion = descripcion
    permiso.save()
    
    listaPermisos = Permiso.objects.all()
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin})

#********************************************

#Vista para ABM de Roles

#********************************************
def rol(request, emailAdmin):
    listaRol = Rol.objects.all()
    return render(request, 'rol.html', {'roles': listaRol,
                                            'email':emailAdmin})
    
def registrarRol(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    descripcion = request.POST.get('txtDescripcion')
    
    rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
    listaRol = Rol.objects.all()
    return render(request, 'rol.html', {'roles': listaRol,
                                            'email':emailAdmin})
    
    

def eliminarRol(request, emailAdmin, idRolAEliminar):
    rol = Rol.objects.get(idRol=idRolAEliminar)
    rol.delete()
    
    listaRol = Rol.objects.all()
    return render(request, 'rol.html', {'roles': listaRol,
                                            'email':emailAdmin})
    
    
def edicionRol(request, emailAdmin, idRolAEditar):
    rol = Rol.objects.get(idRol=idRolAEditar)
    
    return render(request, 'edicionRol.html', {'rol': rol,
                                            'email':emailAdmin})
    
    
def editarRol(request, emailAdmin, idRolAEditar):
    nombre = request.POST.get('txtNombre')
    descripcion = request.POST.get('txtDescripcion')
    
    rol = Rol.objects.get(idRol=idRolAEditar)
    
    rol.nombre = nombre
    rol.descripcion = descripcion
    rol.save()
    
    listaRol = Rol.objects.all()
    return render(request, 'rol.html', {'rol': listaRol,
                                            'email':emailAdmin})
