
import numpy as np
from keras.models import load_model
import os

# Load the FaceNet model
def load_facenet_model():
    model_path = os.path.join('models', 'facenet_keras.h5')
    model = load_model(model_path)
    print("Modelo FaceNet cargado desde", model_path)
    return model

# Obtener el embedding de una cara
def get_face_embedding(model, face_pixels):
    face_pixels = face_pixels.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    yhat = model.predict(samples)
    return yhat[0]

# Guardar embeddings en un archivo .npy
def save_embedding(embedding, filename):
    filepath = os.path.join('embeddings', filename)
    np.save(filepath, embedding)
    print(f"Embeddings guardados en {filepath}")
