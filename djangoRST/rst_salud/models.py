# MODELOS DE LA BASE DE DATOS

from django.db import models
from .genero import genero
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .dia import dia
from .hora import OPCIONES_HORAS_APERTURA , OPCIONES_HORAS_CIERRE
from .minutos import OPCIONES_MINUTOS_APERTURA, OPCIONES_MINUTOS_CIERRE


class DetallesPractica(models.Model):
    id_detalles_practica = models.AutoField(primary_key=True,verbose_name='ID')
    id_paciente = models.ForeignKey('Paciente',null=False,on_delete=models.CASCADE, db_column='id_paciente',verbose_name='Paciente')
    id_medico = models.ForeignKey('Medico',null=False,on_delete=models.CASCADE, db_column='id_medico',verbose_name='Médico')
    id_institucion = models.ForeignKey('Institucion',null=False,on_delete=models.CASCADE, db_column='id_institucion',verbose_name='Institución')
    id_practica = models.ForeignKey('Practica',null=False,on_delete=models.CASCADE, db_column='id_practica',verbose_name='Práctica')
    id_diagnostico = models.ForeignKey('Diagnostico',null=False,on_delete=models.CASCADE, db_column='id_diagnostico',verbose_name='Diagnóstico')
    fecha_generada = models.DateField(verbose_name='Iniciada')
    fecha_finalizada = models.DateField(blank=True, null=True,verbose_name='Finalizada')

    class Meta:
        db_table = 'detalles_practica'
        verbose_name = 'Detalle Práctica'
        verbose_name_plural = 'Detalle Prácticas'


class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(primary_key=True, null=False)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre    
    
    class Meta:
        db_table = 'diagnostico'
        verbose_name_plural = 'Diagnósticos'

class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'especialidad'
        verbose_name_plural = 'Especialidades'


class HorariosAtencion(models.Model):
    id_horarios_atencion = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=10,choices= dia, default='Lunes',verbose_name='Día')
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
    id_institucion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    direccion = models.CharField(max_length=50)
    departamento = models.CharField(max_length=25)
    mail = models.CharField(max_length=40)
    telefono = models.BigIntegerField()
    obras_sociales = models.ManyToManyField('ObraSocial', through='Institucion_Obra_Social',verbose_name= 'Obras sociales que acepta')
    horarios = models.ManyToManyField('HorariosAtencion', through='Institucion_Horarios')
    practicas = models.ManyToManyField('Practica', through='Practica_Institucion',verbose_name= 'Prácticas que realiza')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'institucion'
        verbose_name_plural = 'Instituciones'



class Medico(models.Model):
    id_medico = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # No es nulo porque se lo asignamos nosotros directamente
    nombre = models.CharField(max_length=25,verbose_name='Nombre')
    apellido = models.CharField(max_length=25,verbose_name='Apellido')
    direccion = models.CharField(max_length=50,verbose_name='Dirección')
    departamento = models.CharField(max_length=25,verbose_name='Departamento')
    mail = models.CharField(max_length=40,verbose_name='Mail')
    telefono = models.BigIntegerField(verbose_name='Teléfono')
    genero = models.CharField(max_length=1,choices= genero, default='X',verbose_name='Género')
    matriculaprovincial = models.IntegerField(verbose_name='M.P.')
    nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    id_especialidad = models.ForeignKey('Especialidad', null=False, on_delete=models.CASCADE, db_column='id_especialidad',verbose_name='Especialidad')
    obras_sociales = models.ManyToManyField('ObraSocial', through='Medico_ObraSocial', through_fields=("id_medico", "id_obra_social"),verbose_name='Obras Sociales que atiende')
    rating = models.SmallIntegerField(blank=True, null=True,verbose_name='Rating')
    practicas = models.ManyToManyField('Practica', through='Medico_Practica',verbose_name='Prácticas que realiza')
    # id_agenda = models.IntegerField(blank=True,null=True,verbose_name='Número de Agenda')
    pacientes = models.ManyToManyField('Paciente', through='Medico_Paciente',verbose_name='Pacientes que atiende')


    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre, self.apellido)
    
    class Meta:
        db_table = 'medico'


class ObraSocial(models.Model):
    id_obra_social = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    instituciones = models.ManyToManyField('Institucion', through='Institucion_Obra_Social')
    medicos = models.ManyToManyField('Medico', through='Medico_ObraSocial')
    practicas = models.ManyToManyField('Practica', through='Obra_Social_Practica',verbose_name='Prácticas que cubre')

    class Meta:
        db_table = 'obra_social'
        verbose_name_plural = 'Obra Sociales'

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,verbose_name='Usuario') # Debe ser nulo porque se crea una instancia de paciente y despues le asignamos un usuario creado
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    dni = models.IntegerField(unique=True)
    direccion = models.CharField(max_length=50)
    departamento = models.CharField(max_length=25)
    mail = models.CharField(max_length=40)
    password = models.CharField(max_length=25, null=True, blank=True,verbose_name='Contraseña')
    telefono = models.BigIntegerField()
    genero = models.CharField(max_length=1,choices= genero, default='X',verbose_name='Género')
    nacimiento = models.DateField()
    numero_afiliado = models.BigIntegerField(blank=True, null=True)
    id_obra_social = models.ForeignKey('ObraSocial', blank=True, null=True, on_delete=models.CASCADE, db_column='id_obra_social',verbose_name='Obra Social')
    # id_historia_clinica = models.IntegerField(blank=True,null=True)
    medicos = models.ManyToManyField('Medico', through='Medico_Paciente',verbose_name='Médico con quien se atiende')
    

    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre, self.apellido)
    
    class Meta:
        db_table = 'paciente'


class Practica(models.Model):
    id_practica = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()
    instituciones = models.ManyToManyField('Institucion', through='Practica_Institucion')
    medicos = models.ManyToManyField('Medico', through='Medico_Practica')
    obras_sociales = models.ManyToManyField('ObraSocial', through='Obra_Social_Practica')
    recomendacion = models.CharField(max_length=150, blank=True, null=True, verbose_name= 'Recomendación')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'practica'
        verbose_name = 'Práctica'
        verbose_name_plural = 'Prácticas'


#   MODELOS RELACIONALES

class Institucion_Horarios(models.Model):
    id_institucion_horarios = models.AutoField(primary_key=True,verbose_name='ID_Horarios')
    id_institucion = models.ForeignKey('Institucion', null=False, on_delete=models.CASCADE, db_column='id_institucion',verbose_name='Institucion')
    id_horarios_atencion = models.ForeignKey('HorariosAtencion', null=False, on_delete=models.CASCADE, db_column='id_horarios_atencion',verbose_name='')

    class Meta:
        db_table = 'institucion_horarios'
        unique_together = (('id_institucion', 'id_horarios_atencion'),)
        verbose_name_plural = 'Horarios de atención'
        verbose_name = 'Horario de atención'

    def __str__(self):
        return ""

class Institucion_Obra_Social(models.Model):
    id_institucion_obra_social = models.AutoField(primary_key=True,verbose_name='Obra sociales que acepta')
    id_institucion = models.ForeignKey('Institucion', null=False, on_delete=models.CASCADE, db_column='id_institucion',verbose_name='Instituciones')
    id_obra_social = models.ForeignKey('ObraSocial', null=False, on_delete=models.CASCADE, db_column='id_obra_social',verbose_name='Obras sociales')

    class Meta:
        db_table = 'institucion_obra_social'
        unique_together = (('id_institucion', 'id_obra_social'),)
        verbose_name = 'Obra Social / Institución'
        verbose_name_plural = 'Obras social / Institución'
    
    def __str__(self):
        return ""

class Medico_ObraSocial(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='Obra sociales que acepta')
    id_medico = models.ForeignKey('Medico', on_delete=models.CASCADE, related_name='obras_sociales_rel')
    id_obra_social = models.ForeignKey('ObraSocial', on_delete=models.CASCADE,verbose_name='Obra sociales')

    class Meta:
        db_table = 'medico_obra_social'
        unique_together = (('id_medico', 'id_obra_social'),)
        verbose_name = 'Obra Social'
        verbose_name_plural = 'Obras sociales que acepta'
    
    def __str__(self):
        return ""
        
class Medico_Paciente(models.Model):
    id_medico_paciente = models.AutoField(primary_key=True)
    id_medico = models.ForeignKey('Medico', null=False, on_delete=models.CASCADE, db_column='id_medico',verbose_name='Médicos con quien se atiende')
    id_paciente = models.ForeignKey('Paciente', null=False, on_delete=models.CASCADE, db_column='id_paciente', verbose_name='Pacientes que atiende')

    def __str__(self):
        return ""
    
    class Meta:
        db_table = 'medico_paciente'
        unique_together = (('id_medico', 'id_paciente'),)
        verbose_name = 'Paciente/Medico'
        verbose_name_plural = 'Pacientes/Medicos'

class Medico_Practica(models.Model):
    id_medico_practica = models.AutoField(primary_key=True,verbose_name='Práctica que realiza')
    id_medico = models.ForeignKey('Medico', null=False, on_delete=models.CASCADE, db_column='id_medico')
    id_practica = models.ForeignKey('Practica', null=False, on_delete=models.CASCADE, db_column='id_practica',verbose_name='Práctica')

    class Meta:
        db_table = 'medico_practica'
        unique_together = (('id_medico', 'id_practica'),)
        verbose_name = 'Práctica'
        verbose_name_plural = 'Prácticas que realiza'
    
    def __str__(self):
        return ""

class Obra_Social_Practica(models.Model):
    id_obra_social_practica = models.AutoField(primary_key=True)
    id_obra_social = models.ForeignKey('ObraSocial', null=False, on_delete=models.CASCADE, db_column='id_obra_social')
    id_practica = models.ForeignKey('Practica', null=False, on_delete=models.CASCADE, db_column='id_practica',verbose_name='Práctica')

    class Meta:
        db_table = 'obra_social_practica'
        unique_together = (('id_obra_social', 'id_practica'),)
        verbose_name = 'Práctica'
        verbose_name_plural = 'Prácticas que realiza'

    def __str__(self):
        return ""

class Practica_Institucion(models.Model):
    id_pract_inst = models.AutoField(primary_key=True,verbose_name='Práctica que realiza')
    id_practica = models.ForeignKey('Practica', null=False, on_delete=models.CASCADE,
                                         db_column='id_practica',verbose_name='Práctica')
    id_institucion = models.ForeignKey('Institucion', null=False, on_delete=models.CASCADE,
                                         db_column='id_institucion')

    class Meta:
        db_table = 'practica_institucion'
        unique_together = (('id_practica', 'id_institucion'),)
        verbose_name = 'Práctica'
        verbose_name_plural = 'Prácticas que realiza'
    
    def __str__(self):
        return ""
