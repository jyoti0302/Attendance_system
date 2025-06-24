import cv2
import numpy as np
import pandas as pd
from datetime import datetime, time
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import os
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading
import subprocess
import platform

# ------------------------------ Configuration ------------------------------

all_students = sorted(os.listdir("cleaned_data/train"))
face_classes = os.listdir("cleaned_data/train")
emotion_classes = os.listdir("emotion_dataset/train")

start_str = "17:30"
end_str = "19:37"
csv_path = "final_attendance.csv"

student_logs = {}
detected_today = set()
logged_students = set()
running = False
cap = None

# ------------------------------ Load Models ------------------------------

face_model = load_model('face_model.h5')
emotion_model = load_model('emotion_model.h5')
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ------------------------------ Time Check ------------------------------

def is_within_time():
    now = datetime.now().time()
    return time.fromisoformat(start_str) <= now <= time.fromisoformat(end_str)

# ------------------------------ Attendance Logic ------------------------------

def start_attendance():
    global running, cap
    if not is_within_time():
        status_label.config(text=f"⏱️ Not in allowed time window ({start_str}–{end_str})", fg="red")
        return

    running = True
    cap = cv2.VideoCapture(0)
    threading.Thread(target=video_loop).start()
    status_label.config(text="✅ Attendance started...", fg="green")

def stop_attendance():
    global running, cap
    running = False
    if cap:
        cap.release()
        cap = None
    status_label.config(text="🛑 Attendance stopped", fg="black")
    start_button.config(state=tk.DISABLED)
    save_full_attendance()

def save_full_attendance():
    final_log = []

    for student in all_students:
        if student in student_logs:
            emotion_str = "; ".join(student_logs[student]["emotion"])
            time_str = "; ".join(student_logs[student]["time"])
            status = "Present"
        else:
            emotion_str = "-"
            time_str = "-"
            status = "Absent"

        final_log.append([student, emotion_str, time_str, status])

    df = pd.DataFrame(final_log, columns=["Name", "Emotion", "Time", "Status"])
    df.sort_values(by="Name", inplace=True)
    df.to_csv(csv_path, index=False)
    print("✅ Final attendance saved.")

# ------------------------------ Main Video Loop ------------------------------

def video_loop():
    global running, cap, student_logs
    attendance_end_time = time.fromisoformat(end_str)

    while running and cap.isOpened():
        current_time = datetime.now().time()
        if current_time > attendance_end_time:
            print("⏹️ Time limit reached. Stopping attendance automatically.")
            status_label.config(text="🕘 Time window closed. Attendance stopped.", fg="blue")
            stop_attendance()
            break

        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            face_rgb = frame[y:y+h, x:x+w]
            face_rgb_resized = cv2.resize(face_rgb, (224, 224))
            face_input = preprocess_input(np.expand_dims(face_rgb_resized, axis=0))
            face_pred = face_model.predict(face_input, verbose=0)
            name = face_classes[np.argmax(face_pred)]

            face_gray = gray[y:y+h, x:x+w]
            try:
                face_gray_resized = cv2.resize(face_gray, (48, 48))
            except:
                continue
            emotion_input = np.expand_dims(np.expand_dims(face_gray_resized, axis=-1), axis=0) / 255.0
            emotion_pred = emotion_model.predict(emotion_input, verbose=0)
            emotion = emotion_classes[np.argmax(emotion_pred)]

            log_time = datetime.now().strftime("%H:%M:%S")
            detected_today.add(name)

            if name not in student_logs:
                student_logs[name] = {"emotion": [emotion], "time": [log_time]}
            else:
                student_logs[name]["emotion"].append(emotion)
                student_logs[name]["time"].append(log_time)

            label = f"{name}, {emotion}"
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    stop_attendance()

# ------------------------------ CSV Viewer ------------------------------

def open_csv():
    filepath = os.path.abspath(csv_path)
    if platform.system() == "Windows":
        os.startfile(filepath)
    elif platform.system() == "Darwin":
        subprocess.call(["open", filepath])
    else:
        subprocess.call(["xdg-open", filepath])

# ------------------------------ GUI ------------------------------

root = tk.Tk()
root.title("Attendance & Emotion Detection System")
root.geometry("800x600")

status_label = Label(root, text="Press Start to begin", font=("Arial", 14))
status_label.pack(pady=10)

start_button = Button(root, text="Start Attendance", command=start_attendance, font=("Arial", 12), bg="green", fg="white")
start_button.pack(pady=5)

stop_button = Button(root, text="Stop Attendance", command=stop_attendance, font=("Arial", 12), bg="red", fg="white")
stop_button.pack(pady=5)

view_csv_button = Button(root, text="📄 View Attendance Log", command=open_csv, font=("Arial", 12), bg="#007acc", fg="white")
view_csv_button.pack(pady=5)

video_label = Label(root)
video_label.pack(pady=10)

status_label.config(text="🕘 Time window closed. Attendance stopped.", fg="blue")

root.mainloop()
