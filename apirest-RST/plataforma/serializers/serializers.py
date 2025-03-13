# SERIALIZADORES (desarrollo de APIs REST con Django Rest Framework)

from rest_framework import serializers
from ..models import Usuario
from ..models import Usuario, Direccion, Paciente, ObraSocial, Medico,  Especialidad
from .dtos import PacienteDTOSerializer, ObraSocialDTOSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'dni', 'telefono', 'date_joined', 'email', 'is_active', 'fecha_nacimiento', 'perfil_image',]
        read_only_fields = ['date_joined', ]

        # SERIALIZADORES (desarrollo de APIs REST con Django Rest Framework)


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    apoderado = PacienteDTOSerializer()
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Paciente
        fields = ['usuario', 'numero_afiliado', 'id_obra_social', 'apoderado', 'medicos', ]
        

class ObraSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraSocial
        fields = '__all__'   
        

class MedicoSerializer(serializers.ModelSerializer):
    pacientes = PacienteDTOSerializer(many=True)
    obras_sociales = ObraSocialDTOSerializer(many=True)
    usuario = UsuarioSerializer()

    class Meta:
        model = Medico
        fields = [ 'usuario', 'num_matricula', 'obras_sociales', 'rating', 'pacientes', ]

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'