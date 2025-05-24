# import csv

# # Initialize attendance file
# attendance_file = "attendance.csv"

# # Check if the file exists; if not, create it with headers
# if not os.path.exists(attendance_file):
#     with open(attendance_file, "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["Name", "Date", "Time", "Attendance Status"])

# while True:
#     # Inside the loop where names are detected...
#     for face_encoding, face_location in zip(face_encodings, face_locations):
#         # Compare and get the name (as before)
#         matches = face_recognition.compare_faces(data["encodings"], face_encoding)
#         name = "Unknown"
#         if True in matches:
#             matched_idx = matches.index(True)
#             name = data["names"][matched_idx]

#             # Log attendance if the person is recognized
#             now = datetime.now()
#             date = now.strftime("%Y-%m-%d")
#             time = now.strftime("%H:%M:%S")
#             status = "Present"

#             # Avoid duplicate entries (based on name and date)
#             with open(attendance_file, "r") as f:
#                 records = f.readlines()

#             if f"{name},{date}" not in "".join(records):
#                 with open(attendance_file, "a", newline="") as f:
#                     writer = csv.writer(f)
#                     writer.writerow([name, date, time, status])

#                 print(f"Attendance marked for {name}.")
