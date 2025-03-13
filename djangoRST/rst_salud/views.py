from .models import *
from .serializers import *
from .forms import *
from .utils import *
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
# Imports para Tesseract
# from datetime import date
# from django.http import JsonResponse

# REGISTRO PACIENTE
@permission_classes([AllowAny]) # AllowAny es para probar, ya que no podemos manejar los tokens en las peticiones si no es con Postman.
# Esta vista registra un nuevo paciente mediante un formulario y crea un usuario en base a los datos ingresados.
class PacienteRegistroView(View):
    template_name = 'registro_paciente.html'

    # Formulario para que llene el paciente (no lo deja elegir un tipo de usuario aunque paciente tiene un campo de tipo usuario)
    def get(self, request, *args, **kwargs):
        form = PacienteRegistroForm()
        return render(request, self.template_name, {'form': form})
    
    # Una vez llenado el formulario se verifican los datos, se crea el usuario aparte y se le asigna al paciente.
    def post(self, request, *args, **kwargs):
        form = PacienteRegistroForm(request.POST)
        if form.is_valid():
            # Crea el usuario con los campos del paciente
            user = get_user_model().objects.create_user(
                username=form.cleaned_data['nombre'].lower(),
                password=form.cleaned_data['password'],
                email=form.cleaned_data['mail']
            )
            
            # Asigna al usuario al grupo "Pacientes"
            grupo_pacientes, creado = Group.objects.get_or_create(name='Pacientes')
            user.groups.add(grupo_pacientes)

            # Crea el paciente asociado al usuario
            paciente = Paciente.objects.create(
                user=user,
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                dni=form.cleaned_data['dni'],
                direccion=form.cleaned_data['direccion'],
                departamento=form.cleaned_data['departamento'],
                mail=form.cleaned_data['mail'],
                password=form.cleaned_data['password'],
                telefono=form.cleaned_data['telefono'],
                genero=form.cleaned_data['genero'],
                nacimiento=form.cleaned_data['nacimiento'],
                numero_afiliado=form.cleaned_data['numero_afiliado'],
                id_obra_social=form.cleaned_data['id_obra_social'],
            )

            # Lógica para agregar la lista de medicos a paciente
            medicos_seleccionados = form.cleaned_data['medicos']  
            for medico in medicos_seleccionados:
                paciente.medicos.add(medico)

            paciente.save()

            return redirect('detalle_paciente', nombre=user.username)  # Redireccionamos a la vista del paciente

        return render(request, self.template_name, {'form': form})

"""
LOGIN
Se presentan 2 vistas distintas: una para iniciar sesión como médico, y otra para hacerlo como paciente. Esto es muy común en la mayoría de las webs de salud analizadas.
"""
# LOGIN MEDICO
class LoginMedicoView(View):
    # Renderiza el formulario para llenarlo
    def get(self, request):
        return render(request, 'login_medico.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        # Autentica al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name='Medicos').exists():
            # Inicia sesión
            login(request, user)

            # Redirige a la vista protegida para el usuario autenticado
            return redirect('detalle_medico', nombre = username)

        else:
            # Si la autenticación falla, maneja el error o redirige a otra vista
            return render(request, 'login_medico.html', {'error_message': 'Usuario o contraseña incorrectos'})

# LOGIN PACIENTE
class LoginPacienteView(View):
    def get(self, request):
        return render(request, 'login_paciente.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name='Pacientes').exists():
            login(request, user)

            return redirect('detalle_paciente', nombre=username)

        else:
            return render(request, 'login_paciente.html', {'error_message': 'Usuario o contraseña incorrectos'})

"""
REVISAR: Si el usuario está registrado pero no se le asignó ningún grupo, igual puede acceder a la vista. Ej.: Si se registra a un médico y se le crea un usuario nuevo, que no tiene asignado grupo, puede acceder a la vista detalle_medico de todas maneras. Esto se debe cambiar.
"""

# Las siguientes vistas renderizan todos los datos del médico/paciente guardados en la DB y los muestran en el html. En un futuro se pueden cambiar para que muestren los datos que sean necesarios para el médico/paciente.
def detalle_medico(request, nombre):
    medico = get_object_or_404(Medico, user__username=nombre)
    
    # Obtén los campos del modelo y sus valores
    campos_medico = {field.verbose_name: getattr(medico, field.name) for field in medico._meta.fields}
    
    return render(request, 'medico_detalle.html', {'medico': medico, 'campos_medico': campos_medico})

def detalle_paciente(request, nombre):
    paciente = get_object_or_404(Paciente, user__username=nombre)
    
    campos_paciente = {field.verbose_name: getattr(paciente, field.name) for field in paciente._meta.fields}
    
    return render(request, 'paciente_detalle.html', {'paciente': paciente, 'campos_paciente': campos_paciente})

# LOG OUT
# Cuando se ingresa a esta vista, enviando por metodo POST el access token y refresh token, le da de baja al token actual, colocandolo en la blacklist de la DB.
@permission_classes([AllowAny]) 
class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# INDEX
# Renderiza la página principal de la plataforma, donde se ven los botones para iniciar sesión como medico o paciente, y registrarse como paciente.
def index(request):
    return render(request, 'index.html')

"""
# PROCESAMIENTO DE IMÁGENES CON TESSERACT
def cargar_imagen_y_procesar(request):
    if request.method == 'POST' and request.FILES['imagen']:
        imagen = request.FILES['imagen']

        try:
            # Procesa la imagen y obtiene el texto mediante OCR
            texto_ocr = process_image_and_get_text(imagen)

            if texto_ocr:
                # Procesa el texto y obtiene prácticas coincidentes
                practicas_coincidentes = procesar_texto_y_comparar(texto_ocr)

                if practicas_coincidentes:
                    # Supongamos que tenemos un paciente, medico, institucion, y diagnostico ya existentes (más adelante hay que hacer el mismo proceso de buscar prácticas coincidentes con médico y diagnóstico. A paciente se le asignaría el mismo que está logueado, y la institución que elija el usuario).
                    paciente = Paciente.objects.get(pk=1)
                    medico = Medico.objects.get(pk=1)
                    institucion = Institucion.objects.get(pk=1)
                    diagnostico = Diagnostico.objects.get(pk=1)
                    # Crea un nuevo DetallePractica con la primera práctica coincidente
                    nueva_practica = practicas_coincidentes[0]
                    fecha_generada = date.today()
                    nuevo_detalle_practica = crear_detalle_practica(
                        nueva_practica, paciente.id_paciente, medico.id_medico, institucion.id_institucion, diagnostico.id_diagnostico, fecha_generada
                    )

                    if nuevo_detalle_practica:
                        # El detalle de la práctica se creó con éxito (luego modificar por una redirección a alguna vista).
                        return JsonResponse({'success': True, 'message': 'Detalle de practica creado con exito'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Error al crear el detalle de la practica'})

                else:
                    return JsonResponse({'success': False, 'message': 'No se encontraron practicas coincidentes'})

            else:
                return JsonResponse({'success': False, 'message': 'Error en la lectura OCR'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    return render(request, 'procesar_imagen.html')
"""
