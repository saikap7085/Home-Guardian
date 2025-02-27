import cv2
import datetime
import os
import numpy as np
from ultralytics import YOLO

# Ensure the 'results' directory exists for saving weapon detection images
os.makedirs("results", exist_ok=True)

# Load the YOLO model for weapon detection
print("Loading YOLO model...")
yolo_model = YOLO('./runs/detect/Normal_Compressed/weights/best.pt')
print("Model loaded successfully.")

# Load the trained face recognizer model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

# Load the face cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load names from the CSV file to map label IDs to names
name_map = {}
with open('StudentDetails.csv', 'r') as f:
    next(f)  # Skip the header line
    for line in f:
        id, name, relation = line.strip().split(',')
        name_map[int(id)] = name

print("Starting webcam for weapon and face detection. Press 'q' to quit.")

# Start video capture from the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture video.")
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Weapon detection using YOLO
    results = yolo_model(frame)
    detected = False  # Track if any weapon is detected in the current frame

    for result in results:
        classes = result.names
        cls = result.boxes.cls
        conf = result.boxes.conf
        detections = result.boxes.xyxy

        for pos, detection in enumerate(detections):
            if conf[pos] >= 0.5:  # Confidence threshold for detection
                xmin, ymin, xmax, ymax = detection
                label = f"{classes[int(cls[pos])]} {conf[pos]:.2f}"

                # Check if the object is a gun or knife and set color accordingly
                if classes[int(cls[pos])] == 'guns':
                    color = (0, 0, 255)  # Red for guns
                    detected = True
                    print("Gun detected")

                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_path = f"results/{timestamp}.jpg"
                    cv2.imwrite(image_path, frame)
                    print(f"Frame saved: {image_path}")

                elif classes[int(cls[pos])] == 'knife':
                    color = (255, 0, 0)  # Blue for knives
                    detected = True
                    print("Knife detected")

                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    image_path = f"results/{timestamp}.jpg"
                    cv2.imwrite(image_path, frame)
                    print(f"Frame saved: {image_path}")

                else:
                    color = (0, int(cls[pos] * 50) % 255, 255)

                # Draw bounding box and label for detected weapons
                cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    # Face detection and recognition
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Predict the ID and confidence of the detected face
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is within an acceptable range
        if confidence < 100:  # Lower value indicates higher confidence
            name = name_map.get(id, "Unknown")
            confidence_text = f"{round(100 - confidence)}% match"
        else:
            name = "Unknown"
            confidence_text = ""

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the name and confidence
        cv2.putText(frame, f"{name} {confidence_text}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Show the video feed with weapon and face detections
    cv2.imshow('Weapon and Face Detection', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close display window
cap.release()
cv2.destroyAllWindows()
print("Webcam feed closed.")
