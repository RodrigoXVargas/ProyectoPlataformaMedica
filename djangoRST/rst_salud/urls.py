# URLS DE LAS VISTAS DE LA APP "rst_salud"

from django.urls import path

from .views import *


urlpatterns = [
    # Home
    path('', index, name='index'),
    # Registro pacientes
    path('pacientes/registro/', PacienteRegistroView.as_view(), name='registro_paciente'),
    # Login medicos
    path('login/medicos/', LoginMedicoView.as_view(), name='login_medico'),
    # Login pacientes
    path('login/pacientes/', LoginPacienteView.as_view(), name='login_paciente'),
    # Log out
    path('logout/', Logout.as_view(), name='logout'),
    # Medicos interfaz
    path('medicos/<str:nombre>/', detalle_medico, name='detalle_medico'),
    # Pacientes interfaz
    path('pacientes/<str:nombre>/', detalle_paciente, name='detalle_paciente'),
    # # Tesseract
    # path('cargar_imagen/', cargar_imagen_y_procesar, name='cargar_imagen'),
] 