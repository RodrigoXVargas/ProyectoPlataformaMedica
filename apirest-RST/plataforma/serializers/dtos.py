from rest_framework import serializers
from ..models import Paciente, ObraSocial

class ObraSocialDTOSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraSocial
        fields = ['nombre',] 
        
class PacienteDTOSerializer(serializers.ModelSerializer):
    id_obra_social = ObraSocialDTOSerializer()
    
    class Meta:
        model = Paciente
        fields = ['id_obra_social', ]
        
