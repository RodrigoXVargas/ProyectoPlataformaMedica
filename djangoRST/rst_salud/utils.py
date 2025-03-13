# # FUNCIONES PARA PROCESAMIENTO DE IMÁGENES (PEDIDOS MÉDICOS) CON TESSERACT

# import io
# import os
# import pytesseract
# from PIL import Image
# from django.conf import settings
# from django.db.models import Q
# from .models import Practica, DetallesPractica
# import uuid

# # Guarda la imagen en el directorio de medios y devuelve la ruta.
# def save_image_and_get_path(image):
#     media_root = settings.MEDIA_ROOT
#     image_dir = os.path.join(media_root, 'uploaded_images')

#     # Verifica que el directorio exista, si no, lo crea
#     if not os.path.exists(image_dir):
#         os.makedirs(image_dir)

#     # Genera un nombre de archivo único para la imagen
#     image_name = f"uploaded_image_{uuid.uuid4().hex}.png"
#     image_path = os.path.join(image_dir, image_name)

#     # Guarda la imagen en el directorio de medios
#     image.save(image_path)

#     return image_path

# # Toma directamente una instancia de imagen como entrada y realiza la lectura OCR utilizando Tesseract.
# def read_image_with_tesseract(image):
#     try:
#         # Obtener el texto
#         text = pytesseract.image_to_string(image)
#         print(f"Texto extraído: {text}")
#         return text.strip()
#     except Exception as e:
#         print(f"Error en la lectura OCR: {str(e)}")
#         return None

# # Abre un archivo de imagen, lo convierte en un objeto Image y luego realiza la lectura OCR utilizando la función anterior.
# def process_image_and_get_text(image):
#     # Crea una instancia de la clase Image desde el contenido del archivo
#     image_content = Image.open(io.BytesIO(image.read()))

#     # Realiza el procesamiento OCR con Tesseract
#     ocr_result = read_image_with_tesseract(image_content)

#     return ocr_result

# """
# En referencia a las funciones anteriores:
# La separación en dos funciones permite una modularidad y reutilización del código, ya que la función read_image_with_tesseract podría ser utilizada en otros contextos si es necesario realizar OCR directamente en una imagen sin tener que abrir un archivo de imagen.
# """

# # Función para procesar el texto y comparar con Practicas en la base de datos
# def procesar_texto_y_comparar(texto):
#     # Buscar coincidencias en Practicas
#     practicas_coincidentes = Practica.objects.filter(
#         Q(nombre__icontains=texto) | Q(descripcion__icontains=texto)
#     )

#     return practicas_coincidentes

# # Función para crear un nuevo DetallePractica con la Practica coincidente
# def crear_detalle_practica(practica_coincidente, paciente_id, medico_id, institucion_id, diagnostico_id, fecha_generada):
#     try:
#         # Crea un nuevo DetallePractica
#         detalle_practica = DetallesPractica.objects.create(
#             id_paciente_id=paciente_id,
#             id_medico_id=medico_id,
#             id_institucion_id=institucion_id,
#             id_practica_id=practica_coincidente.id_practica,
#             id_diagnostico_id=diagnostico_id,
#             fecha_generada=fecha_generada,
#         )

#         return detalle_practica
#     except Exception as e:
#         print(f"Error al crear DetallePractica: {str(e)}")
#         return None
