from ast import Return
import email
from os import curdir
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Rol, Usuario
from .models import Permiso
#ASIGNACION
from .models import Rol
from .models import Permiso
from .models import RolesPermisos
from .models import UsuariosRoles
#ASIGNACION

def login(request):
	return render(request, 'index.html')

def iniciarSesion(request):
    email = request.POST['yourEmail']
    contrasenia = request.POST['yourPassword']
    return render(request, 'homeProyecto.html', {'email': email})

def seguridad(request, emailAdmin):
    return render(request, 'seguridad.html', {'email': emailAdmin})

def usuario(request, emailAdmin):
    perPorPatalla = getPermisosPorPantalla(emailAdmin, 'usuario')
    permisosPorPantalla = []
    print('\n')
    for permiso in perPorPatalla:
        print(f'permiso: {permiso.tipo}')
        permisosPorPantalla.append(permiso.tipo)
    print('\n')
    
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla})


def registrarUsuario(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    email = request.POST.get('txtEmail')
    
    usuario = Usuario.objects.create(nombre=nombre, email=email)
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin})


def eliminarUsuario(request, emailAdmin, emailAEliminar):
    usuario = Usuario.objects.get(email=emailAEliminar)
    
    listaUsuariosRoles = []
    listaRoles = []
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    usuariosRoles = UsuariosRoles.objects.all()
    
    #eliminamos todos las asociaciones entre el usuario a eliminar y sus roles
    for usuarioRol in usuariosRoles:
        if usuarioRol.usuario_id == emailAEliminar:
            usuarioRol.delete()
    
    #eliminamos el usuario
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
    #nombreFormulario = request.POST.get('txtFormulario')
    
    '''
    formulario = None
    try:
        #buscamos el formulario para asociar con el permiso
        formulario = Formulario.objects.get(nombre=nombreFormulario.lower())
    except:
        #si no existe creamos el formualario
        formulario = Formulario.objects.create(nombre=nombreFormulario..lower())
    '''
    
    permiso = Permiso.objects.create(nombre=nombre, descripcion=descripcion,
                                     tipo=tipo)
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
    #obtenemos el rol correspondiente
    rol = Rol.objects.get(idRol=idRolAEliminar)
    
    listaRolesPermisos = []
    listaPermisos = []
    
    #tabla intermedia entre Rol y Permiso (relacion M-M)
    rolesPermisos = RolesPermisos.objects.all()
    
    #eliminamos todos las asociaciones entre el rol a eliminar y sus permisos
    for rolPermiso in rolesPermisos:
        if rolPermiso.rol_id == int(idRolAEliminar):
            rolPermiso.delete()
    
    #eliminamos el rol
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
    
    listaRoles = Rol.objects.all()
    return render(request, 'rol.html', {'roles': listaRoles,
                                            'email':emailAdmin})
    


#ASIGNACION
def asignacionRol(request, emailAdmin, emailUsuarioAsignar):
    listaRolesDisponibles = getRolesDisponibles(emailUsuarioAsignar)

    return render(request, 'asignacionRol.html', {
                                    'emailAdmin':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioAsignar,
                                    'roles': listaRolesDisponibles})
#ASIGNACION


def asignarRol(request, emailAdmin, emailUsuarioAsignar, idRol):
    #obtenemos el rol y el permiso
    print('asignando rol a un usuario...')
    usuario = Usuario.objects.get(email=emailUsuarioAsignar)
    rol = Rol.objects.get(idRol=idRol)
    
    #creamos la tabla intermedia la cual almacena los ids de rol y permiso
    usuarioRol = UsuariosRoles.objects.create(usuario=usuario, rol=rol)
    
    listaRolesDisponibles = getRolesDisponibles(emailUsuarioAsignar)
    
    return render(request, 'asignacionRol.html', {
                                    'emailAdmin':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioAsignar,
                                    'roles': listaRolesDisponibles})


def asignacionPermiso(request, emailAdmin, idRolAsignar):
    listaPermisosDisponibles = getPermisosDisponibles(idRolAsignar)
    
    return render(request, 'asignacionPermiso.html', {
                                    'emailAdmin':emailAdmin,
                                    'idRolAsignar': idRolAsignar,
                                    'permisos': listaPermisosDisponibles})
    

def asignarPermiso(request, emailAdmin, idRolAsignar, idPermiso):
    #obtenemos el rol y el permiso
    print('asignando permiso a un rol...')
    rol = Rol.objects.get(idRol=idRolAsignar)
    permiso = Permiso.objects.get(idPermiso=idPermiso)
    
    #creamos la tabla intermedia la cual almacena los ids de rol y permiso
    rolPermiso = RolesPermisos.objects.create(rol=rol, permiso=permiso)
    
    listaPermisosDisponibles = getPermisosDisponibles(idRolAsignar)
    
    return render(request, 'asignacionPermiso.html', {
                                    'emailAdmin':emailAdmin,
                                    'idRolAsignar': idRolAsignar,
                                    'permisos': listaPermisosDisponibles})
    
    
def getPermisosDisponibles(idRolAsignar):
    listaPermisosAsociados = []
    listaPermisos = []
    #tabla intermedia entre Rol y Permiso (relacion M-M)
    rolesPermisos = RolesPermisos.objects.all()
    
    #obtenemos todos los permisos actuales asociados a dicho rol
    for rolPermiso in rolesPermisos:
        if rolPermiso.rol_id == int(idRolAsignar):
            permiso = Permiso.objects.get(idPermiso=rolPermiso.permiso_id)
            listaPermisosAsociados.append(permiso)
    
    #obtenemos todos los permisos
    listaPermisosAux = Permiso.objects.all()
            
    #obtenemos todos los permisos disponibles para ser asignados
    for permiso in listaPermisosAux:
        siEsta = False
        for permisoAsociado in listaPermisosAsociados:
            if permiso.idPermiso == permisoAsociado.idPermiso:
                siEsta = True
                break
            
        if siEsta == False:
            listaPermisos.append(permiso)
        
    return listaPermisos



def getRolesDisponibles(emailUsuarioAsignar):
    '''
    Se obtiene todos los roles disponibles para ese usuario
    '''
    
    listaRolesAsociados = []
    listaRoles = []
    usuariosRoles = []
    
    #tabla intermedia entre Rol y Permiso (relacion M-M)
    try:
        usuariosRoles = UsuariosRoles.objects.all()
    except:
        #en caso de que no hay ningun rol todavia en la BD
        pass
    
    #obtenemos todos los permisos actuales asociados a dicho rol
    for usuarioRol in usuariosRoles:
        if usuarioRol.usuario_id == emailUsuarioAsignar:
            rol = Rol.objects.get(idRol=usuarioRol.rol_id)
            listaRolesAsociados.append(rol)
    
    #obtenemos todos los permisos
    listaRolesAux = []
    try:
        #en caso de que no exista ningun rol
        listaRolesAux = Rol.objects.all()
    except:
        pass
            
    #obtenemos todos los permisos disponibles para ser asignados
    for rol in listaRolesAux:
        siEsta = False
        for rolAsociado in listaRolesAsociados:
            if rol.idRol == rolAsociado.idRol:
                siEsta = True
                break
            
        if siEsta == False:
            listaRoles.append(rol)
        
    return listaRoles



def getPermisosPorPantalla(emailAdmin, nombrePantalla):
    permisos = Permiso.objects.all()
    permisosPorPantalla = []
    permisosAsignados = []
    
    #obtenemos los roles del usuario 
    rolesAsignados = getRolesAsignados(emailAdmin)
    
    #recorremos dichos roles para obtener los permisos
    for rolAsignado in rolesAsignados:
        perAsignados = getPermisosAsignadosARol(rolAsignado.idRol)
        permisosAsignados.extend(perAsignados)
    
    #verificamos que algunos de esos permisos correspondan a la pantalla/formulario
    for permisoAsignado in permisosAsignados:
        if permisoAsignado.descripcion.lower() == nombrePantalla:
            permisosPorPantalla.append(permisoAsignado)

    return permisosPorPantalla

def getPermisosAsignadosARol(idRol):
    permisosAsignados = []
    rolesPermisos = []
    try:
        #tabla intermedia entre Rol y Permiso (relacion M-M)
        rolesPermisos = RolesPermisos.objects.all()
    except:
        pass
    
    #tabla intermedia entre Rol y Permiso (relacion M-M)
    for rolPermiso in rolesPermisos:
        if rolPermiso.rol_id == idRol:
            permiso = Permiso.objects.get(idPermiso=rolPermiso.permiso_id)
            permisosAsignados.append(permiso)
            
    
    return permisosAsignados


def getRolesAsignados(emailAdmin):
    usuariosRoles = []
    rolesAsignados = []
    try:
        #tabla intermedia entre Usuario y Rol (relacion M-M)
        usuariosRoles = UsuariosRoles.objects.all()
    except:
        pass
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    for usuarioRol in usuariosRoles:
        if usuarioRol.usuario_id == emailAdmin:
            rol = Rol.objects.get(idRol=usuarioRol.rol_id)
            rolesAsignados.append(rol)
            
    
    return rolesAsignados