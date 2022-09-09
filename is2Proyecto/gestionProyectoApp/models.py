from tabnanny import verbose
from django.db import models

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=50)
    #Se comenta porque no corresponde el tipo de dato
    #idProyecto = models.CharField(primary_key=True, max_length=6)
    
    def generarIdProyecto():
            #este metodo nos ayuda a generar los valores de id para Proyecto
            #se debe mejorar este metodo
            valorPorDefecto = 100000
            cantidad = Proyecto.objects.count()
            if cantidad == None:
                return 1
            else:
                if cantidad == 0:
                    return valorPorDefecto
                #ordenamos y obtenemos el mayor id para luego sumarle 1
                proyecto = Proyecto.objects.filter().order_by('idProyecto').last()
                return proyecto.idProyecto + 1

    idProyecto = models.IntegerField(primary_key=True, default=generarIdProyecto)
    
   
    def __str__(self):
        texto = '{0} ({1})'
        return texto.format(self.nombre, self.idProyecto)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Proyecto'
        db_table = 'Proyecto'
    
class BackLog(models.Model):
    def generarIdBackLog():
        #este metodo nos ayuda a generar los valores de id para Permiso
        #se debe mejorar este metodo
        valorPorDefecto = 100000
        cantidad = BackLog.objects.count()
        if cantidad == None:
            return 1
        else:
            if cantidad == 0:
                return valorPorDefecto
            #ordenamos y obtenemos el mayor id para luego sumarle 1
            backLog = BackLog.objects.filter().order_by('idBackLog').last()
            return backLog.idBackLog + 1
        
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, default='')
    idBackLog = models.IntegerField(primary_key=True, default=generarIdBackLog)
    proyecto = models.OneToOneField(Proyecto,on_delete=models.CASCADE,
                                    null=True, blank=False)
    
   
    def __str__(self):
        texto = '{0} ({1})'
        return texto.format(self.nombre, self.idBackLog)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'BackLog'
        db_table = 'BackLog'


class SprintBackLog(models.Model):
    nombre = models.CharField(max_length=50)
    idSprintBackLog = models.CharField(primary_key=True, max_length=6)  
    backLog = models.ForeignKey(BackLog, null=True,
                                     blank=True, on_delete=models.CASCADE)    
    
   
    def __str__(self):
        texto = '{} {} {}'
        return texto.format(self.nombre, self.idSprintBackLog, self.backLog)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'SprintBackLog'
        db_table = 'SprintBackLog'


class Sprint(models.Model):
    nombre = models.CharField(max_length=50)
    idSprint = models.CharField(primary_key=True, max_length=6)  
    sprintBackLog = models.ForeignKey(SprintBackLog, null=True,
                                     blank=True, on_delete=models.CASCADE)
    
   
    def __str__(self):
        texto = '{} {} {}'
        return texto.format(self.nombre, self.idSprint, self.sprintBackLog)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Sprint'
        db_table = 'Sprint'


class UserStory(models.Model):
    nombre = models.CharField(max_length=50)
    idUserStory = models.CharField(primary_key=True, max_length=6)  
    sprintBackLog = models.ForeignKey(SprintBackLog, null=True,
                                     blank=True, on_delete=models.CASCADE)
    
   
    def __str__(self):
        texto = '{} {} {}'
        return texto.format(self.nombre, self.idSprint, self.sprintBackLog)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'UserStory'
        db_table = 'UserStory'


class Formulario(models.Model):
    def generarIdFormulario():
        #este metodo nos ayuda a generar los valores de id para Permiso
        #se debe mejorar este metodo
        valorPorDefecto = 100000
        cantidad = Formulario.objects.count()
        if cantidad == None:
            return 1
        else:
            if cantidad == 0:
                return valorPorDefecto
            #ordenamos y obtenemos el mayor id para luego sumarle 1
            formulario = Formulario.objects.filter().order_by('idFormulario').last()
            return formulario.idFormulario + 1
        
    nombre = models.CharField(max_length=50)
    #tipo = models.CharField(max_length=4)
    #descripcion = models.CharField(max_length=200, default='')
    idFormulario = models.IntegerField(primary_key=True)
   
   #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Formulario'
        db_table = 'Formulario'
        
    def __str__(self):
        texto = '{} {} {} {}'
        return texto.format(self.nombre, self.tipo,
                            self.descripcion, self.idFormulario)
    

class Permiso(models.Model):
    '''
    Abstraccion de la clase Permiso
    '''
    
    def generarIdPermisos():
        #este metodo nos ayuda a generar los valores de id para Permiso
        valorPorDefecto = 100000
        cantidad = Permiso.objects.count()
        
        if cantidad == None:
            return 1
        else:
            if cantidad == 0:
                return valorPorDefecto
            #ordenamos y obtenemos el mayor id para luego sumarle 1
            per = Permiso.objects.filter().order_by('idPermiso').last()
            return per.idPermiso + 1
    
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, default='')
    idPermiso = models.IntegerField(primary_key=True, default=generarIdPermisos)
    tipo = models.CharField(max_length=1, default='')
    formulario = models.ForeignKey(Formulario, null=True, on_delete=models.CASCADE)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Permiso'
        db_table = 'Permiso'

    
    def __str__(self):
        texto = '{} {} {}'
        return texto.format(self.nombre, self.descripcion, self.tipo)


class RolesPermisos(models.Model):
    rol = models.ForeignKey('Rol', related_name='roles_permisos', on_delete=models.SET_NULL, null=True)
    permiso = models.ForeignKey('Permiso', related_name='roles_permisos', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'RolesPermisos'
        db_table = 'RolesPermisos'
    
    
class Rol(models.Model):
    def generarIdRol():
        #este metodo nos ayuda a generar los valores de id para Permiso
        #se debe mejorar este metodo
        valorPorDefecto = 100000
        cantidad = Rol.objects.count()
        if cantidad == None:
            return 1
        else:
            if cantidad == 0:
                return valorPorDefecto
            #ordenamos y obtenemos el mayor id para luego sumarle 1
            rol = Rol.objects.filter().order_by('idRol').last()
            return rol.idRol + 1
        
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, default='')
    idRol = models.IntegerField(primary_key=True, default=generarIdRol)
    permisos = models.ManyToManyField(Permiso, through=RolesPermisos, related_name='rol_permiso')
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Rol'
        db_table = 'Rol'
        
    #def __str__(self):
    #    texto = '{0} ({1}) {2}'
    #    return texto.format(self.nombre, self.email, self.idUsuario)



class UsuariosRoles(models.Model):
    '''UsuariosRoles es una tabla intermedia entre Usuarios y Roles M-M'''
    usuario = models.ForeignKey('Usuario', related_name='usuarios_roles',
                                on_delete=models.SET_NULL, null=True)
    rol = models.ForeignKey('Rol', related_name='usuarios_roles',
                            on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'UsuariosRoles'
        db_table = 'UsuariosRoles'


class Usuario(models.Model):
    nombre = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(primary_key=True)
    
    roles = models.ManyToManyField(Rol, through=UsuariosRoles, related_name='usuario_rol')
    proyectos = models.ManyToManyField(Proyecto, related_name='usuario_proyecto')
   
    def __str__(self):
        texto = '{} {}'
        return texto.format(self.nombre, self.email)
    
    #personalizamos la tabla en posgres
    class Meta:
        verbose_name = 'Usuario'
        db_table = 'Usuario'
