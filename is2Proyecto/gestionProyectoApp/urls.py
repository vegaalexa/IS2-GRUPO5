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
    path('asignarPermiso/<emailAdmin>/<idRolAsignar>/<idPermiso>', views.asignarPermiso)
]