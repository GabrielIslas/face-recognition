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

### Deploying into an Azure ML endpoint
1. Create an Azure Machine Learning workspace, then launch the Studio web app.
2. Go to the Environments section, then the Custom Environments section, and create a new environment and use the Dockerfile and environment.yaml from [here](https://github.com/GabrielIslas/face-recognition/tree/master/face_recognition_app/model_dev/azure-ml-endpoint) to define it.
3. After waiting for the environment to get created, go to the Models section and register a new model through a folder to upload both the label encoder and the model itself into one model register.
4. Finally, once the model has been registered, go to the Endpoints section, and create a new endpoint that uses the models registered in the environment created, and the models send their answer using the endpoint function in the same previous link. (Deploying the endpoint takes a while)

### Setting Up MongoDB Atlas
1. Create a MongoDB Atlas account:
   -Go to [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) and create a free cluster
2. Once you are in the home page, look for the option "Database Access" in the sidebar and make sure you have "AtlasAdmin" in the role section.
3. Then go to "Network Access" just below "Database Access" and set it to a public IP address.
4. Add connection settings to the application:
   Update the following code with your credentials: "client = MongoClient("mongodb+srv://<username>:<password>@<cluster-url>")"

### Running the Streamlit App
1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your Github account.
3. Create an app.
4. Select "Deploy a public app from Github"
5. Select the repository where the app is and choose the main file. (app.py)
6. Let streamlit cook your app!

### -Warnings!!!
To effectively deploy your app, make sure you upload all the requirements to the repository.
- The requirements.txt (here you are supposed to write all the libraries used)
- The packages.txt (if necessary)
- A folder called ".streamlit" where you must have the next files (file_name.toml):
  1. The secret key (Azure)
  2. The file where you can customize the app (colors, shapes, font, etc.)
