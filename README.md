# Attendance_system

This project is a real-time attendance system that:

Detects and identifies students using a webcam.

Recognizes their emotions.

Records attendance (present/absent) along with emotions and timestamps in a CSV file.

Works within a specified time window.

Provides a simple GUI to control the system.

📂 Project Structure

AttendanceSystem/
├── cleaned_data/                                       # Folder with student face images (subfolders per student)
├── emotion_dataset/                                    # Folder with emotion images (FER-2013 formatted)
├── face_model.h5                                       # Trained face recognition model
├── emotion_model.h5                                    # Trained emotion detection model
├── final_attendance.csv                                # Output CSV (attendance + emotions + timestamps)
├── gui_attendance_emotion_system.py                    # Main Python script (with GUI)
├── requirements.txt                                    # Required Python packages
└── README.md                                           # Project documentation


🚀 Features
✅ Real-time face detection and recognition.

✅ Real-time emotion detection.

✅ Marks present/absent automatically based on detection.

✅ Records multiple emotions with timestamps for each student.

✅ Automatically stops when the allowed time window ends.

✅ User-friendly GUI to start, stop, and view attendance.

