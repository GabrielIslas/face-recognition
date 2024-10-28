
import cv2
import os
from mtcnn import MTCNN
from facenet_model import load_facenet_model, get_face_embedding, save_embedding
from utils import preprocess_image, save_face_image

# Inicializar el modelo FaceNet
facenet_model = load_facenet_model()

# Cargar una imagen de ejemplo
image_path = 'data/raw/sample_image.jpg'
image = preprocess_image(image_path)

# Detectar las caras con MTCNN
detector = MTCNN()
faces = detector.detect_faces(image)

# Procesar cada cara detectada
for i, face in enumerate(faces):
    x, y, width, height = face['box']
    face_region = image[y:y+height, x:x+width]
    
    # Guardar la imagen de la cara detectada
    face_filename = f"face_{i}.jpg"
    save_face_image(face_region, face_filename)

    # Obtener los embeddings de la cara
    embedding = get_face_embedding(facenet_model, face_region)
    
    # Guardar los embeddings
    embedding_filename = f"embedding_{i}.npy"
    save_embedding(embedding, embedding_filename)
