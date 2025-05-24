import os
import cv2
import face_recognition
import pickle

# Path to the dataset folder
dataset_dir = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Dataset\Faces"
encoding_file = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Model\face_encodings.pkl"  # File to save the encodings

# Initialize lists to store encodings and names
known_encodings = []
known_names = []

# Loop through each image in the dataset directory
for image_name in os.listdir(dataset_dir):
    if not image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue  # Skip non-image files

    # Extract the name from the file (e.g., "Firstname Lastname_number.jpg")
    name = " ".join(image_name.split("_")[:-1])  # Remove the image number and extension

    # Full path to the image
    image_path = os.path.join(dataset_dir, image_name)

    print(f"Processing image: {image_path} for {name}")

    # Load the image using face_recognition
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB format

    # Find face locations and encodings in the image
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    # Assume one face per image and save the encoding
    if len(face_encodings) > 0:
        known_encodings.append(face_encodings[0])
        known_names.append(name)

print("Encoding completed.")

# Save the encodings and names to a file
data = {"encodings": known_encodings, "names": known_names}
with open(encoding_file, "wb") as f:
    pickle.dump(data, f)

print(f"Encodings saved to {encoding_file}.")