import cv2
import os
import pandas as pd

# Paths for storing data
data_path = 'TrainingImage'
csv_file = 'StudentDetails.csv'

# Ensure the data path exists
os.makedirs(data_path, exist_ok=True)

# Capture user details
name = input("Enter name: ")
relation = input("Enter relation: ")

# Load or create CSV with ID assignment
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    last_id = df['ID'].max() if not df.empty else 0
else:
    df = pd.DataFrame(columns=["ID", "Name", "Relation"])
    last_id = 0

new_id = last_id + 1
df = pd.concat([df, pd.DataFrame({"ID": [new_id], "Name": [name], "Relation": [relation]})], ignore_index=True)
df.to_csv(csv_file, index=False)

# Initialize webcam
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
count = 0

while count < 50:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        count += 1
        face_img = frame[y:y + h, x:x + w]
        img_filename = os.path.join(data_path, f"{new_id}_{name}_{count}.jpg")
        cv2.imwrite(img_filename, face_img)

        # Draw a rectangle and label for visual feedback
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f"Captured {count}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow('Face Capture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:
        break

cap.release()
cv2.destroyAllWindows()
