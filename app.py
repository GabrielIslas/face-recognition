import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from PIL import Image
from keras_facenet import FaceNet
from pymongo import MongoClient
from datetime import datetime
import unicodedata

client = MongoClient("mongodb+srv://cesarcorrea:k9DexhefNDS9GTLs@cluster0.rwqzs.mongodb.net/AttendanceDB?retryWrites=true&w=majority&appName=Cluster0")
db = client.AttendanceDB
students_collection = db.students
attendance_collection = db.attendance

API_URL = "https://face-recog-ml-ztsfu.eastus.inference.ml.azure.com/score" 

embedder = FaceNet()

def predict_image(image):
    img_array = np.array(image.convert("RGB"))
    detections = embedder.extract(img_array, threshold=0.95)
    if not detections:
        st.error("No face detected in the image. Please try again.")
        return None

    embedding = detections[0]["embedding"]

    data = {"data": [embedding.tolist()]}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.secrets["API_KEY"]}'
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            matricula = result[0]  # Extract the student ID
            return matricula
        else:
            st.error("The API did not return a valid result.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")
        return None

LOGO_URL = "https://raw.githubusercontent.com/Cesar0ngas/final_faceapp/main/upylogo.png"

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Attendance"])

if page == "Home":
    WELCOME_IMAGE_URL = "https://github.com/Cesar0ngas/final_faceapp/blob/main/UPY%20Attendance%20Systema.jpg?raw=true"
    st.image(WELCOME_IMAGE_URL, use_column_width=True)
    st.write("Please go to the 'Attendance' section from the sidebar to mark attendance.")

elif page == "Attendance":
    st.sidebar.image(LOGO_URL, use_column_width=True)

    career = st.sidebar.selectbox("Select Career", ["Data Engineer", "Cybersecurity", "Embedded Systems", "Robotics"])
    quarter = st.sidebar.selectbox("Select Quarter", ["Immersion", "Third Quarter", "Sixth Quarter", "Ninth Quarter"])
    group = st.sidebar.selectbox("Select Group", ["A", "B"] if career == "Data Engineer" and quarter == "Ninth Quarter" else [])

    if group == "B":
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.subheader("Student Data for Group B")
            df_students = pd.DataFrame(list(students_collection.find({}, {"_id": 0, "name": 1, "matricula": 1, "attendance": 1})))
            student_table = st.empty()
            student_table.dataframe(df_students.sort_values(by='matricula'))

        with col2:
            st.subheader("Add a New Student")
            name = st.text_input("Student Name")
            matricula = st.text_input("Student ID")
            
            if st.button("Add Student"):
                if name and matricula:
                    students_collection.insert_one({"name": name, "matricula": matricula, "attendance": False})
                    st.success(f"Student {name} added successfully.")
                else:
                    st.warning("Please enter both the student name and ID.")

            if st.button("Refresh Table"):
                df_students = pd.DataFrame(list(students_collection.find({}, {"_id": 0, "name": 1, "matricula": 1, "attendance": 1})))
                student_table.dataframe(df_students.sort_values(by='matricula'))
                st.success("Table refreshed.")

            if st.button("Clear Attendance"):
                students_collection.update_many({}, {"$set": {"attendance": False}})
                attendance_collection.delete_many({})
                st.success("Attendance cleared successfully.")

        with col3:
            st.subheader("Camera and Image Upload")

            camera_active = st.toggle("Open Camera", key="camera_toggle")
            
            if camera_active:
                captured_image = st.camera_input("Take a photo", key="camera_input")
                if captured_image is not None:
                    image = Image.open(captured_image)
                    detected_matricula = predict_image(image)
                    if detected_matricula:
                        students_collection.update_one(
                            {"matricula": detected_matricula}, 
                            {"$set": {"attendance": True}}
                        )
                        attendance_collection.insert_one({
                            "name": detected_matricula, 
                            "timestamp": datetime.now()
                        })
                        st.success(f"Attendance marked for student ID: {detected_matricula}")

            uploaded_image = st.file_uploader("Upload an image to identify", type=["jpg", "png"], key="file_uploader")
            if uploaded_image:
                image = Image.open(uploaded_image)
                detected_matricula = predict_image(image)
                if detected_matricula:
                    students_collection.update_one(
                        {"matricula": detected_matricula}, 
                        {"$set": {"attendance": True}}
                    )
                    attendance_collection.insert_one({
                        "name": detected_matricula, 
                        "timestamp": datetime.now()
                    })
                    st.success(f"Attendance marked for student ID: {detected_matricula}")
