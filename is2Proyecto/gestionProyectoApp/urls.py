from gestionProyectoApp import views
from django.urls import path

urlpatterns = [
	path('', views.login), 
	path('homeProyecto/', views.iniciarSesion),
	path('seguridad/<email>', views.seguridad),
 	path('usuario/<email>', views.usuario),
  	path('registrarUsuario/<email>', views.registrarUsuario),
   	path('eliminarUsuario/<email>/<emailAEliminar>', views.eliminarUsuario)
]
