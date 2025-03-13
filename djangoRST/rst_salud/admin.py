from django.contrib import admin
from .models import  Especialidad, Institucion, Medico, ObraSocial, Paciente, Practica, Practica_Institucion, Institucion_Obra_Social, Medico_Practica, Medico_ObraSocial, Medico_Paciente, HorariosAtencion, Institucion_Horarios, Diagnostico, Obra_Social_Practica, DetallesPractica
from .forms import DiagnosticoForm, EspecialidadForm, InstitucionForm, MedicoForm, ObraSocialForm, PacienteForm, PracticaForm
from django.utils.safestring import mark_safe #FUNCION PARA PODER MOSTRAR ELEMENTOS UNO DEBAJO DEL OTRO 


# Modelos "inline" que se utilizarán en la interfaz de administración para gestionar relaciones.

class Institucion_Obra_Social_inline(admin.TabularInline):
    model = Institucion_Obra_Social
    extra = 0

class HorariosAtencion_inline(admin.TabularInline):
    model = HorariosAtencion
    extra = 0

class Institucion_Horacios_inline(admin.TabularInline):
    model = Institucion_Horarios
    extra = 0
    fields = ('id_horarios_atencion',)

class Practica_Institucion_inline(admin.TabularInline):
    model = Practica_Institucion
    extra = 0

class Obra_Social_Practica_inline(admin.TabularInline):
    model = Obra_Social_Practica
    extra = 0

class Medico_Practica_inline(admin.TabularInline):
    model = Medico_Practica
    extra = 0

class Medico_Paciente_inline(admin.TabularInline):
    model = Medico_Paciente
    extra = 0

class Medico_ObraSocial_inline(admin.TabularInline):
    model = Medico_ObraSocial
    extra = 0

# Configuración de la interfaz de administración para cada modelo.

class DetallesPracticaAdmin(admin.ModelAdmin):
    list_display = ('id_detalles_practica','id_paciente','id_medico','id_institucion','id_practica','id_diagnostico','fecha_generada','fecha_finalizada')
    search_fields = ('id_detalles_practica','id_paciente__nombre','id_medico__nombre','id_institucion__nombre','id_practica__nombre','id_diagnostico__nombre','fecha_generada','fecha_finalizada') # PORQUE COLUMNAS SE VA A PODER BUSCAR

class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',) # PORQUE COLUMNAS SE VA A PODER BUSCAR
    form = DiagnosticoForm

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',) # PORQUE COLUMNAS SE VA A PODER BUSCAR
    form = EspecialidadForm

class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre','direccion','departamento','mail','telefono','mostrar_obrassociales','mostrar_horarios','mostrar_practicas')
    search_fields = ('nombre','direccion','departamento','mail','telefono','practicas__nombre','obras_sociales__nombre','horarios__dia')
    form = InstitucionForm
    inlines = [Institucion_Horacios_inline, Practica_Institucion_inline,Institucion_Obra_Social_inline]

    def mostrar_obrassociales(self,obj):
        obras = [str(obras_sociales) for obras_sociales in obj.obras_sociales.all()]
        return mark_safe("<br>".join(obras))
    mostrar_obrassociales.short_description = 'O.S. que atiende' # CAMBIA EL ENCABEZADO DE LA COLUMNA

    def mostrar_horarios(self,obj):
        horarioss = [str(horarios) for horarios in obj.horarios.all()]
        return mark_safe("<br>".join(horarioss))
    mostrar_horarios.short_description = 'Horarios que atiende' # CAMBIA EL ENCABEZADO DE LA COLUMNA

    def mostrar_practicas(self,obj):
        practicass = [str(practicas) for practicas in obj.practicas.all()]
        return mark_safe("<br>".join(practicass))
    mostrar_practicas.short_description = 'Practicas que realiza' # CAMBIA EL ENCABEZADO DE LA COLUMNA

class MedicoAdmin(admin.ModelAdmin):
    #filter_horizontal = ('obras_sociales',)
    list_display = ('nombre','apellido', 'user','id_especialidad','matriculaprovincial','mostrar_obrassociales','mostrar_practicas','mostrar_pacientes','direccion','departamento','mail','telefono') #QUE COLUMNAS VA A MOSTRAR DE CADA REGISTRO
    form = MedicoForm
    ordering = ('nombre','apellido','id_especialidad','matriculaprovincial','genero','direccion','departamento','mail','telefono') # POR QUE COLUMNA VA A ORDENAR 
    search_fields = ('nombre','apellido','matriculaprovincial','genero','direccion','departamento','mail','telefono','practicas__nombre','obras_sociales__nombre','pacientes__nombre') # PORQUE COLUMNAS SE VA A PODER BUSCAR
    #list_editable = ('nombre',) # QUE PARAMETRO SE PUEDE EDITAR
    #list_display_links = ('id_especialidad',) # MUESTRA UN HIPERVINCULO QUE REDIRIJE AL FORMULARIO PARA EDITARLO
    list_filter = ('id_especialidad',) # CREA UN FILTRO POR EL PARAMETRO QUE SE COLOQUE
    list_per_page = 10 # MUESTRA UN NUMERO INDICADO DE REGISTROS POR PAGINA
    #exclude =  (('id_medico','nombre'),) # EXCLUYE CIERTOS ATRIBUTOS PARA QUE NO PUEDAN SER EDITABLES
    inlines = [Medico_Practica_inline,Medico_ObraSocial_inline,Medico_Paciente_inline]

    def mostrar_obrassociales(self,obj):
        obras = [str(obras_sociales) for obras_sociales in obj.obras_sociales.all()]
        return mark_safe("<br>".join(obras))
    mostrar_obrassociales.short_description = 'O.S. que atiende' # CAMBIA EL ENCABEZADO DE LA COLUMNA

    def mostrar_practicas(self,obj):
        practicass = [str(practicas) for practicas in obj.practicas.all()]
        return mark_safe("<br>".join(practicass))
    mostrar_practicas.short_description = 'Practicas que realiza' # CAMBIA EL ENCABEZADO DE LA COLUMNA

    def mostrar_pacientes(self,obj):
        pacientess = [str(pacientes) for pacientes in obj.pacientes.all()]
        return mark_safe("<br>".join(pacientess))
    mostrar_pacientes.short_description = 'Pacientes que atiende' # CAMBIA EL ENCABEZADO DE LA COLUMNA

class ObraSocialAdmin(admin.ModelAdmin):
    list_display = ('nombre','mostrar_practicas','mostrar_instituciones')
    search_fields = ('nombre','practicas__nombre','instituciones__nombre')
    form = ObraSocialForm
    inlines = [Obra_Social_Practica_inline,Institucion_Obra_Social_inline]

    def mostrar_practicas(self,obj):
        practicass = [str(practicas) for practicas in obj.practicas.all()]
        return mark_safe("<br>".join(practicass))
    mostrar_practicas.short_description = 'Practicas que cubre' # CAMBIA EL ENCABEZADO DE LA COLUMNA

    def mostrar_instituciones(self,obj):
        institucioness = [str(instituciones) for instituciones in obj.instituciones.all()]
        return mark_safe("<br>".join(institucioness))
    mostrar_instituciones.short_description = 'Instituciones que la reciben' # CAMBIA EL ENCABEZADO DE LA COLUMNA

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellido', 'user','dni','direccion','departamento','mail','genero','nacimiento','numero_afiliado','id_obra_social','mostrar_medicos')
    search_fields = ('nombre','apellido','dni','direccion','departamento','mail','numero_afiliado','id_obra_social__nombre','medicos__nombre','medicos__apellido')
    form = PacienteForm
    inlines = [Medico_Paciente_inline]
    
    def mostrar_medicos(self,obj):
        medicoss = [str(medicos) for medicos in obj.medicos.all()]
        return mark_safe("<br>".join(medicoss))
    mostrar_medicos.short_description = 'Médicos con quién se atiende' # CAMBIA EL ENCABEZADO DE LA COLUMNA

class PracticaAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion','precio','recomendacion','mostrar_instituciones','mostrar_obrassociales','mostrar_medicos')
    search_fields = ('nombre','descripcion','precio','recomendacion','instituciones__nombre','obras_sociales__nombre','medicos__nombre','medicos__apellido')
    form = PracticaForm

    def mostrar_instituciones(self,obj):
        institucioness = [str(instituciones) for instituciones in obj.instituciones.all()]
        return mark_safe("<br>".join(institucioness))
    mostrar_instituciones.short_description = 'Instituciones que la realizan' # CAMBIA EL ENCABEZADO DE LA COLUMNA

    def mostrar_obrassociales(self,obj):
        obras = [str(obras_sociales) for obras_sociales in obj.obras_sociales.all()]
        return mark_safe("<br>".join(obras))
    mostrar_obrassociales.short_description = 'O.S. que la cubren' # CAMBIA EL ENCABEZADO DE LA COLUMNA

    def mostrar_medicos(self,obj):
        medicoss = [str(medicos) for medicos in obj.medicos.all()]
        return mark_safe("<br>".join(medicoss))
    mostrar_medicos.short_description = 'Médicos con la realizan' # CAMBIA EL ENCABEZADO DE LA COLUMNA

# Registro de los modelos y las configuraciones de administración en el sitio de administración.

admin.site.register(Diagnostico,DiagnosticoAdmin)
admin.site.register(Especialidad,EspecialidadAdmin)
admin.site.register(Institucion,InstitucionAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(ObraSocial, ObraSocialAdmin)
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(Practica,PracticaAdmin)
admin.site.register(DetallesPractica,DetallesPracticaAdmin)
