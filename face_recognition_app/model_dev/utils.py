
import cv2
import os

# Preprocesar imagen (redimensionar y convertir a RGB)
def preprocess_image(image_path, target_size=(160, 160)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, target_size)
    return image

# Guardar una imagen de cara detectada
def save_face_image(face_image, filename):
    output_path = os.path.join('data', 'processed', filename)
    cv2.imwrite(output_path, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))
    print(f"Imagen de la cara guardada en {output_path}")
