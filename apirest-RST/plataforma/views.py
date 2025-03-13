from rest_framework import viewsets, permissions
from .serializers.serializers import DireccionSerializer, PacienteSerializer, ObraSocialSerializer, MedicoSerializer, EspecialidadSerializer
from .models import Direccion, Paciente, ObraSocial, Medico, Especialidad

class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    permission_classes = [permissions.AllowAny]
    
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.AllowAny]
    
class ObraSocialViewSet(viewsets.ModelViewSet):
    queryset = ObraSocial.objects.all()
    serializer_class = ObraSocialSerializer
    permission_classes = [permissions.AllowAny]
    
class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [permissions.AllowAny]
    
class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [permissions.AllowAny]