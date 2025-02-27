import cv2
import numpy as np

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

print("Starting webcam for face detection. Press 'q' to quit.")

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture video.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Predict the ID and confidence of the detected face
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        
        # Check if confidence is within acceptable range
        if confidence < 100:  # Lower value indicates higher confidence
            name = name_map.get(id, "Unknown")
            confidence_text = f"{round(100 - confidence)}% match"
        else:
            name = "Unknown"
            confidence_text = ""

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Display the name and confidence
        cv2.putText(frame, f"{name} {confidence_text}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Show the video feed with face detection
    cv2.imshow('Face Recognition', frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Webcam feed closed.")
