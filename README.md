# Attendance_system

This project is a real-time attendance system that:

Detects and identifies students using a webcam.

Recognizes their emotions.

Records attendance (present/absent) along with emotions and timestamps in a CSV file.

Works within a specified time window.

Provides a simple GUI to control the system.




🚀 Features

✅ Real-time face detection and recognition.

✅ Real-time emotion detection.

✅ Marks present/absent automatically based on detection.

✅ Records multiple emotions with timestamps for each student.

✅ Automatically stops when the allowed time window ends.

✅ User-friendly GUI to start, stop, and view attendance.

📂 Dataset

🔹 Face Recognition Model:

Image Collection:
Images were downloaded using the bing_image_downloader library by providing search queries for each student/class label.

Preprocessing:
Images were preprocessed using the image_preprocessing script to ensure uniform size, proper format, and quality for model training.

Balancing the Dataset:
To balance the number of images per class, data augmentation techniques were applied using the augmentation script.

Final Dataset:
The cleaned and balanced dataset is available here:
https://drive.google.com/drive/u/0/folders/1y7hkfjfcmLMAGrCbOqvOtqVYIlodWybs

🔹 Emotion Detection Model:

Dataset Source:
The FER 2013 dataset was downloaded from Kaggle.

Storage Path:
It is stored in the emotion_dataset folder for model training.

Dataset Link:
https://www.kaggle.com/datasets/msambare/fer2013

Face Model:
https://drive.google.com/file/d/1kspjxTgmh9b7-YVvQqiRZo-xf_8wXsAE/view?usp=sharing

Face Model Weights:
https://drive.google.com/file/d/1Y4aFsSpaNCeHtsLenUKQ_1meOAWrZxfm/view?usp=sharing

Emotion Model:
https://drive.google.com/file/d/1zEIzMiy_cgVSjboGjRIFaVmXfZRTaSjo/view?usp=sharing

Emotion Model Weights:
https://drive.google.com/file/d/1vuer3LheGJGj7dlHsJuJwtvhdah9lyoN/view?usp=sharing
