from ast import Return
import datetime
from email.policy import default
from time import sleep
import email
import threading
from os import curdir
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import BackLog, Formulario, Rol, Usuario
from .models import Permiso
from .models import Proyecto
#ASIGNACION
from .models import Rol
from .models import Permiso
from .models import RolesPermisos
from .models import UsuariosRoles
from .models import SprintBackLog
from .models import UsuariosProyectos
from .models import UserStory
from .models import Sprint
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import Http404
from datetime import timedelta

estado = False
#ASIGNACION

def login(request):
	return render(request, 'index.html')

def iniciarSesion(request):
    '''
        Solo el admin o los usuarios registrados pueden acceder
    '''
    email = request.POST['yourEmail']
    contrasenia = request.POST['yourPassword']
    
    emailArrobaIndice = email.index('@')
    #extraemos el contenido antes del @
    emailAux = email[:emailArrobaIndice]
    
    try:
        if emailAux.lower() != 'admin':
            usuario = Usuario.objects.get(email=email)
    except:
        return render(request, 'index.html', {'mensaje': 'Ponga las credenciales correctas'})
    
    return render(request, 'homeProyecto.html', {'email': email})

def iniciarSesion2(request, emailAdmin):
    #es llamado desde el navbar
    return render(request, 'homeProyecto.html', {'email': emailAdmin})


def seguridad(request, emailAdmin):
    return render(request, 'seguridad.html', {'email': emailAdmin})

def siEsAdmin(emailAdmin):
    indice = emailAdmin.index('@') #obtenemos la posición del carácter @
    admin = emailAdmin[:indice]
    
    return admin == 'admin'

def usuario(request, emailAdmin):
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'usuario')
    print(f'permisosPorPantalla: {permisosPorPantalla}')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Usuario'})


def registrarUsuario(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    email = request.POST.get('txtEmail')
    
    usuario = Usuario.objects.create(nombre=nombre, email=email)
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'usuario')
    print(f'permisosPorPantalla: {permisosPorPantalla}')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Usuario'})


def eliminarUsuario(request, emailAdmin, emailAEliminar):
    usuario = Usuario.objects.get(email=emailAEliminar)
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    usuariosRoles = UsuariosRoles.objects.all()
    
    #eliminamos todos las asociaciones entre el usuario a eliminar y sus roles
    for usuarioRol in usuariosRoles:
        if usuarioRol.usuario_id == emailAEliminar:
            usuarioRol.delete()
    
    
    usuariosProyectos = UsuariosProyectos.objects.all()
    #eliminamos todos las asociaciones entre el usuario a eliminar y sus roles
    for usuarioProyecto in usuariosProyectos:
        if usuarioProyecto.usuario_id == emailAEliminar:
            usuarioProyecto.delete()
    
    #eliminamos el usuario
    usuario.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'usuario')
    print(f'permisosPorPantalla: {permisosPorPantalla}')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Usuario'})


def edicionUsuario(request, emailAdmin, emailAEditar):
    usuario = Usuario.objects.get(email=emailAEditar)
    
    return render(request, 'edicionUsuario.html', {'usuario': usuario,
                                            'email':emailAdmin})


def editarUsuario(request, emailAdmin, emailAEditar):
    nombre = request.POST.get('txtNombre')
    email = request.POST.get('txtEmail')
    
    usuario = Usuario.objects.get(email=emailAEditar)
    usuario.nombre = nombre
    
    if usuario.email == email:
        print('son iguales')
        usuario.email = email
        usuario.save()
    else:
        print('son diferentes')
        usuario_temp = Usuario.objects.create(nombre=nombre, email=email)
        
        actualizarProyectoUsuario(usuario.email, usuario_temp)
        actualizarRolesUsuario(usuario.email, usuario_temp)
        actualizarUserStoryUsuario(usuario.email, usuario_temp)
        
        usuario.delete()
    
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin})
    
    
def actualizarProyectoUsuario(email, usuario_temp):
    proyectos_query = UsuariosProyectos.objects.filter(usuario_id = email)
    for p in proyectos_query:
        p.usuario = usuario_temp
        p.save()

def actualizarRolesUsuario(email, usuario_temp):
    roles_query = UsuariosRoles.objects.filter(usuario_id = email)
    for r in roles_query:
        r.usuario = usuario_temp
        r.save()
        
def actualizarUserStoryUsuario(email, usuario_temp):
    us_query = UserStory.objects.filter(usuario_id = email)
    for us in us_query:
        us.usuario = usuario_temp
        us.save()
#********************************************

#Agregamos las vistas para ABM de los permisos

#********************************************

def permiso(request, emailAdmin):
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'permiso')
        
    listaPermisos = Permiso.objects.all().order_by('idPermiso')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None

    formularios = ['Usuario', 'Permiso', 'Rol', 'Proyecto', 'BackLog', 'SprintBackLog', 'UserStory']
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Permiso',
                                        'formularios': formularios})
    
    
def registrarPermiso(request, emailAdmin, formulario):
    nombre = request.POST.get('txtNombre')
    descripcion = request.POST.get('txtDescripcion')
    tipo = request.POST.get('txtTipo')
    #nombreFormulario = request.POST.get('txtFormulario')
    #print(f'formulario: {formulario}')
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
                                     tipo=tipo, formulario=formulario)

    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'permiso')
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaPermisos = Permiso.objects.all().order_by('idPermiso')

    formularios = ['Usuario', 'Permiso', 'Rol', 'Proyecto', 'BackLog', 'SprintBackLog', 'UserStory']
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Permiso',
                                        'formularios': formularios})
    
    

def eliminarPermiso(request, emailAdmin, idPermisoAEliminar):
    rolesPermisos = []
    try:
        rolesPermisos = RolesPermisos.objects.all()
    except:
        pass
    
    #eliminamos todos las asociaciones entre el rol a eliminar y sus permisos
    for rolPermiso in rolesPermisos:
        if int(rolPermiso.permiso_id) == int(idPermisoAEliminar):
            rolPermiso.delete()
    
    permiso = Permiso.objects.get(idPermiso=idPermisoAEliminar)
    permiso.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'permiso')
    listaPermisos = Permiso.objects.all().order_by('idPermiso')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None

    formularios = ['Usuario', 'Permiso', 'Rol', 'Proyecto', 'BackLog', 'SprintBackLog', 'UserStory']
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Permiso',
                                        'formularios': formularios})
    
    
def edicionPermiso(request, emailAdmin, idPermisoAEditar):
    permiso = Permiso.objects.get(idPermiso=idPermisoAEditar)
    formularios = ['Usuario', 'Permiso', 'Rol', 'Proyecto', 'BackLog', 'SprintBackLog', 'UserStory']
    
    return render(request, 'edicionPermiso.html', {'permiso': permiso,
                                            'formularios': formularios,
                                            'email':emailAdmin})
    
    
def editarPermiso(request, emailAdmin, idPermisoAEditar, formulario):
    nombre = request.POST.get('txtNombre')
    tipo = request.POST.get('txtTipo')
    descripcion = request.POST.get('txtDescripcion')
    
    permiso = Permiso.objects.get(idPermiso=idPermisoAEditar)
    
    permiso.nombre = nombre
    permiso.tipo = tipo
    permiso.descripcion = descripcion
    permiso.formulario = formulario
    permiso.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'permiso')
    listaPermisos = Permiso.objects.all().order_by('idPermiso')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None

    formularios = ['Usuario', 'Permiso', 'Rol', 'Proyecto', 'BackLog', 'SprintBackLog', 'UserStory']
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Permiso',
                                        'formularios': formularios})

#********************************************

#Vista para ABM de Roles

#********************************************
def rol(request, emailAdmin):        
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'rol')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaRol = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRol,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'Rol'})
    
    
def registrarRol(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    descripcion = request.POST.get('txtDescripcion')
    
    rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'rol')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaRol = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRol,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'Rol'})
    
    

def eliminarRol(request, emailAdmin, idRolAEliminar):
    #obtenemos el rol correspondiente
    rol = Rol.objects.get(idRol=idRolAEliminar)
    
    #tabla intermedia entre Rol y Permiso (relacion M-M)
    rolesPermisos = []
    try:
        rolesPermisos = RolesPermisos.objects.all()
    except:
        pass
    
    #eliminamos todos las asociaciones entre el rol a eliminar y sus permisos
    for rolPermiso in rolesPermisos:
        if int(rolPermiso.rol_id) == int(idRolAEliminar):
            rolPermiso.delete()
    
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    usuariosRoles = []
    try:
        usuariosRoles = UsuariosRoles.objects.all()
    except:
        pass
    
    #eliminamos todos las asociaciones entre el rol a eliminar y sus permisos
    for usuarioRol in usuariosRoles:
        if int(usuarioRol.rol_id) == int(idRolAEliminar):
            usuarioRol.delete()
    
    
    #eliminamos el rol
    rol.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'rol')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaRol = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRol,
                                            'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'Rol'})
    
    
def edicionRol(request, emailAdmin, idRolAEditar):
    rol = Rol.objects.get(idRol=idRolAEditar)
    
    return render(request, 'edicionRol.html', {'rol': rol,
                                            'email':emailAdmin})
    
    
def editarRol(request, emailAdmin, idRolAEditar):
    nombre = request.POST.get('txtNombreRol')
    descripcion = request.POST.get('txtDescripcionRol')
    
    rol = Rol.objects.get(idRol=idRolAEditar)
    
    rol.nombre = nombre
    rol.descripcion = descripcion
    rol.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'rol')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaRoles = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRoles,
                                            'email':emailAdmin,
                                            'permisosPorPantalla':permisosPorPantalla,
                                            'nombrePantalla': 'Rol'})


def verRolesAsignados(request, emailAdmin, emailUsuario):
    rolesAsignados = getRolesAsignados(emailUsuario)

    
    dic = {}
    dicRolesPermisos = {}
    
    for rolAsignado in rolesAsignados:
        #print(rolAsignado)
        permisosAsignadosARol = getPermisosAsignadosARol(rolAsignado.idRol)
        #ordenamsos la lista
        permisosAsignadosARol.sort(key=lambda permisosAsignadosARol: permisosAsignadosARol.descripcion)
        
        if len(permisosAsignadosARol) == 0:
            print('Error: este rol no tiene ningun permiso asociado')
            dic_temp = {}
            dic_temp[''] = 'Este rol no tiene permisos asignados'
            dicRolesPermisos[rolAsignado] = dic_temp
            continue
        
        p_aux = permisosAsignadosARol[0]
        permisosTipos = ''
        dic = {}
        
        print(f'ROL: {rolAsignado}')
        for p in permisosAsignadosARol:
            if str(p.formulario) != str(p_aux.formulario):
                dic[str(p_aux.formulario)] = permisosTipos
                p_aux = p
                permisosTipos = ''
                
            permisosTipos = permisosTipos + p.tipo + ' '

        dic[str(p_aux.formulario)] = permisosTipos
        dicRolesPermisos[rolAsignado] = dic
       
    print('--------------')
    for clave in dicRolesPermisos.keys(): 
        print('****************')
        for clave1 in dicRolesPermisos[clave].keys():
           print(f'{clave} {clave1} {dicRolesPermisos[clave][clave1]}')
    
    return render(request, 'rolesAsignados.html', {
                                    'email':emailAdmin,
                                    'emailUsuario': emailUsuario,
                                    'roles': rolesAsignados,
                                    'rolesPermisos':dicRolesPermisos})


def verPermisosAsignados(request, emailAdmin, idRol):
    rol = Rol.objects.get(idRol=idRol)
    permisosAsignados = getPermisosAsignadosARol(idRol)
    permisosAsignados.sort(key=lambda permisosAsignados: permisosAsignados.descripcion)
    
    return render(request, 'permisosAsignados.html', {
                                    'email':emailAdmin,
                                    'rol': rol,
                                    'permisos':permisosAsignados})
    

def desasignarPermiso(request, emailAdmin, idRolAsignar, idPermiso):
    rol = Rol.objects.get(idRol=idRolAsignar)
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    rolesPermisos = RolesPermisos.objects.all()

    #eliminamos todos las asociaciones entre el usuario a eliminar y sus roles
    for rolPermiso in rolesPermisos:
        #lo convierto a int ya que por alguna razon me daba error
        #a pasar de que ambos son int 
        if int(rolPermiso.rol_id) == int(idRolAsignar):
            if int(rolPermiso.permiso_id) == int(idPermiso):
                print('quitando permiso...')
                rolPermiso.delete()
            
    permisosAsignados = getPermisosAsignadosARol(idRolAsignar)
    permisosAsignados.sort(key=lambda permisosAsignados: permisosAsignados.descripcion)
    
    return render(request, 'permisosAsignados.html', {
                                    'email':emailAdmin,
                                    'rol': rol,
                                    'permisos':permisosAsignados})
    
        
def desasignacionRol(request, emailAdmin, emailUsuarioQuitar):
    print('desasignando...')
    
    rolesAsignados = getRolesAsignados(emailUsuarioQuitar)

    return render(request, 'desasignacionRol.html', {
                                    'email':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioQuitar,
                                    'roles': rolesAsignados})
#ASIGNACION
def asignacionRol(request, emailAdmin, emailUsuarioAsignar):
    listaRolesDisponibles = getRolesDisponibles(emailUsuarioAsignar)

    return render(request, 'asignacionRol.html', {
                                    'email':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioAsignar,
                                    'roles': listaRolesDisponibles})
#ASIGNACION


def desasignarRol(request, emailAdmin, emailUsuarioQuitar, idRol):
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    usuariosRoles = UsuariosRoles.objects.all()

    #eliminamos todos las asociaciones entre el usuario a eliminar y sus roles
    for usuarioRol in usuariosRoles:
        #lo convierto a int ya que por alguna razon me daba error
        #a pasar de que ambos son int 
        if int(usuarioRol.rol_id) == int(idRol):
            print('quitando rol...')
            usuarioRol.delete()
            
    rolesAsignados = getRolesAsignados(emailUsuarioQuitar)
    
    return render(request, 'desasignacionRol.html', {
                                    'email':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioQuitar,
                                    'roles': rolesAsignados})


def asignarRol(request, emailAdmin, emailUsuarioAsignar, idRol):
    fechaDesde = parse_date(request.POST.get('txtFechaDesde'))
    fechaHasta = parse_date(request.POST.get('txtFechaHasta'))
    
    #obtenemos el rol y el permiso
    esValida = validarFechaRol(emailUsuarioAsignar, idRol, fechaDesde, fechaHasta)
    
    mensaje = None
    if esValida[0]:
        print('asignando rol a un usuario...')
        
        usuario = Usuario.objects.get(email=emailUsuarioAsignar)
        rol = Rol.objects.get(idRol=idRol)
        
        #creamos la tabla intermedia la cual almacena los ids de rol y permiso
        usuarioRol = UsuariosRoles.objects.create(usuario=usuario, rol=rol,
                                fechaDesde=fechaDesde, fechaHasta=fechaHasta)
        mensaje = 'Asignacion exitosa'
    else:
        mensaje = 'Error: La fecha seleccionada ' + fechaDesde.strftime("%d-%m-%Y") + ' - ' + fechaHasta.strftime("%d-%m-%Y") + ' se solapa con el rol: '
        mensaje += esValida[1].nombre  + ' - '  + str(esValida[2]) + ' - ' + str(esValida[3])
        print(f'mensaje: {mensaje}')
        
    listaRolesDisponibles = getRolesDisponibles(emailUsuarioAsignar)
    
    return render(request, 'asignacionRol.html', {
                                    'email':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioAsignar,
                                    'roles': listaRolesDisponibles,
                                    'mensaje': mensaje})
    
def validarFechaRol(email, idRol, fechaDesdeNuevo, fechaHastaNuevo):
    rolesAsignados = getRolesAsignados(email)
    for rol in rolesAsignados:
        #for fecha in rolesAsignados[rol]:
        # print(rolesAsignados[rol])
        # print(fechaDesde)
        fechaDesde = rolesAsignados[rol][0]
        fechaHasta = rolesAsignados[rol][1]
        
        if (fechaDesdeNuevo >= fechaDesde and fechaDesdeNuevo <= fechaHasta):
            #la fecha coincide con otra fecha de un rol
            return (False, rol, fechaDesde.strftime("%d-%m-%Y"), fechaHasta.strftime("%d-%m-%Y"))
            
        if (fechaHastaNuevo >= fechaHasta and fechaHastaNuevo <= fechaHasta):
            #la fecha coincide con otra fecha de un rol
            return (False, rol, fechaDesde.strftime("%d-%m-%Y"), fechaHasta.strftime("%d-%m-%Y"))

    #fecha valida
    return (True, None)


def asignacionPermiso(request, emailAdmin, idRolAsignar):
    listaPermisosDisponibles = getPermisosDisponibles(idRolAsignar)
    
    return render(request, 'asignacionPermiso.html', {
                                    'email':emailAdmin,
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
                                    'email':emailAdmin,
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


def getUsuariosDisponibles(idProyecto):
    '''
    Se obtiene todos los usuarios disponibles para ese proyecto
    '''
    listaUsuariosAsociados = []
    listaUsuarios = []
    usuariosProyectos = []
    
    #tabla intermedia entre Usuario y Proyecto (relacion M-M)
    try:
        usuariosProyectos = UsuariosProyectos.objects.all()
    except:
        #en caso de que no haya ningun rol todavia en la BD
        pass
    
    #obtenemos todos los usuarios actuales asociados a dicho proyecto
    for usuarioProyecto in usuariosProyectos:
        if int(usuarioProyecto.proyecto_id) == int(idProyecto):
            usuario = Usuario.objects.get(email=usuarioProyecto.usuario_id)
            listaUsuariosAsociados.append(usuario)
            
    #obtenemos todos los usuarios
    listaUsuariosAux = []
    try:
        #en caso de que no exista ningun usuario
        listaUsuariosAux = Usuario.objects.all()
    except:
        pass
    
    #obtenemos todos los usuarios disponibles para ser asignados
    for usuario in listaUsuariosAux:
        siEsta = False
        for usuarioAsociado in listaUsuariosAsociados:
            if usuario.email == usuarioAsociado.email:
                siEsta = True
                break
            
        if siEsta == False:
            listaUsuarios.append(usuario)
        
    return listaUsuarios

'''
def getRolesDisponibles(emailUsuarioAsignar):
    Se obtiene todos los roles disponibles para ese usuario
    
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
'''


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
        #permisosAsignados = Permiso.objects.filter(idPermiso=rolPermiso.permiso_id)
    except:
        pass
    
    #tabla intermedia entre Rol y Permiso (relacion M-M)
    for rolPermiso in rolesPermisos:
        if int(rolPermiso.rol_id) == int(idRol):
            permiso = Permiso.objects.get(idPermiso=rolPermiso.permiso_id)
            #print(permiso)
            permisosAsignados.append(permiso)

    return permisosAsignados


def getRolesAsignados(email):
    usuariosRoles = []
    rolesAsignados = {}
    fechas = []
    try:
        #tabla intermedia entre Usuario y Rol (relacion M-M)
        usuariosRoles = UsuariosRoles.objects.all()
    except:
        pass
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    for usuarioRol in usuariosRoles:
        if usuarioRol.usuario_id == email:
            rol = Rol.objects.get(idRol=usuarioRol.rol_id)
            fechas.append(usuarioRol.fechaDesde)
            fechas.append(usuarioRol.fechaHasta)
            rolesAsignados[rol] = fechas
            fechas = []
            #rolesAsignados.append(rol)
            
    #print(f'roles y fechas {rolesAsignados}')
    
    return rolesAsignados

'''
****************************
    MODULO SPRINTBACKLOG
****************************
'''

def sprintBackLog(request, emailAdmin, idBackLog):
    backLog = BackLog.objects.get(idBackLog=idBackLog)
    
    #traemos todos los SprintBackLogs que corresponden al BackLog
    listaSprintBackLogs = getSprintBackLogAsociados(idBackLog)
    
    #buscamos cual es el SprintBackLog en curso
    #sbl: Sprint BackLog
    sprintBackLog = None
    for sbl in listaSprintBackLogs:
        if sbl.estado == 'C':
            sprintBackLog = sbl
            break
    
    #global estado
    # if estado == False and sprintBackLog:
    #     thread = threading.Thread(target=cerrarSprintBackLog, kwargs={'sprintBackLog':sprintBackLog})
    #     thread.start()
    #if sprintBackLog:
    #    cerrarSprintBackLog(sprintBackLog)
    
    listaSprintBackLogs = getSprintBackLogAsociados(idBackLog)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': backLog,
                                        'nombrePantalla': 'SprintBackLog'})


def  cerrarSprintBackLog(sprintBackLog):
    '''
    VERIFICA CON UN HILO QUE QUE LA FECHA FIN DEL SPRINT
    SEA AUN MENOR A LA FECHA DE HOY PARA QUE SEA VALIDO,
    SINO SE CIERRA EL SPRINT
    '''
    
    #print('\nEjecutando hilo de verificacion de cierre del SprintBackLog...')
    print('\nEjecutando verificacion de cierre del SprintBackLog...')
    
    hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    hoy = str(hoy)
    
    #print(f'sprintBackLog: {sprintBackLog}')
    #print(f'fecha fin: {str(sprintBackLog.fechaFin)}')
    fechaFin = str(sprintBackLog.fechaFin)
    if hoy > fechaFin:
            #continue
        #print('.')
        #sleep(delay)
        
        #estado = True
        
        # print(f'sprintbacklog actual: {sprintBackLog.estado}')
        # print(f'sprintBackLog {sprintBackLog}')
        # print('-------------')
        
        #listamos todos los SprintBackLog
        listaSprintBackLog = SprintBackLog.objects.filter(backLog_id=sprintBackLog.backLog_id).order_by('fechaInicio')
        #for l in listaSprintBackLog:
        #    print(l)
        
        #buscamos el siguiente sprintbacklog en curso
        indice = 0
        for sbl in listaSprintBackLog:
            if sbl.estado == 'C':
                break
            
            indice += 1
        
        #cerramos el sprintbacklog actual
        sprintBackLog.estado = 'F'
        sprintBackLog.save()
        
        #print(f'indice: {indice}')
        
        #traemos el siguiente SprintBacklog a ejecutarse
        siguienteSprintBL = None
        
        #bandera para indicar que es el ultimo SprintBacklog
        esElUltimoSprintBackLog = False
        
        if indice < len(listaSprintBackLog) - 1:
            print('se pasa al siguente sprint...')
            #en caso de que ya este creado el siguiente sprint
            siguienteSprintBL = listaSprintBackLog[indice + 1]
            #iniciamos el siguiente sprint
            siguienteSprintBL.estado = 'C'
            siguienteSprintBL.save()
        else:
            esElUltimoSprintBackLog = True
            
            
        # print(f'siguiente: {siguienteSprintBL}')
        # print('----------------')

        
        tieneUserStoryPendientes = False
        #obtenemos los UserStories asociados a ese SprintBackLog finalizado
        listaUserStories = UserStory.objects.filter(sprintBackLog_id=sprintBackLog.idSprintBackLog)
        for us in listaUserStories:
            if us.estado != 'Finalizado':
                if tieneUserStoryPendientes == False:
                    tieneUserStoryPendientes = True
                    
                    #teniedo en cuenta que se trata del ultimo sprintbacklog y que 
                    #todavia tiene usert stories pendientes, se debe generar otro sprintbacklog
                    if esElUltimoSprintBackLog:
                        print('se crea un nuevo SPRINTBACKLOG')
                        nombre_por_defecto = 'SPRINTBACKLOG ' + str(SprintBackLog.objects.filter(backLog_id=sprintBackLog.backLog_id).count() + 1)
                        
                        #debemos crear un nuevo sprintbacklog
                        siguienteSprintBL = SprintBackLog.objects.create(nombre=nombre_por_defecto,
                                                descripcion=nombre_por_defecto, backLog=sprintBackLog.backLog, estado = 'C') 
                        #siguienteSprintBL.estado = 'C'
                        #siguienteSprintBL.save()
            
                
                #print(f'us, nombre -> {us.nombre}, estado -> {us.estado}, sprintbacklog -> {us.sprintBackLog}')
                #le asignamos al siguiente SprintBackLog
                us.sprintBackLog = siguienteSprintBL
                #lo guardamos en la BD
                us.save()
                #print(f'us, nombre -> {us.nombre}, estado -> {us.estado}, sprintbacklog -> {siguienteSprintBL}')
                
        
        #si el sprint a cerrar es el ultimo y si ya no ha US pendientes
        #entonces se deberia de cerrar el proyecto
        if esElUltimoSprintBackLog and tieneUserStoryPendientes == False:
            print('FINALIZAMOS EL PROYECTO....')
            #traemos el backlog asociado al sprint
            backLog = BackLog.objects.get(idBackLog=sprintBackLog.backLog_id)
            #traemos el proyecto en el que se encuentra
            proyecto = Proyecto.objects.get(idProyecto=backLog.proyecto_id)
            #finalizamos el proyecto
            proyecto.estado = 'F'
            proyecto.save()


def registrarSprintBackLog(request, emailAdmin, idBackLog):
    nombre = request.POST.get('txtNombreSprintBackLog')
    descripcion = request.POST.get('txtDescripcionSprintBackLog')

    fechaInicio= request.POST.get('fechaInicio')
    fechaFin= request.POST.get('fechaFin')
    hayFechaPorDefecto = False

    if fechaInicio == '' or fechaFin == '':
        print('Agregamos por defecto las fecha por defecto a 2 semanas')
        hayFechaPorDefecto = True
        siVacio = False

        sprintBackLogs = SprintBackLog.objects.filter(backLog_id=int(idBackLog)).order_by('-fechaFin')
        if len(sprintBackLogs) == 0:
            siVacio = True
        
        if siVacio == False:
            ultimoSBL = sprintBackLogs[0]
            fechaFinUltimo = ultimoSBL.fechaFin
            #print(f'fechaFinUltimo: {fechaFinUltimo}')
            #print(f'type: {type(fechaFinUltimo)}')
            fechaInicio = fechaFinUltimo + timedelta(days = 1)
            print(f'fechaInicioSiguiente: {fechaInicio}')
            fechaFin = fechaFinUltimo + timedelta(days = 15)
            print(f'fechaFinSiguiente: {fechaFin}')
        else:
            fechaInicio = datetime.date.today()
            fechaFin = fechaInicio + timedelta(days = 15)
    else:
        fechaInicio = parse_date(request.POST.get('fechaInicio'))
        fechaFin = parse_date(request.POST.get('fechaFin'))
        
    backLog = BackLog.objects.get(idBackLog=idBackLog)
    
    #se verifica que la fecha sea valida
    esValida = validarFechaSprintBackLog(-1, idBackLog, fechaInicio, fechaFin)
    mensaje = None
    
    operacionExitosa = ''
    if esValida[0]:
        #se crear el SprintBackLog asociandolo a un BackLog
        
        hoy = datetime.date.today()
        
        #si la fecha de hoy se encuentra en el rango de fechas, entonces lo marcamos EN CURSO
        if hoy >= fechaInicio and hoy <= fechaFin:
            sprintBackLog = SprintBackLog.objects.create(nombre=nombre, descripcion=descripcion,
                                                estado = 'C', fechaInicio=fechaInicio, fechaFin=fechaFin, backLog=backLog)
            
            proyecto = Proyecto.objects.get(idProyecto = backLog.proyecto_id)
            proyecto.estado = 'C'
            proyecto.save()
        elif fechaInicio < hoy and fechaFin < hoy:
            sprintBackLog = SprintBackLog.objects.create(nombre=nombre, descripcion=descripcion,
                                                estado = 'F', fechaInicio=fechaInicio, fechaFin=fechaFin, backLog=backLog)
        else:
            sprintBackLog = SprintBackLog.objects.create(nombre=nombre, descripcion=descripcion,fechaInicio=fechaInicio, fechaFin=fechaFin, backLog=backLog)
        
        mensaje = 'Registro exitoso.'
        operacionExitosa = 'si'
        
        if hayFechaPorDefecto:
            mensaje += ' Se agrego la fecha por DEFECTO A 2 SEMANAS'
    else:
        mensaje = 'Error: La fecha seleccionada ' + fechaInicio.strftime("%d-%m-%Y") + ' - ' + fechaFin.strftime("%d-%m-%Y") + ' se solapa con el SprintBackLog: '
        mensaje += esValida[1].nombre  + ' - '  + str(esValida[2]) + ' - ' + str(esValida[3])
        print(f'mensaje: {mensaje}')
        operacionExitosa = 'no'
    
    listaSprintBackLogs = getSprintBackLogAsociados(idBackLog)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': backLog,
                                        'nombrePantalla': 'SprintBackLog',
                                        'mensaje': mensaje,
                                        'operacionExitosa':operacionExitosa})


def validarFechaSprintBackLog(idSprintBackLog, idBackLog, fechaDesdeNuevo, fechaHastaNuevo):
    sprintBackLogsAsignados = getSprintBackLogAsociados(idBackLog)
    for sp in sprintBackLogsAsignados:
        if sp.idSprintBackLog != idSprintBackLog:
            #for fecha in rolesAsignados[rol]:
            # print(rolesAsignados[rol])
            # print(fechaDesde)
            fechaDesde = sp.fechaInicio
            fechaHasta = sp.fechaFin
            
            if (fechaDesdeNuevo >= fechaDesde and fechaDesdeNuevo <= fechaHasta):
                #la fecha coincide con otra fecha de un sprintbacklog
                return (False, sp, fechaDesde.strftime("%d-%m-%Y"), fechaHasta.strftime("%d-%m-%Y"))
                
            if (fechaHastaNuevo >= fechaDesde and fechaHastaNuevo <= fechaHasta):
                #la fecha coincide con otra fecha de un sprintbacklog
                return (False, sp, fechaDesde.strftime("%d-%m-%Y"), fechaHasta.strftime("%d-%m-%Y"))

    #fecha valida
    return (True, None)

def finalizarSprintBackLog(request, emailAdmin, idSprintBackLog):
    print('finalizando el SprintBackLog...')
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    
    #traemos los user stories que ya fueron asignados a esta sprintBackLog
    userStoryAsignados = getUserStoryAsignadosASprintBackLog(idSprintBackLog)
    operacionExitosa = ''
    mensaje = ''
        
    if sprintBackLog.estado == 'C':
        userStoryEstanFinalizados = True
        for userStory in userStoryAsignados:
            if userStory.estado != 'Finalizado':
                userStoryEstanFinalizados = False
                break
        
        if userStoryEstanFinalizados:
            mensaje = 'SprintBackLog finalizado exitosamente'
            
            #listamos todos los SprintBackLog
            listaSprintBackLog = SprintBackLog.objects.filter(backLog_id=sprintBackLog.backLog_id).order_by('fechaInicio')
            
            #buscamos el siguiente sprintbacklog
            indice = 0
            for sbl in listaSprintBackLog:
                if sbl.estado == 'C':
                    break
                
                indice += 1
            
            #cerramos el sprintbacklog actual
            sprintBackLog.estado = 'F'
            #asignamos la fecha de finalizacion el de hoy
            sprintBackLog.fechaFin = datetime.date.today()
            sprintBackLog.save()
            
            #print(f'indice: {indice}')
            
            #traemos el siguiente SprintBacklog a ejecutarse
            siguienteSprintBL = None
            
            #bandera para indicar que es el ultimo SprintBacklog
            esElUltimoSprintBackLog = False
            
            if indice < len(listaSprintBackLog) - 1:
                print('se pasa al siguente sprint...')
                #en caso de que ya este creado el siguiente sprint
                siguienteSprintBL = listaSprintBackLog[indice + 1]
                #iniciamos el siguiente sprint
                siguienteSprintBL.estado = 'C'
                siguienteSprintBL.save()
                
                actualizarFechasSprintBackLog(listaSprintBackLog, datetime.date.today(), indice + 1)
            else:
                esElUltimoSprintBackLog = True 
            
            
            #si el sprint a cerrar es el ultimo y si ya no ha US pendientes
            #entonces se deberia de cerrar el proyecto
            if esElUltimoSprintBackLog:
                print('FINALIZAMOS EL PROYECTO....')
                #traemos el backlog asociado al sprint
                backLog = BackLog.objects.get(idBackLog=sprintBackLog.backLog_id)
                #traemos el proyecto en el que se encuentra
                proyecto = Proyecto.objects.get(idProyecto=backLog.proyecto_id)
                #finalizamos el proyecto
                proyecto.estado = 'F'
                proyecto.save()
                
                
                mensaje += '. Ademas el proyecto se ha FINALIZADO'
                
            operacionExitosa = 'si'
        else:
            mensaje = 'No se puede finalizar el SprintBackLog por que tiene US pendientes'   
            operacionExitosa = 'no'
    elif sprintBackLog.estado == 'F':
        operacionExitosa = 'no'
        mensaje = 'El EsprintBackLog ya esta "finalizado"'
    else:
        operacionExitosa = 'no'
        mensaje = 'No se puede finalizar el SprintBackLog que no esta "en curso"'
           
    listaSprintBackLogs = getSprintBackLogAsociados(sprintBackLog.backLog_id)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': sprintBackLog.backLog,
                                        'nombrePantalla': 'SprintBackLog',
                                        'mensaje': mensaje,
                                        'operacionExitosa':operacionExitosa})
    
def actualizarFechasSprintBackLog(listaSprintBackLog, fechaFinAnterior, indiceNuevo):
    actual = listaSprintBackLog[indiceNuevo]
    #obtenemos la deferencia de dias entre la fecha de finalizacion del sprint actual
    #e incio del siguiente
    diferenciasDias = actual.fechaInicio - fechaFinAnterior
    # print(f'tipo: {type(actual.fechaInicio)}')
    # print(f'tipo: {type(fechaFinAnterior)}')
    # print(f'tipo: {type(diferenciasDias)}')
    # print(f'diferencia entre fechas: {diferenciasDias}')
    # print(f'diferencia entre fechas: {diferenciasDias.days}')

    print('Nuevas fechas para los SprintBackLogs')
    if diferenciasDias.days > 0:
        for i in range(indiceNuevo, len(listaSprintBackLog)):
            #adelantamos los sprints de acuerdo a la cantidad de dias

            listaSprintBackLog[i].fechaInicio = fechaFinAnterior
            listaSprintBackLog[i].fechaFin = listaSprintBackLog[i].fechaFin - timedelta(days = diferenciasDias.days)
            listaSprintBackLog[i].save()
                
            fechaFinAnterior = listaSprintBackLog[i].fechaFin
            
            print(f'inicio1: {listaSprintBackLog[i].fechaInicio} - fin1: {listaSprintBackLog[i].fechaFin}')
            fechaFinAnterior = fechaFinAnterior + timedelta(days = 1)
        
    
def edicionSprintBackLog(request, emailAdmin, idSprintBackLogAEditar):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLogAEditar)
    
    return render(request, 'edicionSprintBackLog.html', {'sprintBackLog': sprintBackLog,
                                            'email':emailAdmin})  


def editarSprintBackLog(request, emailAdmin, idSprintBackLogAEditar):
    nombre = request.POST.get('txtNombreSprintBackLog')
    descripcion = request.POST.get('txtDescripcionSprintBackLog')
    fechaInicio = parse_date(request.POST.get('fechaInicio'))
    fechaFin = parse_date(request.POST.get('fechaFin'))
    
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLogAEditar)
    
    
    #se verifica que la fecha sea valida
    esValida = validarFechaSprintBackLog(sprintBackLog.idSprintBackLog, sprintBackLog.backLog_id, fechaInicio, fechaFin)
    mensaje = None
    operacionExitosa = ''
    if esValida[0]:
        #if sprintBackLog.estado == 'C':
        #    cerrarSprintBackLog(sprintBackLog)
            
            
        #se crear el SprintBackLog asociandolo a un BackLog
        
        hoy = datetime.date.today()
        
        #si la fecha de hoy se encuentra en el rango de fechas, entonces lo marcamos EN CURSO
        if hoy >= fechaInicio and hoy <= fechaFin:
            sprintBackLog.estado = 'C'
            
            backLog = BackLog.objects.get(idBackLog = sprintBackLog.backLog_id)
            proyecto = Proyecto.objects.get(idProyecto = backLog.proyecto_id)
            proyecto.estado = 'C'
            proyecto.save()
            
        elif fechaInicio < hoy and fechaFin < hoy:
            sprintBackLog.estado = 'F'
        else:
            sprintBackLog.estado = 'I'
            
            
        #guardamos las nuevos datos
        sprintBackLog.nombre = nombre
        sprintBackLog.descripcion = descripcion
        sprintBackLog.fechaInicio = fechaInicio
        sprintBackLog.fechaFin = fechaFin
        sprintBackLog.save()
        
        mensaje = 'Edicion exitosa'
        operacionExitosa = 'si'
    else:
        mensaje = 'Error: La fecha seleccionada ' + fechaInicio.strftime("%d-%m-%Y") + ' - ' + fechaFin.strftime("%d-%m-%Y") + ' se solapa con el SprintBackLog: '
        mensaje += esValida[1].nombre  + ' - '  + str(esValida[2]) + ' - ' + str(esValida[3])
        print(f'mensaje: {mensaje}')
        operacionExitosa = 'no'
        
    
    listaSprintBackLogs = getSprintBackLogAsociados(sprintBackLog.backLog.idBackLog)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': sprintBackLog.backLog,
                                        'nombrePantalla': 'SprintBackLog',
                                        'mensaje': mensaje,
                                        'operacionExitosa':operacionExitosa})
        

def eliminarSprintBackLog(request, emailAdmin, idSprintBackLogAEliminar):
    #obtenemos el SprintBackLog correspondiente
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLogAEliminar)
    backLog = sprintBackLog.backLog
    
    sprintBackLog.delete()
    
    listaSprintBackLogs = getSprintBackLogAsociados(backLog.idBackLog)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': backLog,
                                        'nombrePantalla': 'SprintBackLog'})
    
    
def getSprintBackLogAsociados(idBackLog):
    sprintBackLogs = []
    
    try:
        sprintBackLogs = SprintBackLog.objects.filter(backLog_id=int(idBackLog)).order_by('fechaInicio')
    except:
        pass
    
    return sprintBackLogs


'''
********************************************************
    MODULO ASIGNACION ENTRE USER STORY Y SPRINTBACKLOG
********************************************************
'''

def asignacionUserStorySprintBackLog(request, emailAdmin, idSprintBackLogAsignar):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLogAsignar)
    listaUserStoryDisponibles = getUserStoryDisponibles()

    return render(request, 'asignacionUserStorySprintBackLog.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'userStories': listaUserStoryDisponibles})


def asignarUserStorySprintBackLog(request, emailAdmin, idSprintBackLog, idUserStory):
    #obtenemos el rol y el permiso
    print('asignando user story a un sprint backlog...')
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    userStory = UserStory.objects.get(idUserStory=idUserStory)
    
    userStory.sprintBackLog = sprintBackLog
    userStory.save()
    
    listaUserStoryDisponibles = getUserStoryDisponibles()
        
    return render(request, 'asignacionUserStorySprintBackLog.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'userStories': listaUserStoryDisponibles})
    


def verUserStorySprintBackLog(request, emailAdmin, idSprintBackLog):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    
    #traemos los user stories que ya fueron asignados a esta sprintBackLog
    userStoryAsignados = getUserStoryAsignadosASprintBackLog(idSprintBackLog)
    operacionExitosa = ''
    mensaje = ''

    if(len(userStoryAsignados) == 0):
        operacionExitosa = 'no'
        mensaje = 'El sprintBackLog esta vacio. Nada por mostrar'
    
    return render(request, 'verUserStorySprintBackLog.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'userStories':userStoryAsignados,
                                    'operacionExitosa': operacionExitosa,
                                    'mensaje': mensaje})

def porAsignacionUsuarioAUserStory(request, email, idUserStory):
    userStory = UserStory.objects.get(idUserStory=int(idUserStory))
    userStories = UserStory.objects.all()
    
    
    proyectos = Proyecto.objects.all().order_by('idProyecto')
    usuarios = []
    dic = {}
    for proyecto in proyectos:
        usuariosProyectos = UsuariosProyectos.objects.filter(proyecto_id=proyecto.idProyecto)
        usuarios = []
        for u in usuariosProyectos:
            usuarios.append(Usuario.objects.get(email=u.usuario_id))
        
        dic[proyecto] = usuarios
        
    return render(request, 'porAsignacionUsuarioAUserStory.html', {
                                    'email':email,
                                    'userStory': userStory,
                                    'dicProyectosUsuarios': dic})
    
    
def porAsignarUsuarioAUserStory(request, emailAdmin, idUserStory, email):
    userStory = UserStory.objects.get(idUserStory=int(idUserStory))
    usuario = Usuario.objects.get(email=email)
    
    #asignamos el usuario al user story
    userStory.usuario = usuario
    userStory.save()
    
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaUserStory = UserStory.objects.all().order_by('sprintBackLog')
    sprintBackLog = None
    
    
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory',
                                            'sprintBackLog': sprintBackLog
                                            })
    
    
    
    
    

def desasignarUserStorySprintBackLog(request, emailAdmin, idSprintBackLog, idUserStory):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    userStory = UserStory.objects.get(idUserStory=idUserStory)
    
    # userStory.sprintBackLog = None
    # userStory.save()
    userStory.delete()
    
    userStoryAsignados = getUserStoryAsignadosASprintBackLog(idSprintBackLog)
    
    return render(request, 'verUserStorySprintBackLog.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'userStories':userStoryAsignados})

    
def getUserStoryAsignadosASprintBackLog(idSprintBackLog):
    listaUserStory = []
    
    #obtenemos todos los User Story
    listaUserStoryAux = UserStory.objects.all().order_by('idUserStory')
    
    #obtenemos todos los User Story asociados a el SprintBackLog
    for userStory in listaUserStoryAux:
        if userStory.sprintBackLog_id != None:
            if userStory.sprintBackLog_id == int(idSprintBackLog):
                listaUserStory.append(userStory)
        
    return listaUserStory


def getUserStoryDisponibles():
    listaUserStory = []
    
    #obtenemos todos los User Story
    listaUserStoryAux = UserStory.objects.all()
    
    #obtenemos todos los User Story disponibles para ser asignados
    for userStory in listaUserStoryAux:
        if userStory.sprintBackLog_id == None:
            listaUserStory.append(userStory)
        
    return listaUserStory


def getSprintBackLogDisponibles():
    listaSprintBackLog = []
    
    #obtenemos todos los Sprint BackLog
    listaSprintBackLogAux = SprintBackLog.objects.all()
    
    #obtenemos todos los User Story disponibles para ser asignados
    #for sprintBackLog in listaSprintBackLogAux:
    #    if sprintBackLog.sprintBackLog_id == None:
    #        listaUserStory.append(userStory)
        
    return listaSprintBackLogAux

'''
*************************
    MODULO BACKLOG
*************************
'''

def backlog(request, emailAdmin, idProyecto, codigo):
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')

    proyecto = 'None'
    listaBackLogs = []
    
    if int(codigo) == 0:
        listaBackLogs = BackLog.objects.all().order_by('idBackLog')
    else:
        try:
            listaBackLogs.append(BackLog.objects.get(proyecto_id=idProyecto))
            proyecto = Proyecto.objects.get(idProyecto=idProyecto)
        except:
            pass

    #print(f'proyecto {proyecto}')
    #print('estoy aca????')
    #if codigo == 0:
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'BackLog',
                                        'proyecto':proyecto,
                                        'codigo': codigo})
    
def registrarBackLog(request, emailAdmin, nombreProyecto, descripcionProyecto):

    nombreBackLog = request.POST.get('txtNombreBackLog')
    descripcionBackLog = request.POST.get('txtDescripcionBackLog')

    #verificar en caso de que no tenga un proyecto
    #print(f'{nombre} {descripcion}')
    #proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    proyecto = Proyecto.objects.create(nombre=nombreProyecto, descripcion=descripcionProyecto)
    #print(f'proyecto {proyecto}')
    backLog = BackLog.objects.create(nombre=nombreBackLog, descripcion=descripcionBackLog, proyecto=proyecto)
        
    codigo = '0'
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
        
    listaBackLogs = BackLog.objects.all().order_by('idBackLog') 
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'BackLog',
                                        'proyecto': 'None',
                                        'codigo': codigo})
    

def edicionBackLog(request, emailAdmin, idBackLogAEditar, codigo):
    backLog = BackLog.objects.get(idBackLog=idBackLogAEditar)
    
    listaBackLogs = []
    if int(codigo) == 0:
        listaBackLogs = BackLog.objects.all().order_by('idBackLog')
    else:
        listaBackLogs.append(BackLog.objects.get(proyecto_id=backLog.proyecto_id))
    
    return render(request, 'edicionBackLog.html', {'backLog': backLog,
                                            'email':emailAdmin,
                                            'idProyecto': backLog.proyecto_id,
                                            'codigo': codigo})  
    


def editarBackLog(request, emailAdmin, idBackLogAEditar, idProyecto, codigo):
    nombre = request.POST.get('txtNombreBackLog')
    descripcion = request.POST.get('txtDescripcionBackLog')
    
    backLog = BackLog.objects.get(idBackLog=idBackLogAEditar)
    
    backLog.nombre = nombre
    backLog.descripcion = descripcion
    backLog.save()
    
    operacionExitosa = 'si'
    mensaje = 'Edicion exitosa'
    
    proyecto = None
    listaBackLogs = []
    if int(codigo) == 0:
        print('codigo 0')
        listaBackLogs = BackLog.objects.all().order_by('idBackLog')
    else:
        print('codigo no 0')
        listaBackLogs.append(BackLog.objects.get(proyecto_id=idProyecto))
        proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'BackLog',
                                        'proyecto':proyecto,
                                        'codigo': codigo,
                                    'operacionExitosa': operacionExitosa,
                                    'mensaje': mensaje})


def eliminarBackLog(request, emailAdmin, idBackLogAEliminar):
    #obtenemos el BackLog correspondiente
    backLog = None
    try:
        backLog = BackLog.objects.get(idBackLog=idBackLogAEliminar)
    except:
        pass
    
    sprintBackLogs = []
    try:
        sprintBackLogs = SprintBackLog.objects.all()
    except:
        pass
    
    codigo = '0'
    
    #eliminamos todos las asociaciones entre el BackLog a eliminar y sus SprintBackLog
    for sprintBackLog in sprintBackLogs:
        if int(sprintBackLog.backLog_id) == int(idBackLogAEliminar):
            sprintBackLog.delete()
    
    #eliminamos el backLog
    if backLog:
        proyecto = Proyecto.objects.get(idProyecto=backLog.proyecto_id)
        proyecto.delete()
        backLog.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    listaBackLogs = []
    #if int(codigo) == 0:
    listaBackLogs = BackLog.objects.all().order_by('idBackLog')
        
        
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'BackLog',
                                        'codigo': codigo
                                        })


def asignacionProyecto(request, emailAdmin):
    print('asginando proyecto a backlog...')
    
    permisosPorPantalla = []
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None

    return render(request, 'asignacionProyecto.html', {
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'Proyecto'})


def asignarProyecto(request, emailAdmin):
    permisosPorPantalla = []

    nombreProyecto = request.POST.get('txtNombreProyecto')
    descripcion = request.POST.get('txtDescripcionProyecto')
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')

    listaBackLogs = BackLog.objects.all().order_by('idBackLog')

    #proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    codigo = '0'
    
    #return render(request, 'backlog.html', {'email': emailAdmin})
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'BackLog',
                                        'proyecto': nombreProyecto,
                                        'descripcionProyecto': descripcion,
                                        'codigo': codigo})



def getProyectosSinBackLog():
    proyectosSinBackLog = []
    
    try:
        proyectos = Proyecto.objects.all()
        backLogs = BackLog.objects.all()
    except:
        pass
    
    
    for proyecto in proyectos:
        band = True
        for backLog in backLogs:
            print(f'{backLog.proyecto_id} {proyecto.idProyecto}')
            if backLog.proyecto_id == proyecto.idProyecto:
                band = False
                break
            
        if band:
            proyectosSinBackLog.append(proyecto)
    
    return proyectosSinBackLog
    '''
    
    '''
'''
*************************
    MODULO PROYECTO
*************************
'''

#Home del modulo
def proyecto(request, emailAdmin):
    backLog = None
    return render(request, 'proyecto.html', {'email': emailAdmin,
                                             'backLog': backLog})

#ABM de Proyecto
def proyectoAbm(request, emailAdmin, backLog):
    permisosPorPantalla = []
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    print(f'type: {type(backLog)}')
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'backLog': backLog,
                                    'nombrePantalla': 'Proyecto'})
    

def asignacionBackLogAProyecto(request, emailAdmin):
    print('asginando backlog a proyecto...')
    
    permisosPorPantalla = []
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None

    return render(request, 'asignacionBackLogAProyecto.html', {
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'BackLog'})
    

def asignarBackLogAProyecto(request, emailAdmin):
    nombre = request.POST.get('txtNombreBackLog')
    descripcion = request.POST.get('txtDescripcionBackLog')
    
    #backLog = BackLog.objects.create(nombre=nombre, descripcion=descripcion)
    #backLog.delete()
    
    permisosPorPantalla = []
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    #print(f'type: {type(backLog)}')
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'backLog': nombre,
                                    'descripcion': descripcion,
                                    'nombrePantalla': 'Proyecto'})
    
    
    
def registrarProyectoAbm(request, emailAdmin, nombreBackLog, descripcionBackLog):
    nombre = request.POST.get('txtNombreProyecto')
    descripcion = request.POST.get('txtDescripcionProyecto')

    proyectoAbm = Proyecto.objects.create(nombre=nombre, descripcion=descripcion)
    backlog = BackLog.objects.create(nombre=nombreBackLog, descripcion=descripcionBackLog, proyecto=proyectoAbm)
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'ProyectoAbm'})


def eliminarProyectoAbm(request, emailAdmin, idProyectoAbmAEliminar):
    #obtenemos el Proyecto correspondiente
    backLog = BackLog.objects.get(proyecto_id=idProyectoAbmAEliminar)
    proyectoAbm = Proyecto.objects.get(idProyecto=idProyectoAbmAEliminar)
    
    #tabla intermedia entre Proyecto y Usuario (relacion M-M)
    usuariosProyectos = []
    try:
        usuariosProyectos = UsuariosProyectos.objects.all()
    except:
        pass
    
    #eliminamos todos las asociaciones entre el proyecto a eliminar y sus usuarios
    for usuarioProyecto in usuariosProyectos:
        if int(usuarioProyecto.proyecto_id) == int(idProyectoAbmAEliminar):
            usuarioProyecto.delete()
    
    #eliminamos el proyecto
    proyectoAbm.delete()
    backLog.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'ProyectoAbm'})
    
    
def edicionProyectoAbm(request, emailAdmin, idProyectoAbmAEditar):
    proyectoAbm = Proyecto.objects.get(idProyecto=idProyectoAbmAEditar)
    
    return render(request, 'edicionProyectoAbm.html', {'proyecto': proyectoAbm,
                                            'email':emailAdmin})
    
    
def editarProyectoAbm(request, emailAdmin, idProyectoAbmAEditar):
    nombre = request.POST.get('txtNombreProyecto')
    descripcion = request.POST.get('txtDescripcionProyecto')
    
    proyectoAbm = Proyecto.objects.get(idProyecto=idProyectoAbmAEditar)
    
    proyectoAbm.nombre = nombre
    proyectoAbm.descripcion = descripcion
    proyectoAbm.save()
    operacionExitosa = 'si'
    mensaje = 'Se ha editado el proyecto con exito'
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'ProyectoAbm',
                                    'operacionExitosa': operacionExitosa,
                                    'mensaje': mensaje})
    
    

'''
*******************************************
    MODULO ASIGNACION USUARIO A PROYECTO
*******************************************
'''

def asignacionUsuarioProyecto(request,emailAdmin, idProyecto):
    listaUsuariosDisponibles = getUsuariosDisponibles(idProyecto)
    
    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    
    return render(request, 'asignacionUsuarioProyecto.html', {
                                    'email':emailAdmin,
                                    'proyecto': proyecto,
                                    'usuarios': listaUsuariosDisponibles})

   
def asignarUsuarioProyecto(request, emailAdmin, idProyecto, emailUsuarioAsignar):
    #obtenemos el proyecto y el usuario
    print('asignando un nuevo usuario al proyecto...')
    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    usuario = Usuario.objects.get(email=emailUsuarioAsignar)
    
    #creamos la tabla intermedia la cual almacena los ids de proyecto y de usuario
    usuarioProyecto = UsuariosProyectos.objects.create(usuario=usuario, proyecto=proyecto)
    
    listaUsuariosDisponibles = getUsuariosDisponibles(idProyecto)
    
    return render(request, 'asignacionUsuarioProyecto.html', {
                                    'email':emailAdmin,
                                    'proyecto': proyecto,
                                    'usuarios': listaUsuariosDisponibles})
   


def verUsuariosAsignadosProyecto(request, emailAdmin, idProyecto):
    usuariosAsignados = getUsuariosAsignadosProyecto(idProyecto)
    proyecto = Proyecto.objects.get(idProyecto=idProyecto)

    
    return render(request, 'verUsuariosAsignadosProyecto.html', {
                                    'email':emailAdmin,
                                    'proyecto': proyecto,
                                    'usuarios':usuariosAsignados})


def desasignarUsuarioProyecto(request, emailAdmin, idProyecto, emailUsuarioADesasignar):
    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    
    #tabla intermedia entre Usuario y Proyecto (relacion M-M)
    usuariosProyectos = UsuariosProyectos.objects.all()
    
    #eliminamos todos las asociaciones entre el proyecto a eliminar y el usuario
    for usuarioProyecto in usuariosProyectos:
        if int(usuarioProyecto.proyecto_id) == int(idProyecto):
            if usuarioProyecto.usuario_id == emailUsuarioADesasignar:
                print('quitando usuario...')
                usuarioProyecto.delete()
                
    usuariosAsignados = getUsuariosAsignadosProyecto(idProyecto)
    
    return render(request, 'verUsuariosAsignadosProyecto.html', {
                                    'email':emailAdmin,
                                    'proyecto': proyecto,
                                    'usuarios':usuariosAsignados})
    

def getUsuariosAsignadosProyecto(idProyecto):
    usuariosProyectos = []
    usuariosAsignados = []
    try:
        #tabla intermedia entre Usuario y Rol (relacion M-M)
        usuariosProyectos = UsuariosProyectos.objects.all()
    except:
        pass
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    for usuarioProyecto in usuariosProyectos:
        if int(usuarioProyecto.proyecto_id) == int(idProyecto):
            usuario = Usuario.objects.get(email=usuarioProyecto.usuario_id)
            usuariosAsignados.append(usuario)
    
    return usuariosAsignados

                                          
'''
*************************
    MODULO USER STORY
*************************
'''
def userstory(request, emailAdmin):
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaUserStory = UserStory.objects.all().order_by('sprintBackLog')
    # page = request.GET.get('page', 1)
    
    # try:
    #     paginator = Paginator(listaUserStory, 5)
    #     listaUserStory = paginator.page(page)
    # except:
    #     raise Http404
    
    sprintBackLog = None
    
    
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory',
                                            'sprintBackLog': sprintBackLog
                                            #'paginator': paginator,
                                            #'entity': listaUserStory
                                            })

def edicionAsignacionBackLog(request, emailAdmin, idUserStory):
    print('asginando backlog...')
    dicBackLogSprintBL = getTodosLosBackLogYSprints()
    
    return render(request, 'editarAsignacionBackLogAUserStory.html', {
                                    'email':emailAdmin,
                                    'idUserStory': idUserStory,
                                    'dic': dicBackLogSprintBL})
    
    
def editarAsignacionBackLog(request, emailAdmin, idSprintBackLog, idUserStory):    
    userStory = UserStory.objects.get(idUserStory=int(idUserStory))
    # page = request.GET.get('page', 1)
    
    # try:
    #     paginator = Paginator(listaUserStory, 5)
    #     listaUserStory = paginator.page(page)
    # except:
    #     raise Http404
    
    sp = SprintBackLog.objects.get(idSprintBackLog=int(idSprintBackLog))
    
    return render(request, 'edicionUserStory.html', {'userStory': userStory,
                                            'sprintBackLog': sp,
                                            'email':emailAdmin})


def asignacionBackLog(request, emailAdmin):
    print('asginando backlog...')
    dicBackLogSprintBL = getTodosLosBackLogYSprints()
    
    return render(request, 'asignacionBackLogAUserStory.html', {
                                    'email':emailAdmin,
                                    'dic': dicBackLogSprintBL})

def getTodosLosBackLogYSprints():
    listaBackLogs = BackLog.objects.all().order_by('idBackLog')
    listaSprintBackLogs = []
    dicBackLogSprintBL = {}
    
    for backLog in listaBackLogs:
        listaSprintBackLogs = SprintBackLog.objects.filter(backLog_id=backLog.idBackLog)
        dicBackLogSprintBL[backLog] = listaSprintBackLogs
    
    
    return dicBackLogSprintBL


def asignarBackLog(request, emailAdmin, idSprintBackLog):
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    # page = request.GET.get('page', 1)
    
    # try:
    #     paginator = Paginator(listaUserStory, 5)
    #     listaUserStory = paginator.page(page)
    # except:
    #     raise Http404
    
    sp = SprintBackLog.objects.get(idSprintBackLog=int(idSprintBackLog))
    
    
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory',
                                            'sprintBackLog': sp,
                                            #'paginator': paginator,
                                            #'entity': listaUserStory
                                            })

 

def registrarUserStory(request, emailAdmin, idSprintBackLog):
    
    
    operacionExitosa = ''
    mensaje = ''
    
    if int(idSprintBackLog) != 0:
        nombre = request.POST.get('txtNombreUserStory')
        descripcion = request.POST.get('txtDescripcionUserStory')
        
        sp = SprintBackLog.objects.get(idSprintBackLog=int(idSprintBackLog))
        userStory = UserStory.objects.create(nombre=nombre, descripcion=descripcion, sprintBackLog=sp)
        operacionExitosa = 'si'
        mensaje = 'User Story registrado con exito'
    else:
        operacionExitosa = 'no'
        mensaje = 'Debe asignarse un SprintBackLog'
    
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    # page = request.GET.get('page', 1)
    
    # try:
    #     paginator = Paginator(listaUserStory, 5)
    #     listaUserStory = paginator.page(page)
    # except:
    #     raise Http404
    
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory',
                                            'operacionExitosa':operacionExitosa,
                                            'mensaje': mensaje
                                            #'paginator': paginator,
                                            #'entity': listaUserStory
                                            })


def edicionUserStory(request, emailAdmin, idUserStoryAEditar):
    userStory = UserStory.objects.get(idUserStory=idUserStoryAEditar)
    
    return render(request, 'edicionUserStory.html', {'userStory': userStory,
                                            'sprintBackLog': userStory.sprintBackLog,
                                            'email':emailAdmin})


def editarUserStory(request, emailAdmin, idUserStoryAEditar, idSprintBackLog):
    nombre = request.POST.get('txtNombreUserStory')
    descripcion = request.POST.get('txtDescripcionUserStory')
    
    userStory = UserStory.objects.get(idUserStory=idUserStoryAEditar)
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=int(idSprintBackLog))
    
    userStory.nombre = nombre
    userStory.descripcion = descripcion
    userStory.sprintBackLog = sprintBackLog
    userStory.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
        
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    # page = request.GET.get('page', 1)
    
    # try:
    #     paginator = Paginator(listaUserStory, 5)
    #     listaUserStory = paginator.page(page)
    # except:
    #     raise Http404
    
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory'
                                            #'paginator': paginator,
                                            #'entity': listaUserStory
                                            })
    
    
def eliminarUserStory(request, emailAdmin, idUserStoryAEliminar):
    userStory = UserStory.objects.get(idUserStory=idUserStoryAEliminar)
    userStory.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    # page = request.GET.get('page', 1)
    
    # try:
    #     paginator = Paginator(listaUserStory, 5)
    #     listaUserStory = paginator.page(page)
    # except:
    #     raise Http404
    
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory'
                                            #'paginator': paginator,
                                            #'entity': listaUserStory
                                            })

def cambiarEstadoUserStory(request, emailAdmin, idUserStory, nuevoEstado, idSprintBackLog):
    userStory = UserStory.objects.get(idUserStory=idUserStory)

    operacionExitosa = ''
    mensaje = ''
    band = False
    
    if siEsAdmin(emailAdmin):
        band = True
    else:
        if userStory.usuario:
            band = userStory.usuario.email == emailAdmin
            
            if band == False:
                print(f'userStory.estado: {userStory.estado}')
                print(f'nuevoEstado: {nuevoEstado}')
                if nuevoEstado != 'Finalizado':
                    band = True
                else:
                    operacionExitosa = 'no'
                    mensaje = 'Solo el usuario asignado a este US puede finalizarlo'
        else:
            band = False
            operacionExitosa = 'no'
            mensaje = 'No tiene asignado ningun usuario'
    
    if band:
        userStory.estado = nuevoEstado
        userStory.save()
        
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
    
    if int(idSprintBackLog) == 0:
        #para este caso se asigna el estado desde el modulo PROYECTO/ USER STORY
        print('1')
        listaUserStory = UserStory.objects.all().order_by('idUserStory')
        # page = request.GET.get('page', 1)
        
        # try:
        #     paginator = Paginator(listaUserStory, 5)
        #     listaUserStory = paginator.page(page)
        # except:
        #     raise Http404
        
        return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory',
                                            'operacionExitosa': operacionExitosa,
                                            'mensaje': mensaje
                                            #'paginator': paginator,
                                            #'entity': listaUserStory
                                            })
    else:
        #para este caso se asigna el estado desde el modulo SPRINT BACKLOG/ USER STORY
        print('2')
        sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
        userStoryAsignados = getUserStoryAsignadosASprintBackLog(idSprintBackLog)
        return render(request, 'verUserStorySprintBackLog.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'userStories':userStoryAsignados})

def cambiarEstadoUSDesdeKanban(request, emailAdmin, idUserStory, nuevoEstado, idProyecto):
    #para este caso se asigna el estado desde el modulo PROYECTO / KANBAN
    userStory = UserStory.objects.get(idUserStory=idUserStory)
    
    
    operacionExitosa = ''
    mensaje = ''
    band = False

    if siEsAdmin(emailAdmin):
        band = True
    else:
        if userStory.usuario:
            band = userStory.usuario.email == emailAdmin
            
            if band == False:
                print(f'userStory.estado: {userStory.estado}')
                print(f'nuevoEstado: {nuevoEstado}')
                if nuevoEstado != 'Finalizado':
                    band = True
                else:
                    operacionExitosa = 'no'
                    mensaje = 'Solo el usuario asignado a este US puede finalizarlo'
        else:
            band = False
            operacionExitosa = 'no'
            mensaje = 'No tiene asignado ningun usuario'
    
    
    if band == True:
        print('Cambio de estado permitido...')
        userStory.estado = nuevoEstado
        userStory.save()
        
    sprintBackLog = None
    userStoryAsignados = []
    try:
        #sprintBackLog = SprintBackLog.objects.get(estado='En curso')
        
        #traemos el backlog asociado al proyecto
        backLog = BackLog.objects.get(proyecto_id=int(idProyecto))
        #traemos todos los sprint backlogs asociados
        listaSprintBackLogs = getSprintBackLogAsociados(backLog.idBackLog)
        #buscamos cual es el SprintBackLog en curso
        #sbl: Sprint BackLog
        for sbl in listaSprintBackLogs:
            if sbl.estado == 'C':
                sprintBackLog = sbl
                break
        
        #obtenemos los UserStories relcionados a dicho SprintBackLog
        userStoryAsignados = getUserStoryAsignadosASprintBackLog(sprintBackLog.idSprintBackLog)
    except:
        print('1')
        print('no existe ningun sprintbacklog en curso')
        pass
    proyecto = Proyecto.objects.get(idProyecto = idProyecto)
    
    return render(request, 'tableroKanban.html', {'userstories': userStoryAsignados,
                                            'email':emailAdmin,
                                            'proyecto': proyecto,
                                            'nombrePantalla': 'UserStory',
                                            'operacionExitosa': operacionExitosa,
                                            'mensaje': mensaje})
        



def getPermisosPorPantallaNuevo(emailAdmin, nombrePantalla):
    permisosPorPantalla = []
    permisosAsignados = []
    perPorPatalla = []

    if siEsAdmin(emailAdmin) == False:
        #obtenemos los roles del usuario 
        rolesAsignados = getRolesAsignados(emailAdmin)
        #print(f'rolesAsignados: {rolesAsignados}')
        #recorremos dichos roles para obtener los permisos
        for rolAsignado in rolesAsignados:
            perAsignados = getPermisosAsignadosARol(rolAsignado.idRol)
            permisosAsignados.extend(perAsignados)
        
        #verificamos que algunos de esos permisos correspondan a la pantalla/formulario
        for permisoAsignado in permisosAsignados:
            if permisoAsignado.formulario.lower() == nombrePantalla:
                perPorPatalla.append(permisoAsignado)
        
        print(f'perPorPatalla: {perPorPatalla}')
                
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
        
    return permisosPorPantalla


'''
*************************
    MODULO SPRINT
*************************
'''

def sprint(request, emailAdmin):
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprint')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaSprint = Sprint.objects.all()
    return render(request, 'sprint.html', {'sprints': listaSprint,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Sprint'})
    


def registrarSprint(request, emailAdmin):
    nombre = request.POST.get('txtNombreSprint')
    descripcion = request.POST.get('txtDescripcionSprint')

    #verificar en caso de que no tenga un proyecto
    print(f'{nombre} {descripcion}')
    sprint = Sprint.objects.create(nombre=nombre, descripcion=descripcion)
        
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprint')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaSprint = Sprint.objects.all()
    return render(request, 'sprint.html', {'sprints': listaSprint,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Sprint'})
    
    
def eliminarSprint(request, emailAdmin, idSprint):
    #obtenemos el Sprint correspondiente
    sprint = Sprint.objects.get(idSprint=idSprint)
    
    
    #eliminamos el Sprint
    sprint.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprint')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaSprints = Sprint.objects.all()
    return render(request, 'sprint.html', {'sprints': listaSprints,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Sprint'})



def edicionSprint(request, emailAdmin, idSprintAEditar):
    sprint = Sprint.objects.get(idSprint=idSprintAEditar)
    
    return render(request, 'edicionSprint.html', {'sprint': sprint,
                                            'email':emailAdmin})  

    
def editarSprint(request, emailAdmin, idSprint):
    nombre = request.POST.get('txtNombreSprint')
    descripcion = request.POST.get('txtDescripcionSprint')
    
    sprint = Sprint.objects.get(idSprint=idSprint)
    
    sprint.nombre = nombre
    sprint.descripcion = descripcion
    sprint.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprint')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None
        
    listaSprints = Sprint.objects.all()
    return render(request, 'sprint.html', {'sprints': listaSprints,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Sprint'})
    

'''
    ASIGNACION SPRINT BACKLOG A UN SPRINT
'''

def asignacionSprintBackloASprint(request, emailAdmin, idSprint):
    sprint = Sprint.objects.get(idSprint=idSprint)

    listaSprintBackLogDisponibles = getSprintBackLogDisponibles()

    return render(request, 'asignacionSprintBackloASprint.html', {
                                    'email':emailAdmin,
                                    'sprint': sprint,
                                    'sprintBackLogs': listaSprintBackLogDisponibles})
    
    
    

def tableroKanban(request, emailAdmin, idProyecto):
    #permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    sprintBackLog = None
    userStoryAsignados = []
    mensaje = ''
    operacionExitosa = ''
    try:
        #sprintBackLog = SprintBackLog.objects.get(estado='En curso')
        
        #traemos el backlog asociado al proyecto
        #print(f'idProyecto: {idProyecto}')
        backLog = BackLog.objects.get(proyecto_id=int(idProyecto))
        #print(f'backlog: {backLog}')
        #traemos todos los sprint backlogs asociados
        listaSprintBackLogs = getSprintBackLogAsociados(backLog.idBackLog)
        #buscamos cual es el SprintBackLog en curso
        #sbl: Sprint BackLog
        for sbl in listaSprintBackLogs:
            if sbl.estado == 'C':
                sprintBackLog = sbl
                break
        #obtenemos los UserStories relcionados a dicho SprintBackLog
        userStoryAsignados = getUserStoryAsignadosASprintBackLog(sprintBackLog.idSprintBackLog)
        
        if len(userStoryAsignados) == 0:
            print('el sprintBackLog esta vacio')
            operacionExitosa = 'no'
            mensaje = 'El sprintBackLog esta vacio. Nada por mostrar'
    except:
        print('no existe ningun sprintbacklog en curso')
        operacionExitosa = 'no'
        mensaje = 'No existe ningun sprintbacklog en curso por mostrar'
        pass
    
    proyecto = Proyecto.objects.get(idProyecto = idProyecto)
    
    return render(request, 'tableroKanban.html', {'userstories': userStoryAsignados,
                                            'email':emailAdmin,
                                            'proyecto': proyecto,
                                            'nombrePantalla': 'UserStory',
                                            'mensaje': mensaje})


def cambiarEstadoSprintBackLog(request, emailAdmin, idSprintBackLog, nuevoEstado):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    sprintBackLog.estado = nuevoEstado
    sprintBackLog.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'SprintBacklog')
    listasprintBackLog = SprintBackLog.objects.all().order_by('idSprintBackLog')
    
    if len(permisosPorPantalla) == 0:
        permisosPorPantalla = None

    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listasprintBackLog,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'SprintBacklog'})
    

def verGrafico(request, emailAdmin, idProyecto):
    
    listaSprintBackLogs = []
    backLog = None
    proyecto = None
    
    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    
    try:
        #obtenemos el backlog del proyecto
        backLog = BackLog.objects.get(proyecto_id=idProyecto)
    except:
        pass
    
    #obtenemos los sprintbacklos de ese backlog
    try:
        listaSprintBackLogs = SprintBackLog.objects.filter(backLog_id=backLog.idBackLog)
    except:
        pass
    
    
    
    return render(request, 'graficoBurnDown.html', {'sprintBackLogs': listaSprintBackLogs,
                                            'email':emailAdmin,
                                            'proyecto': proyecto,
                                            'nombrePantalla': 'Proyecto'})
    
    
def getSprintBackLogsApi(request, idProyecto):
    backLog = BackLog.objects.get(proyecto_id=int(idProyecto))
    sprintBackLogs = SprintBackLog.objects.filter(backLog_id=backLog.idBackLog).order_by('fechaInicio')

    labels = ['']
    sprint = 0
    totalUserStories = 0
    
    #contamos cuantos User Stories tiene el proyecto
    for sp in sprintBackLogs:
        userstories = UserStory.objects.filter(sprintBackLog_id=sp.idSprintBackLog)
        totalUserStories += len(userstories)
        
    defaultData = [totalUserStories]
    
    for sp in sprintBackLogs:
        userstories = UserStory.objects.filter(sprintBackLog_id=sp.idSprintBackLog)
        
        cantidadUserStories = 0
        for us in userstories:
            if us.estado == 'Finalizado':
                cantidadUserStories += 1
        

        if cantidadUserStories > 0:
            #print(f'cantidadUserStories: {cantidadUserStories} --- totalUserStories: {totalUserStories}')
            totalUserStories -= cantidadUserStories
            
        defaultData.append(totalUserStories)
        sprint += 1
        labels.append('Sprit ' + str(sprint))
 
    data = {
        'labels': labels,
        'default': defaultData
    }
    
    return JsonResponse(data)


def asignacionUserStoryUsuario(request, emailAdmin, idSprintBackLog, idUserStory):
    #obtenemos el sprintbacklog actual
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    #obtenemos el backlog asociado
    backLog = BackLog.objects.get(idBackLog=sprintBackLog.backLog_id)
    #obtenemos el proyecto asociado
    proyecto = Proyecto.objects.get(idProyecto=backLog.proyecto_id)
    
    #obtenemos los ids de los usuarios del proyecto
    listaUsuariosTemp = UsuariosProyectos.objects.filter(proyecto_id = proyecto.idProyecto)
    listaUsuarios = []
    
    userStory = UserStory.objects.get(idUserStory=idUserStory)
    
    #obtenemos todos los usuarios
    for usuario in listaUsuariosTemp:
        if userStory.usuario_id != usuario.usuario_id: #si son iguales es por que ya tiene asignado ese US
            listaUsuarios.append(Usuario.objects.get(email=usuario.usuario_id))

    
    

    return render(request, 'asignacionUserStoryUsuario.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'usuarios':listaUsuarios,
                                    'userStory': userStory,
                                    'idProyecto': proyecto.idProyecto})

#path('asignarUserStoryUsuario/<emailAdmin>/<idSprintBackLog>/<idUserStory>/<email>', views.asignarUserStoryUsuario),
def asignarUserStoryUsuario(request, emailAdmin, idSprintBackLog, idUserStory, email):
    #obtenemos el proyecto y el usuario
    print('asignando un nuevo usuario al user story...')
    userStory = UserStory.objects.get(idUserStory=int(idUserStory))
    usuario = Usuario.objects.get(email=email)
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=int(idSprintBackLog))
    
    #asignamos el usuario al user story
    userStory.usuario = usuario
    userStory.save()
    
    #traemos los user stories que ya fueron asignados a esta sprintBackLog
    userStoryAsignados = getUserStoryAsignadosASprintBackLog(idSprintBackLog)
    
    return render(request, 'verUserStorySprintBackLog.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'userStories':userStoryAsignados})