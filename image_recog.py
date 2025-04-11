import os
from deepface import DeepFace

# Path to the database folder where images are stored
DATABASE_PATH = "database"

def verify_face(input_image):
    """
    Compare the input image against all images in the database to find a match.
    """
    if not os.path.exists(DATABASE_PATH):
        print("Database folder not found!")
        return None

    for stored_image in os.listdir(DATABASE_PATH):
        stored_image_path = os.path.join(DATABASE_PATH, stored_image)

        try:
            # Compare input image with stored image
            result = DeepFace.verify(input_image, stored_image_path)
            
            if result["verified"]:
                print(f"Match found with: {stored_image}")
                return stored_image

        except Exception as e:
            print(f"Error processing {stored_image}: {e}")

    print("No match found.")
    return None

if __name__ == "__main__":
    input_image = input("Enter path to the input image: ")
    
    if os.path.exists(input_image):
        matched_image = verify_face(input_image)
        if matched_image:
            print(f"Identity confirmed with {matched_image}")
        else:
            print("No identity match found.")
    else:
        print("Input image file not found.")
