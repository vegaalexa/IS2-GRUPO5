from gestionProyectoApp import views
from django.urls import path

urlpatterns = [
	path('', views.login), 
	path('homeProyecto/', views.iniciarSesion),
    #CERRAR SESION
    path('cerrarSesion/', views.login), 
    #homeProyecto con el navbar
    path('homeProyecto2/<emailAdmin>', views.iniciarSesion2),
	path('seguridad/<emailAdmin>', views.seguridad),
 	path('usuario/<emailAdmin>', views.usuario),
  	path('registrarUsuario/<emailAdmin>', views.registrarUsuario),
   	path('eliminarUsuario/<emailAdmin>/<emailAEliminar>', views.eliminarUsuario),
	path('edicionUsuario/<emailAdmin>/<emailAEditar>', views.edicionUsuario),
	path('editarUsuario/<emailAdmin>/<emailAEditar>', views.editarUsuario),
	#PERMISOS
	path('permiso/<emailAdmin>', views.permiso),
	path('registrarPermiso/<emailAdmin>/<formulario>', views.registrarPermiso),
	path('eliminarPermiso/<emailAdmin>/<idPermisoAEliminar>', views.eliminarPermiso),
	path('edicionPermiso/<emailAdmin>/<idPermisoAEditar>', views.edicionPermiso),
	path('editarPermiso/<emailAdmin>/<idPermisoAEditar>/<formulario>', views.editarPermiso),
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
    path('backlog/<emailAdmin>/<idProyecto>/<codigo>', views.backlog),
    path('registrarBackLog/<emailAdmin>/<idProyecto>/<codigo>', views.registrarBackLog),
    path('edicionBackLog/<emailAdmin>/<idBackLogAEditar>/<idProyecto>/<codigo>', views.edicionBackLog),
    path('editarBackLog/<emailAdmin>/<idBackLogAEditar>/<idProyecto>/<codigo>', views.editarBackLog),
    path('eliminarBackLog/<emailAdmin>/<idBackLogAEliminar>/<codigo>', views.eliminarBackLog),
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
    path('registrarUserStory/<emailAdmin>/<idSprintBackLog>', views.registrarUserStory),
    path('edicionUserStory/<emailAdmin>/<idUserStoryAEditar>', views.edicionUserStory),
    path('editarUserStory/<emailAdmin>/<idUserStoryAEditar>', views.editarUserStory),
    path('eliminarUserStory/<emailAdmin>/<idUserStoryAEliminar>', views.eliminarUserStory),
    path('cambiarEstadoUserStory/<emailAdmin>/<idUserStory>/<nuevoEstado>/<idSprintBackLog>', views.cambiarEstadoUserStory),
    path('cambiarEstadoUSDesdeKanban/<emailAdmin>/<idUserStory>/<nuevoEstado>/<idProyecto>', views.cambiarEstadoUSDesdeKanban),
    path('asignacionBackLog/<emailAdmin>', views.asignacionBackLog),
    path('asignarBackLog/<emailAdmin>/<idSprintBackLog>', views.asignarBackLog),
    #SPRINTBACKLOGS
    path('sprintBackLog/<emailAdmin>/<idBackLog>', views.sprintBackLog),
    path('registrarSprintBackLog/<emailAdmin>/<idBackLog>', views.registrarSprintBackLog),
    path('edicionSprintBackLog/<emailAdmin>/<idSprintBackLogAEditar>', views.edicionSprintBackLog),
    path('finalizarSprintBackLog/<emailAdmin>/<idSprintBackLog>', views.finalizarSprintBackLog),
    path('editarSprintBackLog/<emailAdmin>/<idSprintBackLogAEditar>', views.editarSprintBackLog),
    path('eliminarSprintBackLog/<emailAdmin>/<idSprintBackLogAEliminar>', views.eliminarSprintBackLog),
    path('cambiarEstadoSprintBackLog/<emailAdmin>/<idSprintBackLog>/<nuevoEstado>', views.cambiarEstadoSprintBackLog),
    #ASIGNACION USER STORY A SPRINT BACKLOGS
    path('asignacionUserStorySprintBackLog/<emailAdmin>/<idSprintBackLogAsignar>', views.asignacionUserStorySprintBackLog),
    path('asignarUserStorySprintBackLog/<emailAdmin>/<idSprintBackLog>/<idUserStory>', views.asignarUserStorySprintBackLog),
    path('verUserStorySprintBackLog/<emailAdmin>/<idSprintBackLog>', views.verUserStorySprintBackLog),
    path('desasignarUserStorySprintBackLog/<emailAdmin>/<idSprintBackLog>/<idUserStory>', views.desasignarUserStorySprintBackLog),
    #SPRINT
    path('sprint/<emailAdmin>', views.sprint),
    path('registrarSprint/<emailAdmin>', views.registrarSprint),
    path('eliminarSprint/<emailAdmin>/<idSprint>', views.eliminarSprint),
    path('edicionSprint/<emailAdmin>/<idSprintAEditar>', views.edicionSprint),
    path('editarSprint/<emailAdmin>/<idSprint>', views.editarSprint),
    path('asignacionSprintBackloASprint/<emailAdmin>/<idSprint>', views.asignacionSprintBackloASprint),
    #ASIGNACION USUARIO A USER STORY
    path('asignacionUserStoryUsuario/<emailAdmin>/<idSprintBackLog>/<idUserStory>', views.asignacionUserStoryUsuario),
    path('asignarUserStoryUsuario/<emailAdmin>/<idSprintBackLog>/<idUserStory>/<email>', views.asignarUserStoryUsuario),
    #KAMBAN
    path('tableroKanban/<emailAdmin>/<idProyecto>', views.tableroKanban),
    #MODULO BURNDOWN
    path('verGrafico/<emailAdmin>/<idProyecto>', views.verGrafico),
    path('api/grafico/<idProyecto>', views.getSprintBackLogsApi),
]