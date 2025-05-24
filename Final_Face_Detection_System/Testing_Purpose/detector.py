import cv2
import face_recognition
import pickle
from datetime import datetime

# Load the trained encodings and names
encoding_file = "face_encodings.pkl"
with open(encoding_file, "rb") as f:
    data = pickle.load(f)

# Initialize webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to exit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare the detected face encoding with the known encodings
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Unknown"  # Default name if no match is found

        if True in matches:
            # Get the index of the matched face
            matched_idx = matches.index(True)
            name = data["names"][matched_idx]

        # Draw a box around the face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Add the name below the face
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Display the video feed
    cv2.imshow("Face Recognition", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
