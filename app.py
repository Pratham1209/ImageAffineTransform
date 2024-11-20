import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# Function for Affine Transformations
def perform_transformation(image, choice):
    rows, cols = image.shape[:2]
    
    if choice == "Translation":
        tx, ty = st.sidebar.slider("Translate X", -cols//2, cols//2, 50), st.sidebar.slider("Translate Y", -rows//2, rows//2, 30)
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        transformed = cv2.warpAffine(image, translation_matrix, (cols, rows))
    
    elif choice == "Rotation":
        angle = st.sidebar.slider("Rotation Angle", -180, 180, 45)
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        transformed = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    
    elif choice == "Scaling":
        scale_x = st.sidebar.slider("Scale X", 0.1, 3.0, 1.5)
        scale_y = st.sidebar.slider("Scale Y", 0.1, 3.0, 1.5)
        transformed = cv2.resize(image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)
    
    elif choice == "Shearing":
        shear_x = st.sidebar.slider("Shear X", -1.0, 1.0, 0.2)
        shear_y = st.sidebar.slider("Shear Y", -1.0, 1.0, 0.3)
        shearing_matrix = np.float32([[1, shear_x, 0], [shear_y, 1, 0]])
        transformed = cv2.warpAffine(image, shearing_matrix, (cols + int(shear_x * rows), rows + int(shear_y * cols)))
    
    else:
        transformed = image
    
    return transformed

# Streamlit App
st.title("Affine Transformation on Images")
st.write("Upload an image and choose a transformation to apply.")

# Upload image
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Transformation options
    option = st.selectbox("Choose a transformation:", ["Translation", "Rotation", "Scaling", "Shearing"])
    st.sidebar.title("Adjust Parameters")
    
    # Perform the transformation
    transformed_image = perform_transformation(image_np, option)
    
    # Display the result
    st.image(transformed_image, caption=f"Transformed Image - {option}", use_column_width=True)
else:
    st.write("Please upload an image to begin.")
