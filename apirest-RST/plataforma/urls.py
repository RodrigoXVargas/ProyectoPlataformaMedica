from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from .views import DireccionViewSet, PacienteViewSet, ObraSocialViewSet, MedicoViewSet, EspecialidadViewSet


#Urls de la api
router = routers.DefaultRouter()
""" router.register(r'usuarios', UsuarioViewSet) """
router.register(r'pacientes', PacienteViewSet)
router.register(r'direcciones', DireccionViewSet)
router.register(r'obrasociales', ObraSocialViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'especialidades', EspecialidadViewSet)


urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


urlpatterns += router.urls