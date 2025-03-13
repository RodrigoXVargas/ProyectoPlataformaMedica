from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .dics import provincias, municipiosXProvincia, genero, dia
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    perfil_image = models.ImageField(upload_to="users", null=True, blank=True)
    id_direccion = models.ForeignKey('Direcc', related_name='direccion' ,on_delete=models.CASCADE)
    
    # Agregar related_name para evitar conflictos
    groups = models.ManyToManyField(Group, related_name='plataforma_users')
    user_permissions = models.ManyToManyField(Permission, related_name='plataforma_users')
        
    """ def get_image(self):
        if self.perfil_image:
            return '{}{}'.format(MEDIA_URL, self.perfil_image)
        return '{}{}'.format(STATIC_URL, 'img/empty.jpg') """

class Persona(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    genero = models.CharField(max_length=1,choices=genero, verbose_name='Género')
    fecha_nacimiento = models.DateField(default='2000-01-01')
    

class ObraSocial(models.Model):
    
    nombre = models.CharField(max_length=20)
    #instituciones = models.ManyToManyField('Institucion', through='Institucion_Obra_Social')
    #medicos = models.ManyToManyField('Medico', through='Medico_ObraSocial')
    #practicas = models.ManyToManyField('Practica', through='Obra_Social_Practica',verbose_name='Prácticas que cubre')

    class Meta:
        verbose_name_plural = 'Obras Sociales'

    def _str_(self):
        return self.nombre 
        
class Paciente(models.Model):
    numero_afiliado = models.BigIntegerField(blank=True, null=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete= models.CASCADE
    )
    id_obra_social = models.ForeignKey(ObraSocial, blank=True, null=True, on_delete=models.SET_DEFAULT, default=1, verbose_name='Obra Social')
    apoderado = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    #id_historia_clinica = models.IntegerField(blank=True,null=True)
    medicos = models.ManyToManyField('Medico', verbose_name='Médico con quien se atiende', blank=True)
    
    
    class Meta:
        verbose_name= "Paciente"
        
class Especialidad(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Especialidades'
        
class Medico(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete= models.CASCADE
    )
    
    num_matricula = models.IntegerField(verbose_name='Número de matricula')    
    id_especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_DEFAULT, default=1, verbose_name='Especialidad')
    #obras_sociales = models.ManyToManyField(ObraSocial) 
    """through='Medico_ObraSocial', through_fields=("id_medico", "id_obra_social"),verbose_name='Obras Sociales que atiende' """
    rating = models.FloatField(verbose_name='Rating', default = 0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    #practicas = models.ManyToManyField(Practica', through='Medico_Practica',verbose_name='Prácticas que realiza')
    # id_agenda = models.IntegerField(blank=True,null=True,verbose_name='Número de Agenda')
    pacientes = models.ManyToManyField(Paciente,verbose_name='Pacientes que atiende')
    
    class Meta:
        verbose_name = 'Medico'
        
class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numeracion = models.IntegerField()
    observaciones = models.CharField(max_length=500, null=True, blank=True)
    id_provincia = models.CharField(max_length=100,choices= provincias, default='X')
    id_departamento = models.CharField(max_length=100,choices= municipiosXProvincia, default='X')
    
    class Meta:
        verbose_name_plural = 'Direcciones'

""" class HorariosAtencion(models.Model):
    dia = models.CharField(max_length=10, choices= dia, default='Lunes', verbose_name='Día')
    hora_apertura = models.CharField(choices= OPCIONES_HORAS_APERTURA)
    minutos_apertura = models.CharField(choices= OPCIONES_MINUTOS_APERTURA)
    hora_cierre = models.CharField(choices= OPCIONES_HORAS_CIERRE)
    minutos_cierre = models.CharField(choices= OPCIONES_MINUTOS_CIERRE)

    class Meta:
        db_table = 'horarios_atencion'
        verbose_name_plural = 'Horarios de atención'
    
    def fecha_completa(self):
        return "{} {}:{} a {}:{}".format(self.dia, self.hora_apertura, self.minutos_apertura, self.hora_cierre, self.minutos_cierre)
    
    def __str__(self):
        return self.fecha_completa()


class Institucion(models.Model):
    fecha_inicio_actividad = models.DateField(default='2000-01-01', verbose_name='Fecha de inicio de actividad')
    nombre = models.CharField(max_length=25)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)
    mail = models.CharField(max_length=40)
    telefono = models.BigIntegerField()
    obras_sociales = models.ManyToManyField('ObraSocial', through='Institucion_Obra_Social',verbose_name= 'Obras sociales que acepta')
    horarios = models.ManyToManyField('HorariosAtencion', through='Institucion_Horarios')
    practicas = models.ManyToManyField('Practica', through='Practica_Institucion',verbose_name= 'Prácticas que realiza')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'institucion'
        verbose_name_plural = 'Instituciones' """