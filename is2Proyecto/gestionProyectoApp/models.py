from tabnanny import verbose
from django.db import models

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    idProyecto = models.CharField(primary_key=True, max_length=6)
    
   
    def __str__(self):
        texto = '{0} ({1})'
        return texto.format(self.nombre, self.codigo)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Proyecto'
        db_table = 'Proyecto'
    

class Formulario(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=4)
    descripcion = models.CharField(max_length=200, default='')
    idFormulario = models.CharField(primary_key=True, max_length=6)
   
   #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Formulario'
        db_table = 'Formulario'
    def __str__(self):
        texto = '{} {} {} {}'
        return texto.format(self.nombre, self.tipo,
                            self.descripcion, self.idFormulario)
    

class Permiso(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, default='')
    idPermiso = models.CharField(primary_key=True, max_length=6)
    idFormulario = models.ForeignKey(Formulario, null=True, on_delete=models.CASCADE)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Permiso'
        db_table = 'Permiso'
        
    def __str__(self):
        texto = '{} {} {} {}'
        return texto.format(self.nombre, self.descripcion, self.idPermiso, self.idPermiso)
    
    
class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    idRol = models.CharField(primary_key=True, max_length=6)
    permisos = models.ManyToManyField(Permiso, related_name='rol_permiso')
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Rol'
        db_table = 'Rol'
        
    #def __str__(self):
    #    texto = '{0} ({1}) {2}'
    #    return texto.format(self.nombre, self.email, self.idUsuario)
    
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    idUsuario = models.CharField(primary_key=True, max_length=6)
    roles = models.ManyToManyField(Rol, related_name='usuario_rol')
    proyectos = models.ManyToManyField(Proyecto, related_name='usuario_proyecto')
   
    def __str__(self):
        texto = '{0} ({1}) {2}'
        return texto.format(self.nombre, self.email, self.idUsuario)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Usuario'
        db_table = 'Usuario'
