import cv2
import os
import time

# Create a folder to save the images if it doesn't exist
student_name = input("Enter the student's name: ")  # For naming the folder
output_dir = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Raw_Dataset"
os.makedirs(output_dir, exist_ok=True)

# Initialize webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit early.")
print("Starting to capture images...")

count = 0
total_images = 100  # Number of photos to capture

while count < total_images:
    time.sleep(0.4)
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Exiting.")
        break

    # Show the live video
    cv2.imshow("Capturing Images", frame)

    # Save the frame as an image
    file_path = os.path.join(output_dir, f"{student_name}_{count + 1}.jpg")
    cv2.imwrite(file_path, frame)
    print(f"Image {count + 1} saved: {file_path}")

    count += 1

    # Press 'q' to quit early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting early.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

print(f"Finished capturing {count} images.")
print(f"Images saved in: {output_dir}")
