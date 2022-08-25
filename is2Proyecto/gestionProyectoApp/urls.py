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
    path('permiso/<emailAdmin>', views.permiso),
    path('registrarPermiso/<emailAdmin>', views.registrarPermiso),
    path('eliminarPermiso/<emailAdmin>/<idPermisoAEliminar>', views.eliminarPermiso)
]
