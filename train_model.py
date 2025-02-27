import cv2
import numpy as np
import os

# Path for training images
data_path = 'TrainingImage'
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Get image paths and initialize data arrays
image_paths = [os.path.join(data_path, f) for f in os.listdir(data_path)]
faces = []
ids = []

for image_path in image_paths:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue

    # Extract the ID from the filename (format: id_name_count.jpg)
    label_id = int(os.path.basename(image_path).split('_')[0])
    faces.append(img)
    ids.append(label_id)

recognizer.train(faces, np.array(ids))
recognizer.save('trainer.yml')
print("Model training complete.")
