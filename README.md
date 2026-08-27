Anti glare face recognition door lock based system (dual verification via pushbullet) Project Summary

This project implements a smart door lock system that uses face recognition with anti-spoofing techniques to ensure that only real, authorized users can unlock the door. It combines computer vision (Python & OpenCV) with Arduino-controlled hardware to provide secure and reliable access control. To prevent spoofing attempts such as photo or screen attacks, the system performs glare detection, motion analysis, and texture checks before granting access. When an unauthorized person is detected, the system captures an image and sends a Pushbullet notification to the owner. Authorized access events are automatically logged for attendance and monitoring purposes.

Key Features

Real-time face recognition using OpenCV and face_recognition Anti-spoofing using glare detection, motion analysis, and texture quality checks Arduino-controlled servo motor for door locking mechanism Pushbullet notifications with captured images for unauthorized access Automatic attendance logging for authorized users Modular, well-structured, and easy-to-understand codebase

How It Works

The camera captures a live video feed. Face detection and anti-spoofing checks are applied. If the face is authorized and passes anti-spoofing → door unlocks. If an unknown or spoofing attempt is detected → image is captured and sent via Pushbullet. Authorized access details are logged into an attendance file.

Security & Privacy

Real face images are excluded from the public repository for privacy. Pushbullet API keys are managed using environment variables. The project is intended for educational and prototype use.

Materials Required Software

Python (3.7 or higher) Arduino IDE OpenCV and face recognition libraries Pushbullet account (for notifications)

Hardware

Webcam (for face capture) Arduino board (e.g., Arduino UNO) Servo motor (door lock) USB cable (Arduino connection) Power supply (if required)
