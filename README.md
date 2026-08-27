# 🔐 Anti-Glare Face Recognition Door Lock

### Dual-Verification Smart Door Access System with Pushbullet Notifications

A smart security and access-control system that combines **real-time face recognition, anti-spoofing techniques, Arduino-controlled locking, and Pushbullet notifications** to provide a secure and intelligent door-locking solution.

The system verifies whether a person is an **authorized user** and whether the detected face belongs to a **real person rather than a photo or screen replay**. Authorized users can unlock the door, while unauthorized or suspicious attempts trigger an alert with a captured image.

---

## 📌 Project Overview

Traditional face-recognition systems can be vulnerable to simple spoofing attacks, such as presenting a photograph or a phone screen in front of the camera.

This project improves security by introducing multiple anti-spoofing checks before allowing access:

* 👤 Face recognition
* ✨ Glare/reflection detection
* 🎥 Motion analysis
* 🧩 Texture/quality analysis
* 🔐 Arduino-controlled servo locking
* 📲 Pushbullet security notifications
* 📝 Automatic attendance/access logging

The combination of these mechanisms provides an additional security layer over basic face recognition.

---

## ✨ Key Features

### 👤 Real-Time Face Recognition

Uses **OpenCV** and the `face_recognition` library to identify registered users from a live camera feed.

### 🛡️ Anti-Spoofing Detection

The system performs multiple checks to reduce the possibility of unauthorized access using:

* Printed photographs
* Mobile-phone displays
* Screens displaying a person's face
* Other basic replay attacks

Anti-spoofing is based on:

* **Glare detection** – identifies characteristics commonly associated with reflective screens or printed surfaces.
* **Motion analysis** – checks for natural movement in the detected face.
* **Texture analysis** – examines image characteristics to distinguish real facial regions from potential spoofing media.

### 🔒 Arduino-Based Door Lock

An Arduino controls a **servo motor** that physically locks and unlocks the door.

### 📲 Pushbullet Security Alerts

When an unauthorized or suspicious access attempt is detected, the system:

1. Captures an image.
2. Sends the captured image through Pushbullet.
3. Notifies the owner about the access attempt.

### 📝 Attendance & Access Logging

Successful authorized entries are automatically recorded for monitoring and attendance purposes.

### 🔑 Environment-Based API Security

Sensitive credentials such as the Pushbullet API token are stored using **environment variables** rather than being hard-coded into the source code.

---

## 🏗️ System Architecture

```text
                 ┌──────────────────┐
                 │      Webcam      │
                 └────────┬─────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Face Detection   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Face Recognition    │
                └─────────┬──────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │  Anti-Spoofing      │
               │      Checks         │
               │                     │
               │ • Glare Detection   │
               │ • Motion Analysis   │
               │ • Texture Check     │
               └──────────┬──────────┘
                          │
                 ┌────────┴────────┐
                 │                 │
              Authorized        Unknown /
               + Real           Suspicious
                 │                 │
                 ▼                 ▼
        ┌────────────────┐   ┌─────────────────┐
        │ Arduino +      │   │ Capture Image   │
        │ Servo Motor    │   └────────┬────────┘
        └───────┬────────┘            │
                │                     ▼
                ▼              ┌────────────────┐
          🔓 Door Unlock       │   Pushbullet   │
                               │   Notification  │
                               └────────────────┘
```

---

## ⚙️ How It Works

### Step 1 — Camera Capture

The webcam continuously captures frames from the environment.

### Step 2 — Face Detection

The system detects faces present in the camera frame.

### Step 3 — Face Recognition

The detected face is compared against registered/known faces.

### Step 4 — Anti-Spoofing Verification

Before unlocking the door, additional checks are performed:

```text
Face Detected
     │
     ▼
Face Recognized?
     │
   ┌─┴─────────┐
   │           │
  YES          NO
   │           │
   ▼           ▼
Anti-Spoof   Capture
Checks       Image
   │           │
   ▼           ▼
Passed?     Pushbullet
   │         Alert
 ┌─┴───┐
 │     │
YES    NO
 │     │
 ▼     ▼
Unlock Alert
Door   +
 │    Log
 ▼
Log Access
```

### Step 5 — Door Control

If the face is recognized **and** the anti-spoofing checks pass, the Arduino activates the servo motor and unlocks the door.

### Step 6 — Unauthorized Access

If the face is unknown or the anti-spoofing checks fail:

* The door remains locked.
* An image is captured.
* A Pushbullet notification is sent.
* The event can be recorded for monitoring.

---

## 🧰 Technologies Used

| Component               | Technology            |
| ----------------------- | --------------------- |
| Programming Language    | Python                |
| Computer Vision         | OpenCV                |
| Face Recognition        | `face_recognition`    |
| Hardware Control        | Arduino               |
| Lock Mechanism          | Servo Motor           |
| Notifications           | Pushbullet            |
| Camera                  | USB Webcam            |
| Data Logging            | CSV / Text File       |
| Development Environment | Arduino IDE / VS Code |

---

## 🔩 Hardware Requirements

* 💻 Computer/Laptop
* 📷 USB Webcam
* 🔌 Arduino Uno or compatible Arduino board
* ⚙️ Servo Motor
* 🔗 USB Cable
* 🔋 External power supply if required
* 🚪 Servo-compatible door-lock mechanism
* Jumper wires/breadboard as required

---

## 💻 Software Requirements

* Python **3.7+**
* Arduino IDE
* OpenCV
* `face_recognition`
* NumPy
* PySerial
* Pushbullet API access

Install the required Python packages with:

```bash
pip install opencv-python face-recognition numpy pyserial pushbullet.py
```

> Depending on your operating system and Python version, installing `face_recognition` may require additional dependencies such as `dlib`.

---

## 📂 Suggested Project Structure

```text
anti-glare-face-door-lock/
│
├── main.py
├── face_recognition_module.py
├── anti_spoofing.py
├── arduino_controller.py
├── notification.py
├── attendance.py
│
├── known_faces/
│   ├── person1.jpg
│   ├── person2.jpg
│   └── person3.jpg
│
├── captured_images/
│
├── attendance/
│   └── attendance.csv
│
├── arduino/
│   └── door_lock.ino
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/anti-glare-face-door-lock.git
cd anti-glare-face-door-lock
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Authorized Faces

Place clear images of authorized users inside the `known_faces/` directory.

Example:

```text
known_faces/
├── Alice.jpg
├── Bob.jpg
└── Charlie.jpg
```

The system uses these images to create the known-face database.

> **Privacy:** Do not upload real personal face images to a public repository without appropriate permission.

### 4. Configure Pushbullet

Create a Pushbullet access token and store it as an environment variable.

Example `.env`:

```env
PUSHBULLET_ACCESS_TOKEN=your_token_here
```

**Never commit the `.env` file to GitHub.**

Add it to `.gitignore`:

```gitignore
.env
captured_images/
attendance/
__pycache__/
*.pyc
```

### 5. Upload Arduino Code

Open the Arduino sketch:

```text
arduino/door_lock.ino
```

Open it using **Arduino IDE**, select the correct board and COM port, and upload the program.

### 6. Connect the Hardware

Connect the servo motor to the Arduino according to the pin configuration defined in the Arduino sketch.

Example:

```text
Arduino
   │
   ├── USB ───────── Computer
   │
   └── Servo Motor
          │
          └── Door Lock
```

### 7. Configure the Serial Port

Update the Python configuration with the serial port used by your Arduino.

Example:

```python
SERIAL_PORT = "COM3"
BAUD_RATE = 9600
```

For Linux/macOS, the port may look like:

```text
/dev/ttyUSB0
```

or:

```text
/dev/cu.usbmodem...
```

### 8. Run the System

```bash
python main.py
```

The webcam should start and the system will begin monitoring for faces.

---

## 🔐 Security Logic

The system follows a layered verification approach:

```text
                 Face Detected
                       │
                       ▼
              Is Face Recognized?
                 /           \
               No             Yes
               │               │
               ▼               ▼
        Unauthorized      Anti-Spoofing
           Alert              Checks
                               │
                         ┌─────┴─────┐
                         │           │
                       Pass         Fail
                         │           │
                         ▼           ▼
                    Unlock Door   Keep Locked
                         │           │
                         ▼           ▼
                    Log Entry    Send Alert
```

This ensures that **face recognition alone is not sufficient to unlock the door**.

---

## 📲 Unauthorized Access Notification

When an unknown or suspicious face is detected, the system captures an image and sends an alert through Pushbullet.

Example notification:

```text
⚠️ Unauthorized Access Attempt

An unknown or suspicious person was detected
at the door.

Captured image attached.
```

This allows the owner to be immediately informed of potential access attempts.

---

## 📝 Attendance Logging

Authorized access events can be recorded with information such as:

```text
Name, Date, Time, Status
Alice, 2026-08-27, 09:15:23, Authorized
Bob,   2026-08-27, 09:42:11, Authorized
```

This provides a simple mechanism for maintaining an access/attendance history.

---

## 🛡️ Security & Privacy

This project is intended primarily for **educational and prototype purposes**.

### Privacy

* Real face images should not be committed to public repositories.
* Captured unauthorized-access images should be stored securely.
* Access logs may contain personally identifiable information and should be protected.

### API Security

Never hard-code your Pushbullet token:

❌ Avoid:

```python
TOKEN = "your-secret-token"
```

✅ Prefer:

```python
import os

TOKEN = os.getenv("PUSHBULLET_ACCESS_TOKEN")
```

### Repository Security

Add sensitive files to `.gitignore`:

```gitignore
.env
known_faces/
captured_images/
attendance/
```

---

## ⚠️ Limitations

Although the project implements multiple anti-spoofing techniques, these methods are **not equivalent to professional biometric liveness detection**.

Performance may be affected by:

* Poor lighting
* Camera quality
* Strong reflections
* Face angle
* Facial occlusion
* Multiple people in the frame
* Camera positioning
* Similar-looking individuals
* Different types of display/print attacks

For a production security system, dedicated hardware and more advanced liveness-detection techniques should be considered.

---

## 🔮 Future Improvements

Possible improvements include:

* 🎯 Deep-learning-based liveness detection
* 👁️ Eye-blink detection
* 🧠 CNN-based anti-spoofing
* 👤 Multi-person detection
* 📱 Mobile application for remote monitoring
* 🔔 Additional notification channels
* 🗄️ Database-based access logging
* 🔐 Encrypted access records
* 📊 Web dashboard for attendance
* 🪪 RFID + face-recognition dual authentication
* 🔑 PIN + face-recognition authentication
* ☁️ Cloud-based monitoring
* 📷 Higher-quality camera integration
* 🚨 Tamper detection and alarm system

---

## 📊 Project Advantages

| Feature               | Benefit                            |
| --------------------- | ---------------------------------- |
| Face Recognition      | Identifies authorized users        |
| Anti-Spoofing         | Reduces basic photo/screen attacks |
| Arduino Control       | Provides physical door control     |
| Pushbullet            | Enables remote security alerts     |
| Attendance Logging    | Maintains access history           |
| Environment Variables | Protects API credentials           |
| Modular Design        | Easier maintenance and extension   |

---

## 🎯 Use Cases

This prototype can be adapted for:

* 🏠 Smart home entry systems
* 🏢 Office access control
* 🧪 Academic security projects
* 🏫 Laboratory access management
* 🏢 Attendance systems
* 🔬 Computer-vision demonstrations
* 🚪 Small-scale smart-lock prototypes

---

## 👨‍💻 Project Objective

The main objective of this project is to demonstrate how **computer vision, facial recognition, anti-spoofing techniques, IoT-style hardware control, and real-time notifications** can be combined to create a smarter access-control system.

The project focuses on providing an additional verification layer rather than relying solely on conventional face recognition.

---

## 📜 Disclaimer

This project is developed for **educational and research purposes**.

It should not be considered a replacement for professionally certified access-control or biometric security systems. Real-world deployment should include appropriate security testing, fail-safe mechanisms, privacy protections, and hardware safeguards.

---

## ⭐ Contributing

Contributions and improvements are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test the changes.
5. Submit a pull request.

---

## 📄 License

Add the license appropriate for your project. For example:

```text
MIT License
```

---

## ⭐ Acknowledgements

This project makes use of:

* **OpenCV** for computer vision
* **face_recognition** for facial identification
* **Arduino** for hardware control
* **Pushbullet** for security notifications

---

### 🔐 In Short

```text
Camera
   ↓
Face Detection
   ↓
Face Recognition
   ↓
Anti-Spoofing Verification
   ↓
┌───────────────────────────┐
│                           │
▼                           ▼
Authorized + Real       Unknown/Spoof
│                           │
▼                           ▼
Unlock Door             Keep Locked
│                           │
▼                           ▼
Log Entry              Capture Image
                            │
                            ▼
                     Push Notification
```

**A simple, modular prototype for combining facial recognition with physical access control and anti-spoofing verification.**
