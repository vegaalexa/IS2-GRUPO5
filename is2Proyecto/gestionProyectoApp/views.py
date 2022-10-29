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
        return render(request, 'index.html', {'mensaje': 'El usuario no existe'})
    
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
        
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'Usuario'})


def registrarUsuario(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    email = request.POST.get('txtEmail')
    
    usuario = Usuario.objects.create(nombre=nombre, email=email)
    listaUsuarios = Usuario.objects.all()
    return render(request, 'usuario.html', {'usuarios': listaUsuarios,
                                            'email':emailAdmin})


def eliminarUsuario(request, emailAdmin, emailAEliminar):
    usuario = Usuario.objects.get(email=emailAEliminar)
    
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
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'permiso')
        
    listaPermisos = Permiso.objects.all().order_by('idPermiso')
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Permiso'})
    
    
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
    listaPermisos = Permiso.objects.all().order_by('idPermiso')
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin})
    
    

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
    
    listaPermiso = Permiso.objects.all().order_by('idPermiso')
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
    
    listaPermisos = Permiso.objects.all().order_by('idPermiso')
    return render(request, 'permiso.html', {'permisos': listaPermisos,
                                            'email':emailAdmin})

#********************************************

#Vista para ABM de Roles

#********************************************
def rol(request, emailAdmin):        
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'rol')
    
    listaRol = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRol,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'Rol'})
    
    
def registrarRol(request, emailAdmin):
    nombre = request.POST.get('txtNombre')
    descripcion = request.POST.get('txtDescripcion')
    
    rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
    listaRol = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRol,
                                            'email':emailAdmin})
    
    

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
    
    listaRol = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRol,
                                            'email':emailAdmin})
    
    
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
    
    listaRoles = Rol.objects.all().order_by('idRol')
    return render(request, 'rol.html', {'roles': listaRoles,
                                            'email':emailAdmin})
    


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
            break
        
        p_aux = permisosAsignadosARol[0]
        permisosTipos = ''
        dic = {}
        for p in permisosAsignadosARol:
            if str(p.descripcion) != str(p_aux.descripcion):
                dic[str(p_aux.descripcion)] = permisosTipos
                p_aux = p
                permisosTipos = ''
                
            permisosTipos = permisosTipos + p.tipo + ' '

        dic[str(p_aux.descripcion)] = permisosTipos
        dicRolesPermisos[rolAsignado] = dic
       
    #print('--------------')
    #for clave in dicRolesPermisos.keys(): 
    #    for clave1 in dicRolesPermisos[clave].keys():
    #        print(f'{clave} {clave1} {dicRolesPermisos[clave][clave1]}')
    
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
        mensaje = 'La fecha seleccionada ' + fechaDesde.strftime("%d-%m-%Y") + ' - ' + fechaHasta.strftime("%d-%m-%Y") + ' se solapa con el rol: '
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
    except:
        pass
    
    #tabla intermedia entre Rol y Permiso (relacion M-M)
    for rolPermiso in rolesPermisos:
        if int(rolPermiso.rol_id) == int(idRol):
            permiso = Permiso.objects.get(idPermiso=rolPermiso.permiso_id)
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
    
    #cerrarSprintBackLog(sprintBackLog)
    global estado
    if estado == False and sprintBackLog:
        thread = threading.Thread(target=cerrarSprintBackLog(sprintBackLog))
        thread.start()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': backLog,
                                        'nombrePantalla': 'SprintBacklog'})


def  cerrarSprintBackLog(sprintBackLog):
    '''
    VERIFICA CON UN HILO QUE QUE LA FECHA FIN DEL SPRINT
    SEA AUN MENOR A LA FECHA DE HOY PARA QUE SEA VALIDO,
    SINO SE CIERRA EL SPRINT
    '''
    global estado
    
    hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    hoy = str(hoy)
    
    #print(f'sprintBackLog: {sprintBackLog}')
    #print(f'fecha fin: {str(sprintBackLog.fechaFin)}')
    fechaFin = str(sprintBackLog.fechaFin)
    #delay de 5 segundos
    delay = 5
    estado = True
    while estado:
        if hoy > fechaFin:
            estado = False
            continue
        print('.')
        sleep(delay)
    
    #estado = True
    
    # print(f'sprintbacklog actual: {sprintBackLog.estado}')
    # print(f'sprintBackLog {sprintBackLog}')
    # print('-------------')
    
    #listamos todos los SprintBackLog
    listaSprintBackLog = SprintBackLog.objects.filter(backLog_id=sprintBackLog.backLog_id).order_by('fechaInicio')
    for l in listaSprintBackLog:
        print(l)
    
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
    if indice < len(listaSprintBackLog) - 1:
        print('se pasa al siguente sprint...')
        #en caso de que ya este creado el siguiente sprint
        siguienteSprintBL = listaSprintBackLog[indice + 1]
    else:
        #generamos los datos del siguiente sprintbacklog
        print('se creo un nuevo SPRINTBACKLOG')
        nombre_por_defecto = 'SPRINTBACKLOG ' + str(SprintBackLog.objects.count() + 1)
        #debemos crear un nuevo sprintbacklog
        #siguienteSprintBL = SprintBackLog.objects.create(nombre=nombre_por_defecto,
        #                        descripcion=nombre_por_defecto, backLog=sprintBackLog.backLog)
        
        
    print(f'siguiente: {siguienteSprintBL}')
    print('----------------')
    #iniciamos el siguiente sprint
    siguienteSprintBL.estado = 'C'
    siguienteSprintBL.save()
    #obtenemos los UserStories asociados a ese SprintBackLog finalizado
    listaUserStories = UserStory.objects.filter(sprintBackLog_id=sprintBackLog.idSprintBackLog)
    for us in listaUserStories:
        if us.estado != 'F':
            print(f'us, nombre -> {us.nombre}, estado -> {us.estado}, sprintbacklog -> {us.sprintBackLog}')
            #le asignamos al siguiente SprintBackLog
            us.sprintBackLog = siguienteSprintBL
            #lo guardamos en la BD
            us.save()
            print(f'us, nombre -> {us.nombre}, estado -> {us.estado}, sprintbacklog -> {siguienteSprintBL}')
            
    
    #RETORNO TODOS LOS US NO FINALIZADOS
    #FALTA AGREGAR AL SIGUIENTE SPRINTBACKLOG


def registrarSprintBackLog(request, emailAdmin, idBackLog):
    nombre = request.POST.get('txtNombreSprintBackLog')
    descripcion = request.POST.get('txtDescripcionSprintBackLog')
    fechaInicio = parse_date(request.POST.get('fechaInicio'))
    fechaFin = parse_date(request.POST.get('fechaFin'))
    backLog = BackLog.objects.get(idBackLog=idBackLog)
    
    esValida = validarFechaSprintBackLog(idBackLog, fechaInicio, fechaFin)
    mensaje = None
    if esValida[0]:
        #se crear el SprintBackLog asociandolo a un BackLog
        sprintBackLog = SprintBackLog.objects.create(nombre=nombre, descripcion=descripcion,fechaInicio=fechaInicio, fechaFin=fechaFin, backLog=backLog)
        mensaje = 'Registro exitoso'
    else:
        mensaje = 'La fecha seleccionada ' + fechaInicio.strftime("%d-%m-%Y") + ' - ' + fechaFin.strftime("%d-%m-%Y") + ' se solapa con el SprintBackLog: '
        mensaje += esValida[1].nombre  + ' - '  + str(esValida[2]) + ' - ' + str(esValida[3])
        print(f'mensaje: {mensaje}')
    
    listaSprintBackLogs = getSprintBackLogAsociados(idBackLog)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': backLog,
                                        'nombrePantalla': 'SprintBacklog',
                                        'mensaje': mensaje})


def validarFechaSprintBackLog(idBackLog, fechaDesdeNuevo, fechaHastaNuevo):
    sprintBackLogsAsignados = getSprintBackLogAsociados(idBackLog)
    for sp in sprintBackLogsAsignados:
        #for fecha in rolesAsignados[rol]:
        # print(rolesAsignados[rol])
        # print(fechaDesde)
        fechaDesde = sp.fechaInicio
        fechaHasta = sp.fechaFin
        
        if (fechaDesdeNuevo >= fechaDesde and fechaDesdeNuevo <= fechaHasta):
            #la fecha coincide con otra fecha de un rol
            return (False, sp, fechaDesde.strftime("%d-%m-%Y"), fechaHasta.strftime("%d-%m-%Y"))
            
        if (fechaHastaNuevo >= fechaHasta and fechaHastaNuevo <= fechaHasta):
            #la fecha coincide con otra fecha de un rol
            return (False, sp, fechaDesde.strftime("%d-%m-%Y"), fechaHasta.strftime("%d-%m-%Y"))

    #fecha valida
    return (True, None)

def edicionSprintBackLog(request, emailAdmin, idSprintBackLogAEditar):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLogAEditar)
    
    return render(request, 'edicionSprintBackLog.html', {'sprintBackLog': sprintBackLog,
                                            'email':emailAdmin})  


def editarSprintBackLog(request, emailAdmin, idSprintBackLogAEditar):
    nombre = request.POST.get('txtNombreSprintBackLog')
    descripcion = request.POST.get('txtDescripcionSprintBackLog')
    fechaInicio = request.POST.get('fechaInicio')
    fechaFin = request.POST.get('fechaFin')
    
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLogAEditar)
    sprintBackLog.nombre = nombre
    sprintBackLog.descripcion = descripcion
    sprintBackLog.fechaInicio = fechaInicio
    sprintBackLog.fechaFin = fechaFin
    sprintBackLog.save()
    
    listaSprintBackLogs = getSprintBackLogAsociados(sprintBackLog.backLog.idBackLog)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': sprintBackLog.backLog,
                                        'nombrePantalla': 'SprintBacklog'})
    

def eliminarSprintBackLog(request, emailAdmin, idSprintBackLogAEliminar):
    #obtenemos el SprintBackLog correspondiente
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLogAEliminar)
    backLog = sprintBackLog.backLog
    
    sprintBackLog.delete()
    
    listaSprintBackLogs = getSprintBackLogAsociados(backLog.idBackLog)
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'sprintbacklog')
    
    return render(request, 'sprintBackLog.html', {'sprintBackLogs': listaSprintBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'backLog': backLog,
                                        'nombrePantalla': 'SprintBacklog'})
    
    
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
    
    return render(request, 'verUserStorySprintBackLog.html', {
                                    'email':emailAdmin,
                                    'sprintBackLog': sprintBackLog,
                                    'userStories':userStoryAsignados})
    

def desasignarUserStorySprintBackLog(request, emailAdmin, idSprintBackLog, idUserStory):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    userStory = UserStory.objects.get(idUserStory=idUserStory)
    
    userStory.sprintBackLog = None
    userStory.save()
    
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

    proyecto = None
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
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog',
                                        'proyecto':proyecto,
                                        'codigo': codigo})
    
def registrarBackLog(request, emailAdmin, idProyecto, codigo):

    nombre = request.POST.get('txtNombreBackLog')
    descripcion = request.POST.get('txtDescripcionBackLog')

    #verificar en caso de que no tenga un proyecto
    print(f'{nombre} {descripcion}')
    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    print(f'proyecto {proyecto}')
    backLog = BackLog.objects.create(nombre=nombre, descripcion=descripcion, proyecto=proyecto)
        
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    listaBackLogs = BackLog.objects.all().order_by('idBackLog') 
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog',
                                        'codigo': codigo})
    

def edicionBackLog(request, emailAdmin, idBackLogAEditar, idProyecto, codigo):
    backLog = BackLog.objects.get(idBackLog=idBackLogAEditar)
    
    listaBackLogs = []
    if int(codigo) == 0:
        listaBackLogs = BackLog.objects.all().order_by('idBackLog')
    else:
        listaBackLogs.append(BackLog.objects.get(proyecto_id=idProyecto))
    
    return render(request, 'edicionBackLog.html', {'backLog': backLog,
                                            'email':emailAdmin,
                                            'idProyecto': idProyecto,
                                            'codigo': codigo})  
    


def editarBackLog(request, emailAdmin, idBackLogAEditar, idProyecto, codigo):
    nombre = request.POST.get('txtNombreBackLog')
    descripcion = request.POST.get('txtDescripcionBackLog')
    
    backLog = BackLog.objects.get(idBackLog=idBackLogAEditar)
    
    backLog.nombre = nombre
    backLog.descripcion = descripcion
    backLog.save()
    
    proyecto = None
    listaBackLogs = []
    if int(codigo) == 0:
        listaBackLogs = BackLog.objects.all().order_by('idBackLog')
    else:
        listaBackLogs.append(BackLog.objects.get(proyecto_id=idProyecto))
        proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog',
                                        'proyecto':proyecto,
                                        'codigo': codigo})


def eliminarBackLog(request, emailAdmin, idBackLogAEliminar, codigo):
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
    
    #eliminamos todos las asociaciones entre el BackLog a eliminar y sus SprintBackLog
    for sprintBackLog in sprintBackLogs:
        if int(sprintBackLog.backLog_id) == int(idBackLogAEliminar):
            sprintBackLog.delete()
    
    #eliminamos el backLog
    if backLog:
        backLog.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')
    
    listaBackLogs = []
    if int(codigo) == 0:
        listaBackLogs = BackLog.objects.all().order_by('idBackLog')
        
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog',
                                        'codigo': codigo})


def asignacionProyecto(request, emailAdmin):
    proyectos = getProyectosSinBackLog()
    
    return render(request, 'asignacionProyecto.html', {
                                    'email':emailAdmin,
                                    'proyectos': proyectos})


def asignarProyecto(request, emailAdmin, idProyecto):
    permisosPorPantalla = []
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'backlog')

    listaBackLogs = BackLog.objects.all().order_by('idBackLog')

    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    
    
    codigo = '0'
    #return render(request, 'backlog.html', {'email': emailAdmin})
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog',
                                        'proyecto':proyecto,
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
    return render(request, 'proyecto.html', {'email': emailAdmin})

#ABM de Proyecto
def proyectoAbm(request, emailAdmin):
    permisosPorPantalla = []
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'Proyecto'})
    
    
def registrarProyectoAbm(request, emailAdmin):
    nombre = request.POST.get('txtNombreProyecto')
    descripcion = request.POST.get('txtDescripcionProyecto')

    proyectoAbm = Proyecto.objects.create(nombre=nombre, descripcion=descripcion)
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'ProyectoAbm'})


def eliminarProyectoAbm(request, emailAdmin, idProyectoAbmAEliminar):
    #obtenemos el Proyecto correspondiente
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
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
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
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'proyecto')
    
    listaProyectoAbm = Proyecto.objects.all().order_by('idProyecto') #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'ProyectoAbm'})
    
    

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
        
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory'})


def registrarUserStory(request, emailAdmin):
    nombre = request.POST.get('txtNombreUserStory')
    descripcion = request.POST.get('txtDescripcionUserStory')
    
    userStory = UserStory.objects.create(nombre=nombre, descripcion=descripcion)
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
        
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory'})


def edicionUserStory(request, emailAdmin, idUserStoryAEditar):
    userStory = UserStory.objects.get(idUserStory=idUserStoryAEditar)
    
    return render(request, 'edicionUserStory.html', {'userStory': userStory,
                                            'email':emailAdmin})


def editarUserStory(request, emailAdmin, idUserStoryAEditar):
    nombre = request.POST.get('txtNombreUserStory')
    descripcion = request.POST.get('txtDescripcionUserStory')
    
    userStory = UserStory.objects.get(idUserStory=idUserStoryAEditar)
    
    userStory.nombre = nombre
    userStory.descripcion = descripcion
    userStory.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
        
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory'})
    
    
def eliminarUserStory(request, emailAdmin, idUserStoryAEliminar):
    userStory = UserStory.objects.get(idUserStory=idUserStoryAEliminar)
    userStory.delete()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory'})
    

def cambiarEstadoUserStory(request, emailAdmin, idUserStory, nuevoEstado, idSprintBackLog):
    userStory = UserStory.objects.get(idUserStory=idUserStory)
    userStory.estado = nuevoEstado
    userStory.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'userstory')
    
    listaUserStory = UserStory.objects.all().order_by('idUserStory')
    
    if int(idSprintBackLog) == 0:
        #para este caso se asigna el estado desde el modulo PROYECTO/ USER STORY
        print('1')
        return render(request, 'userstory.html', {'userstories': listaUserStory,
                                            'email':emailAdmin,
                                            'permisosPorPantalla': permisosPorPantalla,
                                            'nombrePantalla': 'UserStory'})
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
                                            'nombrePantalla': 'UserStory'})
        
    
def getPermisosPorPantallaNuevo(emailAdmin, nombrePantalla):
    permisosPorPantalla = []
    permisosAsignados = []
    perPorPatalla = []

    if siEsAdmin(emailAdmin) == False:
        #obtenemos los roles del usuario 
        rolesAsignados = getRolesAsignados(emailAdmin)
        
        #recorremos dichos roles para obtener los permisos
        for rolAsignado in rolesAsignados:
            perAsignados = getPermisosAsignadosARol(rolAsignado.idRol)
            permisosAsignados.extend(perAsignados)
        
        #verificamos que algunos de esos permisos correspondan a la pantalla/formulario
        for permisoAsignado in permisosAsignados:
            if permisoAsignado.descripcion.lower() == nombrePantalla:
                perPorPatalla.append(permisoAsignado)
                
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
    except:
        print('no existe ningun sprintbacklog en curso')
        pass
    
    proyecto = Proyecto.objects.get(idProyecto = idProyecto)
    
    return render(request, 'tableroKanban.html', {'userstories': userStoryAsignados,
                                            'email':emailAdmin,
                                            'proyecto': proyecto,
                                            'nombrePantalla': 'UserStory'})


def cambiarEstadoSprintBackLog(request, emailAdmin, idSprintBackLog, nuevoEstado):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=idSprintBackLog)
    sprintBackLog.estado = nuevoEstado
    sprintBackLog.save()
    
    permisosPorPantalla = getPermisosPorPantallaNuevo(emailAdmin, 'SprintBacklog')
    listasprintBackLog = SprintBackLog.objects.all().order_by('idSprintBackLog')

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
    
    
def getSprintBackLogsApi(request, idSprintBackLog):
    sprintBackLog = SprintBackLog.objects.get(idSprintBackLog=int(idSprintBackLog))
    print(f'nombre del sprint: {sprintBackLog.nombre}')
    
    hoy = str(datetime.datetime.now().strftime ("%Y-%m-%d"))
    fechaInicio = str(sprintBackLog.fechaInicio)
    #print(f'fechaInicio: {fechaInicio} | hoy: {hoy}')
    
    # if fechaInicio < hoy:
    #     print('ya paso todo')
    # else:
    #     print('todavia no paso')
    listaUserStories = UserStory.objects.filter(sprintBackLog_id=idSprintBackLog)
    print(f'us cant: {len(listaUserStories)}')
    
    defaultData = []
    for i in range(len(listaUserStories)):
        defaultData.append(i + 1)
        
    print(defaultData)
    defaultData = [12, 19, 3, 5, 2, 3]
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange',]
 
    data = {
        'labels': labels,
        'default': defaultData
    }
    
    return JsonResponse(data)
