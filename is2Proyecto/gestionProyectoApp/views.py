from ast import Return
import email
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
#ASIGNACION

def login(request):
	return render(request, 'index.html')

def iniciarSesion(request):
    email = request.POST['yourEmail']
    contrasenia = request.POST['yourPassword']
    return render(request, 'homeProyecto.html', {'email': email})

def seguridad(request, emailAdmin):
    return render(request, 'seguridad.html', {'email': emailAdmin})

def siEsAdmin(emailAdmin):
    indice = emailAdmin.index('@') #obtenemos la posición del carácter @
    admin = emailAdmin[:indice]
    
    return admin == 'admin'

def usuario(request, emailAdmin):
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'usuario')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
        
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
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'permiso')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
        
    listaPermisos = Permiso.objects.all()
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
    listaPermisos = Permiso.objects.all()
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
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'rol')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaRol = Rol.objects.all()
    return render(request, 'rol.html', {'roles': listaRol,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'Rol'})
    
    
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
    


def verRolesAsignados(request, emailAdmin, emailUsuario):
    rolesAsignados = getRolesAsignados(emailUsuario)
    dic = {}
    dicRolesPermisos = {}
    
    for rolAsignado in rolesAsignados:
        permisosAsignadosARol = getPermisosAsignadosARol(rolAsignado.idRol)
        #ordenamsos la lista
        permisosAsignadosARol.sort(key=lambda permisosAsignadosARol: permisosAsignadosARol.descripcion)
        
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
                                    'emailAdmin':emailAdmin,
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
                                    'emailAdmin':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioQuitar,
                                    'roles': rolesAsignados})
#ASIGNACION
def asignacionRol(request, emailAdmin, emailUsuarioAsignar):
    listaRolesDisponibles = getRolesDisponibles(emailUsuarioAsignar)

    return render(request, 'asignacionRol.html', {
                                    'emailAdmin':emailAdmin,
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
                                    'emailAdmin':emailAdmin,
                                    'emailUsuarioAsignar': emailUsuarioQuitar,
                                    'roles': rolesAsignados})


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
    rolesAsignados = []
    try:
        #tabla intermedia entre Usuario y Rol (relacion M-M)
        usuariosRoles = UsuariosRoles.objects.all()
    except:
        pass
    
    #tabla intermedia entre Usuario y Rol (relacion M-M)
    for usuarioRol in usuariosRoles:
        if usuarioRol.usuario_id == email:
            rol = Rol.objects.get(idRol=usuarioRol.rol_id)
            rolesAsignados.append(rol)
            
    
    return rolesAsignados

'''
*************************
    MODULO BACKLOG
*************************
'''

def backlog(request, emailAdmin):
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'backlog')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']

    listaBackLogs = BackLog.objects.all()
    proyecto = None
    #return render(request, 'backlog.html', {'email': emailAdmin})
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog',
                                        'proyecto':proyecto})


def registrarBackLog(request, emailAdmin, idProyecto):

    nombre = request.POST.get('txtNombreBackLog')
    descripcion = request.POST.get('txtDescripcionBackLog')

    #verificar en caso de que no tenga un proyecto
    print(f'{nombre} {descripcion}')
    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    print(f'proyecto {proyecto}')
    backLog = BackLog.objects.create(nombre=nombre, descripcion=descripcion, proyecto=proyecto)
    
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'backlog')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaBackLogs = BackLog.objects.all()    
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog'})
    

def edicionBackLog(request, emailAdmin, idBackLogAEditar):
    backLog = BackLog.objects.get(idBackLog=idBackLogAEditar)
    
    return render(request, 'edicionBackLog.html', {'backLog': backLog,
                                            'email':emailAdmin})  
    


def editarBackLog(request, emailAdmin, idBackLogAEditar):
    nombre = request.POST.get('txtNombreBackLog')
    descripcion = request.POST.get('txtDescripcionBackLog')
    
    backLog = BackLog.objects.get(idBackLog=idBackLogAEditar)
    
    backLog.nombre = nombre
    backLog.descripcion = descripcion
    backLog.save()
    
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'backlog')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaBackLogs = BackLog.objects.all()    
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog'})


def eliminarBackLog(request, emailAdmin, idBackLogAEliminar):
    #obtenemos el BackLog correspondiente
    backLog = BackLog.objects.get(idBackLog=idBackLogAEliminar)
    
    sprintBackLogs = []
    try:
        sprintBackLogs = SprintBackLog.objects.all()
    except:
        pass
    
    #eliminamos todos las asociaciones entre el BackLog a eliminar y sus SprintBackLog
    for sprintBackLog in sprintBackLogs:
        if int(sprintBackLogs.backLog_id) == int(idBackLogAEliminar):
            sprintBackLog.delete()
    
    '''
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
    
    
    '''
    #eliminamos el backLog
    backLog.delete()
    
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'backlog')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaBackLogs = BackLog.objects.all()    
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog'})


def asignacionProyecto(request, emailAdmin):
    proyectos = getProyectosSinBackLog()
    
    return render(request, 'asignacionProyecto.html', {
                                    'email':emailAdmin,
                                    'proyectos': proyectos})


def asignarProyecto(request, emailAdmin, idProyecto):
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'backlog')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']

    listaBackLogs = BackLog.objects.all()

    proyecto = Proyecto.objects.get(idProyecto=idProyecto)
    #return render(request, 'backlog.html', {'email': emailAdmin})
    return render(request, 'backlog.html', {'backlogs': listaBackLogs,
                                        'email':emailAdmin,
                                        'permisosPorPantalla':permisosPorPantalla,
                                        'nombrePantalla': 'Backlog',
                                        'proyecto':proyecto})



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
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'proyectoAbm')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaProyectoAbm = Proyecto.objects.all() #En models.py está creado el modelo como Proyecto
    return render(request, 'proyectoAbm.html', {'proyectos': listaProyectoAbm,
                                    'email':emailAdmin,
                                    'permisosPorPantalla':permisosPorPantalla,
                                    'nombrePantalla': 'ProyectoAbm'})
    
    
def registrarProyectoAbm(request, emailAdmin):
    nombre = request.POST.get('txtNombreProyecto')
    descripcion = request.POST.get('txtDescripcionProyecto')

    proyectoAbm = Proyecto.objects.create(nombre=nombre, descripcion=descripcion)
    
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'proyectoAbm')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaProyectoAbm = Proyecto.objects.all() #En models.py está creado el modelo como Proyecto
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
    
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'proyectoAbm')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaProyectoAbm = Proyecto.objects.all() #En models.py está creado el modelo como Proyecto
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
    
    permisosPorPantalla = []
    
    if siEsAdmin(emailAdmin) == False:
        perPorPatalla = getPermisosPorPantalla(emailAdmin, 'proyectoAbm')
        permisosPorPantalla = []
        for permiso in perPorPatalla:
            permisosPorPantalla.append(permiso.tipo)
    else:
        permisosPorPantalla = ['C','R','U','D']
    
    listaProyectoAbm = Proyecto.objects.all() #En models.py está creado el modelo como Proyecto
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
                                    'emailAdmin':emailAdmin,
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
                                    'emailAdmin':emailAdmin,
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
                
'''
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
    
'''

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
    return render(request, 'userstory.html', {'email': emailAdmin})