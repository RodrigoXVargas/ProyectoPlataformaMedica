from django import forms
from .models import Diagnostico, Especialidad, Institucion, Medico, ObraSocial, Paciente, Practica, HorariosAtencion, Institucion_Horarios

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = '__all__'

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = '__all__'

class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = '__all__'

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ('nombre', 'apellido', 'user','direccion', 'departamento', 'mail', 'telefono', 'genero', 'matriculaprovincial', 'nacimiento', 'id_especialidad', 'obras_sociales', 'practicas', 'rating')

class ObraSocialForm(forms.ModelForm):
    class Meta:
        model = ObraSocial
        fields = ('nombre', 'practicas')

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

class PacienteRegistroForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ('nombre', 'apellido', 'dni', 'direccion','departamento' , 'mail', 'password', 'telefono', 'genero', 'nacimiento', 'numero_afiliado', 'id_obra_social', 'medicos')

class PracticaForm(forms.ModelForm):
    class Meta:
        model = Practica
        fields = '__all__'

class HorariosAtencionForm(forms.ModelForm):
    class Meta:
        model = HorariosAtencion
        fields = '__all__'

class Institucion_HorariosForm(forms.ModelForm):
    class Meta:
        model = Institucion_Horarios
        fields = '__all__'