from flask import Flask, render_template, request, redirect, url_for , Response
from datetime import datetime
import cv2
import face_recognition
import pickle
from datetime import datetime
import pandas as pd
import time
import threading

app = Flask(__name__)

# Load trained encodings
encoding_file = r"C:\Users\suyas\Desktop\Final_Face_Detection_System\Final_Face_Detection_System\Model\face_encodings.pkl"
with open(encoding_file, "rb") as f:
    data = pickle.load(f)

# Default values for student details
default_student_data = {
    "name": "Not Recognized",
    "enrollment": "N/A",
    "faculty": "N/A",
    "subject": "N/A",
    "status": "N/A",
    "period": "N/A",
    "percentage": "0%",
    "total_classes": 0,
    "attended_classes": 0,
    "missed_classes": 0,
    "datetime": "N/A"
}

# Globals for threading
frame = None
lock = threading.Lock()
video_running = False


# Global variable to store recognition details
recognition_details = default_student_data.copy()

# Load attendance data
# attendance_file = "data/attendance.csv"
# attendance_df = pd.read_csv(attendance_file)

#TIME TABLE 
timetable = {
    "Monday": [
        {"period": 1, "start_time": "09:45", "end_time": "10:45", "subject": "Cyber Security", "faculty": "Prof. Santosh Nagar"},
        {"period": 2, "start_time": "10:45", "end_time": "11:45", "subject": "TOC", "faculty": "Prof. Vaibhav Patel"},
        {"period": 3, "start_time": "11:45", "end_time": "12:45", "subject": "IWT", "faculty": "Prof. Deepika Pal"},
        {"period": 4, "start_time": "13:25", "end_time": "14:25", "subject": "DBMS", "faculty": "Prof. Netesh"},
        {"period": 5, "start_time": "14:25", "end_time": "16:25", "subject": "Lab", "faculty": "Prof. Anjali Sharma"}
    ],
    "Tuesday": [
        {"period": 1, "start_time": "09:45", "end_time": "10:45", "subject": "IWT", "faculty": "Prof. Deepika Pal"},
        {"period": 2, "start_time": "10:45", "end_time": "11:45", "subject": "Cyber Security", "faculty": "Prof. Santosh Nagar"},
        {"period": 3, "start_time": "11:45", "end_time": "12:45", "subject": "TOC", "faculty": "Prof. Vaibhav Patel"},
        {"period": 4, "start_time": "13:25", "end_time": "14:25", "subject": "Lab", "faculty": "Prof. Anjali Sharma"},
        {"period": 5, "start_time": "14:25", "end_time": "16:25", "subject": "DBMS", "faculty": "Prof. Netesh"}
    ],
    "Wednesday": [
        {"period": 1, "start_time": "09:45", "end_time": "10:45", "subject": "DBMS", "faculty": "Prof. Netesh"},
        {"period": 2, "start_time": "10:45", "end_time": "11:45", "subject": "Cyber Security", "faculty": "Prof. Santosh Nagar"},
        {"period": 3, "start_time": "11:45", "end_time": "12:45", "subject": "TOC", "faculty": "Prof. Vaibhav Patel"},
        {"period": 4, "start_time": "13:25", "end_time": "14:25", "subject": "IWT", "faculty": "Prof. Deepika Pal"},
        {"period": 5, "start_time": "14:25", "end_time": "16:25", "subject": "Lab", "faculty": "Prof. Anjali Sharma"}
    ],
    "Thursday": [
        {"period": 1, "start_time": "09:45", "end_time": "10:45", "subject": "Lab", "faculty": "Prof. Anjali Sharma"},
        {"period": 2, "start_time": "10:45", "end_time": "11:45", "subject": "IWT", "faculty": "Prof. Deepika Pal"},
        {"period": 3, "start_time": "11:45", "end_time": "12:45", "subject": "DBMS", "faculty": "Prof. Netesh"},
        {"period": 4, "start_time": "13:25", "end_time": "14:25", "subject": "Cyber Security", "faculty": "Prof. Santosh Nagar"},
        {"period": 5, "start_time": "14:25", "end_time": "16:25", "subject": "TOC", "faculty": "Prof. Vaibhav Patel"}
    ],
    "Friday": [
        {"period": 1, "start_time": "09:45", "end_time": "10:45", "subject": "Cyber Security", "faculty": "Prof. Santosh Nagar"},
        {"period": 2, "start_time": "10:45", "end_time": "11:45", "subject": "DBMS", "faculty": "Prof. Netesh"},
        {"period": 3, "start_time": "11:45", "end_time": "12:45", "subject": "IWT", "faculty": "Prof. Deepika Pal"},
        {"period": 4, "start_time": "13:25", "end_time": "14:25", "subject": "TOC", "faculty": "Prof. Vaibhav Patel"},
        {"period": 5, "start_time": "14:25", "end_time": "16:25", "subject": "Lab", "faculty": "Prof. Anjali Sharma"}
    ],
    "Saturday": [
        {"period": 1, "start_time": "09:45", "end_time": "10:45", "subject": "TOC", "faculty": "Prof. Vaibhav Patel"},
        {"period": 2, "start_time": "10:45", "end_time": "11:45", "subject": "Cyber Security", "faculty": "Prof. Santosh Nagar"},
        {"period": 3, "start_time": "11:45", "end_time": "12:45", "subject": "Lab", "faculty": "Prof. Anjali Sharma"},
        {"period": 4, "start_time": "13:25", "end_time": "14:25", "subject": "DBMS", "faculty": "Prof. Netesh"},
        {"period": 5, "start_time": "14:25", "end_time": "16:25", "subject": "IWT", "faculty": "Prof. Deepika Pal"}
    ]
}

#DEtails

# Function to get the current day and time
def get_class_for_current_time():
    now = datetime.now()
    # current_day = now.strftime("%A")  # Get full weekday name (e.g., Monday, Tuesday)
    # current_time = now.strftime("%H:%M")  # Get time in HH:MM format
    # current_time = "10:05"
    current_time = "10:15"
    current_day = "Monday"


    if current_day in timetable:
        for slot in timetable[current_day]:
            # If current time is between start_time and end_time of a class, return the class details
            if slot["start_time"] <= current_time <= slot["end_time"]:
                return slot
    return None  # If no class found for the current time

# Function to update the recognition details
def update_recognition_details(recognized_name):
    global recognition_details
    now = datetime.now()
    class_details = get_class_for_current_time()
    if recognized_name == "Abhinav Nema":
        recognized_name = "Suyash Patel"

    if recognized_name != "Unknown" and class_details:
        recognition_details.update({
            "name": recognized_name,
            "enrollment": "123456 / CSE",
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "faculty": class_details["faculty"],
            "subject": class_details["subject"],
            "period": class_details["period"],
            "status": "Success",
            "percentage": "80%",
            "total_classes": 30,
            "attended_classes": 24,
            "missed_classes": 6,
        })
    else:
        recognition_details.update({
            "name": "Not Recognized",
            "enrollment": "N/A",
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "faculty": "N/A",
            "subject": "N/A",
            "period": "N/A",
            "status": "Failure",
            "percentage": "0%",
            "total_classes": 30,
            "attended_classes": 0,
            "missed_classes": 30,
        })





def generate_frames():
    global frame, video_running
    cap = cv2.VideoCapture(0)
    video_running = True

    while video_running:
        ret, frame_read = cap.read()
        if not ret:
            break

        with lock:
            frame = frame_read.copy()

        # Overlay recognition details on the frame
        # overlay_text = f"Name: {recognition_details['name']}"
        # cv2.putText(frame, overlay_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    cap.release()



# Function to process video feed and perform face recognition
def scan_faces():
    global recognition_details, frame, video_running

    while video_running:
        with lock:
            if frame is None:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            recognized_name = "Unknown"
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(data["encodings"], face_encoding)
                if True in matches:
                    matched_idx = matches.index(True)
                    recognized_name = data["names"][matched_idx]

            update_recognition_details(recognized_name)
            time.sleep(1)  # Adjust delay as needed


    # now = datetime.now()
    # recognition_details = {
    #     "name": recognized_name if recognized_name != "Unknown" else "Not Recognized",
    #     "enrollment": "123456 / CSE" if recognized_name != "Unknown" else "N/A",
    #     "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
    #     "faculty": "Dr. Smith" if recognized_name != "Unknown" else "N/A",
    #     "subject": "Computer Science" if recognized_name != "Unknown" else "N/A",
    #     "status": "Success" if recognized_name != "Unknown" else "Failure",
    #     "percentage": "80%" if recognized_name != "Unknown" else "0%",
    #     "total_classes": 30,
    #     "attended_classes": 24 if recognized_name != "Unknown" else 0,
    #     "missed_classes": 6 if recognized_name != "Unknown" else 30,
    # }


@app.route("/")
def index():
    return render_template("index.html", student_details=recognition_details)

@app.route("/start_scan", methods=["POST"])
def start_scan():
    threading.Thread(target=scan_faces, daemon=True).start()
    return redirect(url_for("index"))

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/stop_scan", methods=["POST"])
def stop_scan():
    global video_running
    video_running = False
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)