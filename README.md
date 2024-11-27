# Face Recognition App
Developed by Cesar Correa, Christian Can, Gabriel Islas, Mariano Miranda, and Juan Tec
This repository contains the files for a web application used to take attendance in class through a face recognition model.
The webpage was done using Streamlit, the facenet model was trained using the keras-facenet library and then hosted through Azure ML, and the image and student data was stored in 

--------

## Image showcase
The following section showcases what the website looks like with some screenshots
![Group selection](https://i.imgur.com/wE6ieix.jpeg)
![Functionality](https://i.imgur.com/lCXCW1w.jpeg)

## Setting up the project
The project consists of four sections:
- Creating the initial model
- The model in an Azure ML endpoint
- Mongo Atlas DB for student data
- Streamlit website

### Creating the initial model
To setup the model, you will need your set of images, organized in folders named according to their ID, and also a Python environment with numpy, keras-facenet, sklearn, and joblib.
Follow the code in [this notebook](https://github.com/GabrielIslas/face-recognition/blob/master/face_recognition_app/model_dev/model_dev.ipynb) and use or customize to your own folder structure, but basically:
1. Use the directory_face_recognition function to make the keras-facenet embedder return the vector representations of images while also relating them to their labels (their IDs)
2. Create a label encoder with sklearn using those IDs
3. Create a C-Support Vector Classificator using sklearn which learns from the embeddings generated
4. Dump both into .pkl files through joblib
These last two are what is going to be deployed in the Azure ML endpoint. An sklearn model is created separately like this, leaving the embedding conversion in the front side which is still safe, and also avoids using keras-facenet module in the Azure environments, which are prone to cause compatability problems because Python version which can support this module is not available.
