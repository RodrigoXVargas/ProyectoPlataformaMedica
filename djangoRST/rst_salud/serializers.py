# SERIALIZADORES (desarrollo de APIs REST con Django Rest Framework)

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# RELACIONES MEDICO

class Medico_ObraSocialSerializer(serializers.ModelSerializer):
    obrasocial = serializers.ReadOnlyField(source='obrasocial.id_obra_social')

    class Meta:
        model = Medico_ObraSocial
        fields = '__all__'

class Medico_PracticasSerializer(serializers.ModelSerializer):
    practica = serializers.ReadOnlyField(source='practica.id_practica')

    class Meta:
        model = Medico_Practica
        fields = '__all__'

class Medico_PacienteSerializer(serializers.ModelSerializer):
    paciente = serializers.ReadOnlyField(source='paciente.id_paciente')

    class Meta:
        model = Medico_Paciente
        fields = '__all__'

# RELACIONES OBRA SOCIAL

class ObraSocial_PracticaSerializer(serializers.ModelSerializer):
    practica = serializers.ReadOnlyField(source='practica.id_practica')

    class Meta:
        model = Obra_Social_Practica
        fields = '__all__'

# RELACIONES INSTITUCION

class Institucion_HorariosSerializer(serializers.ModelSerializer):
    horarios = serializers.ReadOnlyField(source='horarios.id_horarios_atencion')

    class Meta:
        model = Institucion_Horarios
        fields = '__all__'

class Institucion_Obra_SocialSerializer(serializers.ModelSerializer):
    obrasocial = serializers.ReadOnlyField(source='obrasocial.id_obra_social')

    class Meta:
        model = Institucion_Obra_Social
        fields = '__all__'

class Intitucion_PracticaSerializer(serializers.ModelSerializer):
    practica = serializers.ReadOnlyField(source='practica.id_practica')

    class Meta:
        model = Practica_Institucion
        fields = '__all__'


# MODELOS

class DetallesPracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallesPractica
        fields = '__all__'


class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = '__all__'


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'


class HorariosAtencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorariosAtencion
        fields = '__all__'


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = '__all__'


class ObraSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraSocial
        fields = '__all__'


class MedicoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Medico
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Paciente
        fields = '__all__'


class PracticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practica
        fields = '__all__'
