# Home Guardian

## Overview

Home Guardian is an advanced surveillance system incorporating **face recognition** and **weapon detection** for knives and guns. It is designed to identify threats and unknown individuals, enhancing security in various environments. Additionally, the system includes a **To-Do List feature** that allows users to manage daily tasks and receive reminders.

## Features

- **Face Recognition**: Detects and identifies individuals based on stored facial data.
- **Weapon Detection**: Identifies the presence of knives and firearms in real time.
- **Surveillance & Threat Detection**: Monitors the surroundings and raises alerts upon detecting unknown individuals or potential threats.
- **To-Do List & Reminder**: Users can add and remove tasks with reminder notifications.



## Installation & Usage

### Step 1: Enrolling Faces

To add a person's face to the database, run the following file:

```bash
python upload_face.py
```

- The script will prompt for the person's **name** and their **relation** to the user.
- The camera will open to capture multiple images of the person’s face for training.

### Step 2: Training the Model

After enrolling faces, train the model using:

```bash
python train_model.py
```

- This process will store the facial data and details of the registered individuals.

### Step 3: Running the Main Detection System

Start the detection system by executing:

```bash
python gui.py
```

- A login screen will appear, prompting for a **username** and **password**.
  - **Username**: `a`
  - **Password**: `a`
- After logging in, the main interface opens, allowing access to:
  - **Real-time face and weapon detection**
  - **To-Do List and Reminders**

## System Requirements

- Python 3.x
- OpenCV
- TensorFlow/Keras
- NumPy
- Tkinter (for GUI)

## Future Enhancements

- SMS/Email Alerts for detected threats
- Cloud integration for remote monitoring
- Expanded weapon detection for additional threat identification

## Contact & Support

For any issues or inquiries, reach out to our support team at

**shubham21303162@gmail.com**

