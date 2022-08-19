from tabnanny import verbose
from django.db import models

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    idProyecto = models.CharField(primary_key=True, max_length=6)
   
    def __str__(self):
        texto = '{0} ({1})'
        return texto.format(self.nombre, self.codigo)
    
    class Meta:
        verbose_name = 'Proyecto'
        db_table = 'Proyecto'
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    idUsuario = models.CharField(primary_key=True, max_length=6)
   
    def __str__(self):
        texto = '{0} ({1}) {2}'
        return texto.format(self.nombre, self.email, self.idUsuario)
    class Meta:
        verbose_name = 'Usuario'
        db_table = 'Usuario'

class Formulario(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=4)
    idFormulario = models.CharField(primary_key=True, max_length=6)
    #idFormulario = models.ForeignKey(Formulario, null=True, on_delete=models.CASCADE)
   
    class Meta:
        verbose_name = 'Formulario'
        db_table = 'Formulario'
    #def __str__(self):
    #    texto = '{0} ({1}) {2}'
    #    return texto.format(self.nombre, self.email, self.idUsuario)
    

class Permiso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    idPermiso = models.CharField(primary_key=True, max_length=6)
    idFormulario = models.ForeignKey(Formulario, null=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Permiso'
        db_table = 'Permiso'
    #def __str__(self):
    #    texto = '{0} ({1}) {2}'
    #    return texto.format(self.nombre, self.email, self.idUsuario)