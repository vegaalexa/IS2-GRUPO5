from gestionProyectoApp import views
from django.urls import path

urlpatterns = [
	path('', views.login), 
	path('homeProyecto/', views.iniciarSesion),
	path('seguridad/<emailAdmin>', views.seguridad),
 	path('usuario/<emailAdmin>', views.usuario),
  	path('registrarUsuario/<emailAdmin>', views.registrarUsuario),
   	path('eliminarUsuario/<emailAdmin>/<emailAEliminar>', views.eliminarUsuario),
	path('edicionUsuario/<emailAdmin>/<emailAEditar>', views.edicionUsuario),
	path('editarUsuario/<emailAdmin>/<emailAEditar>', views.editarUsuario),
	#PERMISOS
	path('permiso/<emailAdmin>', views.permiso),
	path('registrarPermiso/<emailAdmin>', views.registrarPermiso),
	path('eliminarPermiso/<emailAdmin>/<idPermisoAEliminar>', views.eliminarPermiso),
	path('edicionPermiso/<emailAdmin>/<idPermisoAEditar>', views.edicionPermiso),
	path('editarPermiso/<emailAdmin>/<idPermisoAEditar>', views.editarPermiso),
	#ROL
	path('rol/<emailAdmin>', views.rol),
	path('registrarRol/<emailAdmin>', views.registrarRol),
	path('eliminarRol/<emailAdmin>/<idRolAEliminar>', views.eliminarRol),
	path('edicionRol/<emailAdmin>/<idRolAEditar>', views.edicionRol),
	path('editarRol/<emailAdmin>/<idRolAEditar>', views.editarRol),
    #ASIGNACION DE ROL
    path('asignacionRol/<emailAdmin>/<emailUsuarioAsignar>', views.asignacionRol),
    path('asignarRol/<emailAdmin>/<emailUsuarioAsignar>/<idRol>', views.asignarRol),
    path('verRolesAsignados/<emailAdmin>/<emailUsuario>', views.verRolesAsignados),
    path('desasignacionRol/<emailAdmin>/<emailUsuarioQuitar>', views.desasignacionRol),
    path('desasignarRol/<emailAdmin>/<emailUsuarioQuitar>/<idRol>', views.desasignarRol),
    #ASIGNACION DE PERMISO
    path('asignacionPermiso/<emailAdmin>/<idRolAsignar>', views.asignacionPermiso),
    path('asignarPermiso/<emailAdmin>/<idRolAsignar>/<idPermiso>', views.asignarPermiso),
    path('verPermisosAsignados/<emailAdmin>/<idRol>', views.verPermisosAsignados),
    path('desasignarPermiso/<emailAdmin>/<idRolAsignar>/<idPermiso>', views.desasignarPermiso),
    path('proyecto/<emailAdmin>', views.proyecto),
    #BACKLOG
    path('backlog/<emailAdmin>', views.backlog),
    path('registrarBackLog/<emailAdmin>/<idProyecto>', views.registrarBackLog),
    path('edicionBackLog/<emailAdmin>/<idBackLogAEditar>', views.edicionBackLog),
    path('editarBackLog/<emailAdmin>/<idBackLogAEditar>', views.editarBackLog),
    path('eliminarBackLog/<emailAdmin>/<idBackLogAEliminar>', views.eliminarBackLog),
    #BACKLOG: ASIGNACION CON PROYECTO
    path('asignacionProyecto/<emailAdmin>', views.asignacionProyecto),
    path('asignarProyecto/<emailAdmin>/<idProyecto>', views.asignarProyecto),
    #PROYECTO
    path('proyectoAbm/<emailAdmin>', views.proyectoAbm),
    path('registrarProyectoAbm/<emailAdmin>', views.registrarProyectoAbm),
    path('eliminarProyectoAbm/<emailAdmin>/<idProyectoAbmAEliminar>', views.eliminarProyectoAbm),
    path('edicionProyectoAbm/<emailAdmin>/<idProyectoAbmAEditar>', views.edicionProyectoAbm),
    path('editarProyectoAbm/<emailAdmin>/<idProyectoAbmAEditar>', views.editarProyectoAbm),
    #PROYECTO: ASIGNACION USUARIO A PROYECTOS
    path('asignacionUsuarioProyecto/<emailAdmin>/<idProyecto>', views.asignacionUsuarioProyecto),
    path('asignarUsuarioProyecto/<emailAdmin>/<idProyecto>/<emailUsuarioAsignar>', views.asignarUsuarioProyecto),
    #verUsuariosAsignadosProyectos
    path('verUsuariosAsignadosProyecto/<emailAdmin>/<idProyecto>', views.verUsuariosAsignadosProyecto),
    path('desasignarUsuarioProyecto/<emailAdmin>/<idProyecto>/<emailUsuarioADesasignar>', views.desasignarUsuarioProyecto),
    #USER HISTORY
    path('userstory/<emailAdmin>', views.userstory),
]
