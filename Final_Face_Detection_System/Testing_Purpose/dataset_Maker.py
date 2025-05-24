import os
import shutil

def expand_dataset(source_folder, target_folder, desired_count):
    # Prompt user for the name
    fname = input("Enter the first name: ").strip()
    lname = input("Enter the last name: ").strip()

    # Ensure the target folder exists
    os.makedirs(target_folder, exist_ok=True)

    # Get a list of image files in the source folder
    images = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    if len(images) == 0:
        print("No images found in the source folder.")
        return

    current_count = len(images)
    if current_count >= desired_count:
        print(f"The dataset already has {current_count} or more images.")
        return

    print(f"Expanding dataset from {current_count} to at least {desired_count} images...")

    # Copy images to the target folder with new labels
    index = 1
    while current_count < desired_count:
        for img in images:
            if current_count >= desired_count:
                break

            # Construct new file name
            new_name = f"{fname} {lname}_{index}.jpg"
            source_path = os.path.join(source_folder, img)
            target_path = os.path.join(target_folder, new_name)

            # Copy the file
            shutil.copy(source_path, target_path)
            print(f"Copied {img} to {new_name}")

            index += 1
            current_count += 1

    print(f"Dataset expanded to {current_count} images.")

# Specify source and target folders
source_folder = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Testing_Purpose\images"  # Replace with your source folder path
target_folder = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Raw_Dataset"  # Replace with your target folder path
desired_count = 100  # Desired number of images

expand_dataset(source_folder, target_folder, desired_count)
