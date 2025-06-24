import os
import cv2
import numpy as np
import random
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image

# Define augmentation generator
augmentor = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.05,
    height_shift_range=0.05,
    zoom_range=0.1,
    brightness_range=[0.8, 1.2],
    horizontal_flip=True,
    fill_mode='nearest'
)

def augment_to_target(folder_path, target_count):
    image_files = os.listdir(folder_path)
    image_paths = [os.path.join(folder_path, f) for f in image_files if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    current_count = len(image_paths)

    if current_count == 0:
        print(f"[WARNING] {folder_path} is empty.")
        return

    img_size = (224, 224)  # your face image size

    while current_count < target_count:
        img_path = random.choice(image_paths)
        img = cv2.imread(img_path)
        img = cv2.resize(img, img_size)
        img = np.expand_dims(img, axis=0)

        # Generate one augmented image
        aug_iter = augmentor.flow(img, batch_size=1)
        aug_img = next(aug_iter)[0].astype(np.uint8)

        # Save with unique name
        new_name = f"aug_{current_count}.jpg"
        new_path = os.path.join(folder_path, new_name)
        Image.fromarray(aug_img).save(new_path)

        current_count += 1

    print(f"[INFO] {folder_path} now has {target_count} images.")

# Define folders
train_root = "cleaned_data/train"
test_root = "cleaned_data/test"

# Augment all folders
for folder in os.listdir(train_root):
    augment_to_target(os.path.join(train_root, folder), target_count=50)

for folder in os.listdir(test_root):
    augment_to_target(os.path.join(test_root, folder), target_count=20)
