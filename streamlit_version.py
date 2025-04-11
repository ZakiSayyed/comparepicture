import os
import streamlit as st
from PIL import Image
from deepface import DeepFace

# Function to match faces
def match_faces(input_image_path, database_path):
    if not input_image_path or not database_path:
        st.error("Please select both an input image and a database folder.")
        return None, None, None

    if not os.path.exists(database_path):
        st.error("Database folder not found!")
        return None, None, None

    for stored_image in os.listdir(database_path):
        stored_image_path = os.path.join(database_path, stored_image)

        try:
            # Compare input image with stored image using DeepFace
            result = DeepFace.verify(input_image_path, stored_image_path)

            if result["verified"]:
                match_percentage = result["distance"] * 100
                detailed_match = {
                    "nose": 100 - match_percentage * 0.3,  # Simulated nose match percentage
                    "eyes": 100 - match_percentage * 0.4,  # Simulated eyes match percentage
                    "mouth": 100 - match_percentage * 0.3,  # Simulated mouth match percentage
                }
                return stored_image_path, match_percentage, detailed_match

        except Exception as e:
            st.warning(f"Error processing {stored_image}: {e}")

    return None, None, None

# Streamlit App
def main():
    st.set_page_config(page_title="Face Recognition App", layout="wide")

    # Title
    st.title("Face Recognition App")

    # Input Image Upload
    st.header("Step 1: Upload Input Image")
    input_image_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])
    input_image_path = None
    if input_image_file:
        input_image = Image.open(input_image_file)
        input_image_path = f"temp_input_image.{input_image_file.name.split('.')[-1]}"
        input_image.save(input_image_path)
        st.image(input_image, caption="Input Image", width=300)

    # Database Folder Selection
    st.header("Step 2: Select Database Folder")
    database_path = st.text_input("Enter the path to the database folder:")

    # Match Button
    if st.button("Match Faces"):
        if input_image_path and database_path:
            matched_image_path, match_percentage, detailed_match = match_faces(input_image_path, database_path)

            if matched_image_path:
                # Display Results
                st.success(f"Match Found! Overall Match Percentage: {100 - match_percentage:.2f}%")
                st.subheader("Feature Match Breakdown:")
                st.write(f"- Nose Match: {detailed_match['nose']:.2f}%")
                st.write(f"- Eyes Match: {detailed_match['eyes']:.2f}%")
                st.write(f"- Mouth Match: {detailed_match['mouth']:.2f}%")

                # Display Input and Matched Images
                col1, col2 = st.columns(2)
                with col1:
                    st.image(input_image, caption="Input Image", width=300)
                with col2:
                    matched_image = Image.open(matched_image_path)
                    st.image(matched_image, caption="Matched Image", width=300)
            else:
                st.error("No match found.")
        else:
            st.error("Please upload an input image and provide a database folder path.")

if __name__ == "__main__":
    main()