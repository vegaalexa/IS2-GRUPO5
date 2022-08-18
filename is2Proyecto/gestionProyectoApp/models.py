import email
from django.db import models

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    idProyecto = models.CharField(primary_key=True, max_length=6)
   
    def __str__(self):
        texto = '{0} ({1})'
        return texto.format(self.nombre, self.codigo)
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    idUsuario = models.CharField(primary_key=True, max_length=6)
   
    def __str__(self):
        texto = '{0} ({1}) {2}'
        return texto.format(self.nombre, self.email, self.idUsuario)
    
