import os
import cv2
import shutil

# Input folder paths 
train_input = "dataset/train"  
test_input = "dataset/test"

# Output path
output_dir = "cleaned_data"
img_size = (224, 224)

# Load OpenCV's Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def preprocess_faces(input_path, output_path):
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    for class_folder in os.listdir(input_path):
        class_input_dir = os.path.join(input_path, class_folder)
        class_output_dir = os.path.join(output_path, class_folder)
        os.makedirs(class_output_dir, exist_ok=True)

        for i, img_name in enumerate(os.listdir(class_input_dir)):
            img_path = os.path.join(class_input_dir, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                continue

            (x, y, w, h) = faces[0]  # Use the first detected face
            face = img[y:y+h, x:x+w]
            face = cv2.resize(face, img_size)

            save_path = os.path.join(class_output_dir, f"{i}.jpg")
            cv2.imwrite(save_path, face)

    print(f"[INFO] Processed and saved faces to {output_path}")

# Run preprocessing
preprocess_faces(train_input, os.path.join(output_dir, "train"))
preprocess_faces(test_input, os.path.join(output_dir, "test"))
