import csv
import random
from datetime import datetime, timedelta

# List of students
students = [
    "Akshay Kumar",
    "Alexandra Daddario",
    "Alia Bhatt",
    "Amitabh Bachchan",
    "Andy Samberg",
    "Anushka Sharma"
]

# Random list of branches
branches = ["CSE", "ECE", "ME", "Civil", "IT"]

# Faculty names and subjects
faculty_subjects = [
    ("Dr. Sharma", "Mathematics"),
    ("Prof. Singh", "Computer Science"),
    ("Dr. Verma", "Physics"),
    ("Prof. Patel", "Chemistry"),
    ("Dr. Gupta", "Mechanical Engineering")
]

# Function to generate random attendance data
def generate_attendance_data():
    attendance_data = []

    # Current Date and Time
    current_datetime = datetime.now()
    
    # Iterate over students to generate data
    for student in students:
        for i in range(60):  # Generating data for 2 months (60 days)
            # Random Enrollment Number and Branch
            enrollment_number = f"{random.randint(10000, 99999)}"
            branch = random.choice(branches)

            # Random Date/Time/Period (within the last 60 days)
            random_days = random.randint(0, 60)
            date_time = current_datetime - timedelta(days=random_days)
            period = random.choice(["1st Period", "2nd Period", "3rd Period", "4th Period", "5th Period"])

            # Random Faculty Name and Subject
            faculty_name, subject = random.choice(faculty_subjects)

            # Random Attendance Status (Success/Failure)
            status = random.choice(["Success", "Failure"])

            # Random Attendance Percentage (between 60% and 90%)
            attendance_percentage = round(random.uniform(60, 90), 2)

            # Number of Total Classes, Attended, and Missed
            total_classes = random.randint(30, 50)
            attended_classes = random.randint(0, total_classes)
            missed_classes = total_classes - attended_classes

            # Append to the list
            attendance_data.append([
                student, 
                f"{enrollment_number}/{branch}", 
                date_time.strftime("%Y-%m-%d %H:%M:%S"), 
                f"{faculty_name} - {subject}", 
                status, 
                f"{attendance_percentage}%", 
                f"{total_classes} ({attended_classes}/{missed_classes})"
            ])
    
    # Write the data to a CSV file
    with open('attendance_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Name", "Enrollment Number / Branch", "Date/Time/Period", "Faculty Name & Subject", "Attendance Status", "Attendance Percentage", "Total Classes (Attended/Missed)"])
        # Write data rows
        writer.writerows(attendance_data)

# Generate the random attendance data
generate_attendance_data()
