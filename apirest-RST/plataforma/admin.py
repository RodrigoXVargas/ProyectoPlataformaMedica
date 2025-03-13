from django.contrib import admin
from .models import Direccion, Paciente, ObraSocial, Medico, Especialidad, Usuario

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    #Eliminé id así lo subia funcionando al github
    fields = ('id', 'first_name', 'last_name', 'username', 'password', 'dni', 'telefono','date_joined', 'email', 'is_active', 'fecha_nacimiento', 'perfil_image')
    ordering= ['last_name', ]
    readonly_fields = ['id', 'date_joined']
    
class PacienteAdmin(admin.ModelAdmin):
    fields = ('usuario', 'numero_afiliado', 'id_obra_social', 'apoderado', 'medicos')
    #list_display = ['last_name', 'first_name', 'dni', 'id_obra_social']
    #list_filter = ['date_joined', 'medicos']
    
    readonly_fields = ['id']
    
class DireccionAdmin(admin.ModelAdmin):
    #list_display = [ 'calle', 'numeracion', 'id_departamento', 'id_provincia', 'id_usuario']
    list_filter = ['id_departamento', 'id_provincia']
    search_fields = ['id_usuario__username',]
    ordering= ['id_provincia',]
    
class ObraSocialAdmin(admin.ModelAdmin):
    list_display = [ 'nombre',]
    list_filter = [ 'nombre',]
    search_fields = [ 'nombre',]
    ordering= [ 'id',]
    
class MedicoAdmin(admin.ModelAdmin):
    fields = ['usuario', 'num_matricula', 'obras_sociales', 'rating', 'pacientes']
    ordering= [ 'id',]
    
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = [ 'nombre',]
    list_filter = [ 'nombre',]
    search_fields = [ 'nombre',]
    ordering= [ 'id',]

# Register your models here.
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(ObraSocial, ObraSocialAdmin)
admin.site.register(Direccion, DireccionAdmin)

