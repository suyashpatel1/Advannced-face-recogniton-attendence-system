import cv2
import os

# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to crop face from the image
def crop_face(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert the image to grayscale (required for face detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image (returns a list of rectangles where faces are detected)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # If no faces are detected, return None
    if len(faces) == 0:
        print(f"No face detected in {image_path}")
        return None
    
    # Loop through all the faces detected (in case there are multiple faces)
    for (x, y, w, h) in faces:
        # Crop the face from the image
        cropped_img = img[y:y+h, x:x+w]
        
        return cropped_img

# Directory containing the images
image_directory = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Raw_Dataset"  # Update this path

# Directory to save cropped faces
output_directory = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Dataset\Faces"  # Update this path
os.makedirs(output_directory, exist_ok=True)

# Process all images in the directory
for filename in os.listdir(image_directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Full image path
        image_path = os.path.join(image_directory, filename)
        
        # Get the cropped face
        cropped_image = crop_face(image_path)
        
        # If a face was detected, save the cropped image
        if cropped_image is not None:
            output_path = os.path.join(output_directory, filename)  # Save with the same filename
            cv2.imwrite(output_path, cropped_image)
            print(f"Saved cropped image: {filename}")
        else:
            print(f"Face not detected in {filename}")

print("Face cropping completed.")
