import cv2
from ultralytics import YOLO
import datetime
import os

# Ensure the 'results' directory exists
os.makedirs("results", exist_ok=True)

def detect_objects_in_webcam():
    try:
        # Initialize the YOLO model
        print("Loading YOLO model...")
        yolo_model = YOLO('./runs/detect/Normal_Compressed/weights/best.pt')
        print("Model loaded successfully.")

        # Open the webcam (0 is usually the built-in webcam)
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("Error: Could not open webcam.")
            return

        print("Analyzing live webcam feed...")
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Run YOLO detection on the frame
            results = yolo_model(frame)

            detected = False  # Track if any gun or knife is detected

            for result in results:
                classes = result.names
                cls = result.boxes.cls
                conf = result.boxes.conf
                detections = result.boxes.xyxy

                # Debugging: print out detected class names
                print(f"Detected classes: {classes}")

                for pos, detection in enumerate(detections):
                    if conf[pos] >= 0.5:  # Confidence threshold
                        xmin, ymin, xmax, ymax = detection
                        label = f"{classes[int(cls[pos])]} {conf[pos]:.2f}" 

                        # Debugging: Print the class being detected
                        print(f"Class detected: {classes[int(cls[pos])]} with confidence {conf[pos]:.2f}")

                        # Check if the object is a gun or knife and set the detection flag
                        if classes[int(cls[pos])] == 'gun':
                            color = (0, 0, 255)  # Red for guns
                            detected = True  # Mark detection as True if gun is detected
                            print("Gun detected")  # Debugging print for guns
                        if classes[int(cls[pos])] == 'knife':
                            color = (255, 0, 0)  # Blue for knives
                            detected = True  # Mark detection as True if knife is detected
                            print("Knife detected")  # Debugging print for knives
                        else:
                            color = (0, int(cls[pos] * 50) % 255, 255)  # Default color

                        # Draw bounding box and label
                        cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                        cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)


                    # Save the frame immediately when a gun or knife is detected  
                        if detected:
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            image_path = f"results/{timestamp}.jpg"  # Fixed path to save in the 'results' directory
                            cv2.imwrite(image_path, frame)  # Save the frame in real-time
                            print(f"Frame saved: {image_path}")


            # Display the frame with detections
            cv2.imshow("Weapon Detection", frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture object and close display window
        video_capture.release()
        cv2.destroyAllWindows()
        print("Webcam feed closed.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Run the function to start detecting from the webcam
detect_objects_in_webcam()
