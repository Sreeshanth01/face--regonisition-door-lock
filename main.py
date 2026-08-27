import warnings
warnings.filterwarnings("ignore", category=UserWarning)
#  Face recog door lock system (py code)

import face_recognition
import cv2
import pickle
import os
import time
import serial
import pyttsx3
import numpy as np
import csv
from pushbullet import Pushbullet
from datetime import datetime

# Config
ENCODINGS_FILE = "encodings.face"
CAMERA_INDEX = 0
TOLERANCE = 0.45
MODEL = "hog"
SERIAL_PORT = "COM3"
BAUD_RATE = 115200
UNLOCK_DURATION = 10
PREVIEW_DURATION = 5
DISPLAY_DURATION = 5
VOICE_RATE = 170
CAMERA_DELAY = 0.0
APPROVAL_TIMEOUT = 60
CAMERA_WARMUP = 2
ATTENDANCE_FILE = "attendance.csv"
PUSHBULLET_API_KEY = "o.LEm9i6Ya9y5IWRPiQAwoS6x2viF0nFso"
# ---------------


def speak(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', VOICE_RATE)
    engine.say(message)
    engine.runAndWait()


def log_attendance(name, access_type="Local", remarks="Authorized Access Granted"):
    """Record attendance to CSV file."""
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    file_exists = os.path.exists(ATTENDANCE_FILE)
    with open(ATTENDANCE_FILE, "a", newline="") as csvfile:
        fieldnames = ["Name", "Date", "Time", "Access Type", "Remarks"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Name": name,
            "Date": date,
            "Time": time_str,
            "Access Type": access_type,
            "Remarks": remarks
        })
    print(f"📝 Attendance recorded for {name} at {time_str}.")


def load_known_faces():
    if not os.path.exists(ENCODINGS_FILE):
        print(f"⚠ '{ENCODINGS_FILE}' not found! Please run 'train_faces.py' first.")
        exit()
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    print(f"✅ Loaded {len(data['encodings'])} known faces.")
    return data["encodings"], data["names"]


def connect_arduino(retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)
            print(f"✅ Connected to Arduino on {SERIAL_PORT}")
            return ser
        except Exception as e:
            print(f"⚠ Attempt {attempt}: Could not connect to Arduino ({e})")
            time.sleep(delay)
    print("❌ Failed to connect to Arduino after retries.")
    return None


def send_arduino_command(ser, cmd):
    if not ser:
        print("⚠ Serial not available.")
        return False
    try:
        ser.write((cmd.upper().strip() + "\n").encode("utf-8"))
        ser.flush()
        print(f"📤 Sent to Arduino: {cmd}")
        return True
    except Exception as e:
        print(f"❌ Failed to send to Arduino: {e}")
        return False


def send_pushbullet_notification(pb, title, message, img_path=None):
     
    try:
        if pb is None:
            return
        if img_path and os.path.exists(img_path):
            with open(img_path, "rb") as f:
                file_data = pb.upload_file(f, os.path.basename(img_path))
            pb.push_file(file_data, body=message, title=title)
         else:
            pb.push_note(title, message)
        print(f"📱 Pushbullet notification sent: {title}")
    except Exception as e:
        print(f"❌ Failed to send Pushbullet notification: {e}")


def wait_for_approval(pb, timeout=60, since_time=None):
    print(f"⏳ Waiting up to {timeout}s for Pushbullet reply...")
    start = time.time()
    latest_ts = since_time if since_time else start
    while time.time() - start < timeout:
        try:
            pushes = pb.get_pushes(modified_after=latest_ts)
        except Exception as e:
            print(f"⚠ Pushbullet API error: {e}")
            time.sleep(3)
            continue
        for push in pushes:
            msg = (push.get("body") or "").strip().lower()
            created = push.get("created", 0)
            if created > latest_ts and msg:
                if "approve" in msg or "accept" in msg:
                    return True
                if "deny" in msg or "reject" in msg:
                    return False
        time.sleep(3)
    print("⌛ No reply received.")
    return False


# Anti Glare
def detect_photo_glare(frame):
    """
    Detect possible phone/photo glare:
    - Detects small concentrated bright spots.
    - Ignores evenly bright natural lighting.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, bright_mask = cv2.threshold(gray_blur, 240, 255, cv2.THRESH_BINARY)
    glare_area = np.sum(bright_mask == 255)
    total_area = frame.shape[0] * frame.shape[1]
    glare_ratio = glare_area / total_area
    avg_brightness = np.mean(gray)

    if avg_brightness > 180 and glare_ratio < 0.08:
        return False, glare_ratio
    elif glare_ratio > 0.015 and avg_brightness < 230:
        return True, glare_ratio
    else:
        return False, glare_ratio


# Face recognition
def main():
    known_encodings, known_names = load_known_faces()
    ser = connect_arduino()

    try:
        pb = Pushbullet(PUSHBULLET_API_KEY)
        print("✅ Connected to Pushbullet API.")
    except Exception as e:
        pb = None
        print(f"⚠ Pushbullet not available: {e}")

    video = cv2.VideoCapture(CAMERA_INDEX)
    if not video.isOpened():
        print("❌ Cannot open webcam.")
        return

    print(f"🎥 Camera warming up for {CAMERA_WARMUP}s to adjust focus/exposure...")
    time.sleep(CAMERA_WARMUP)
    print("✅ Camera ready. Starting detection...")

    access_granted = False
    authorized_name = "Unknown"
    start_time = time.time()

    while (time.time() - start_time) < PREVIEW_DURATION:
        ret, frame = video.read()
        if not ret:
            continue

        # Glare check
        glare_detected, glare_ratio = detect_photo_glare(frame)
        if glare_detected:
            cv2.putText(frame, f"⚠ Possible Photo Glare ({glare_ratio*100:.1f}%)", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("🔐 Face Recognition Door Lock", frame)
            print(f"⚠ Glare detected ({glare_ratio*100:.2f}%) — possible photo spoof attempt.")
            speak("Glare detected. Possibly a photo. Access denied.")
            send_arduino_command(ser, "REJECT")

            # Pushbullet glare notif
            if pb:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                img_filename = f"glare_alert_{timestamp}.jpg"
                cv2.imwrite(img_filename, frame)
                send_pushbullet_notification(
                    pb,
                    title="⚠ Possible Photo Spoof Detected",
                    message=f"Glare detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Possible photo or screen spoof.",
                    img_path=img_filename
                )
                os.remove(img_filename)

            time.sleep(2)
            continue  # Skip face recognition when glare found

        # Face recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model=MODEL)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=TOLERANCE)
            if True in matches:
                match_index = matches.index(True)
                authorized_name = known_names[match_index]
                access_granted = True
            else:
                authorized_name = "Unknown"

            color = (0, 255, 0) if access_granted else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, authorized_name, (left + 5, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("🔐 Face Recognition Door Lock", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # If accepted
    if access_granted:
        speak(f"Access Granted. Welcome {authorized_name}.")
        print(f"🔓 Access Granted. Welcome {authorized_name}.")
        send_arduino_command(ser, "ACCEPT")

        # Attendance
        log_attendance(authorized_name, access_type="Local", remarks="Authorized Access Granted")

        # Send notif
        if pb:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_pushbullet_notification(
                pb,
                title="✅ Authorized Access Granted",
                message=f"{authorized_name} accessed the door at {timestamp}."
            )

        time.sleep(UNLOCK_DURATION)
        speak("Door locked.")
        print("🔒 Door locked automatically.")
    else:
        # Unauthorized
        print("🚨 Unknown face detected!")
        speak("Unknown person detected. Sending alert.")
        send_arduino_command(ser, "REJECT")
        if pb:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_filename = f"unknown_{timestamp}.jpg"
            ret, snapshot = video.read()
            if ret:
                cv2.imwrite(img_filename, snapshot)
                send_pushbullet_notification(
                    pb,
                    title="🚨 Unknown Person Detected",
                    message="An unknown person was detected. Reply 'approve' or 'deny' within 60s.",
                    img_path=img_filename
                )
                alert_time = time.time()
                approved = wait_for_approval(pb, timeout=APPROVAL_TIMEOUT, since_time=alert_time)
                os.remove(img_filename)
            else:
                approved = False

            if approved:
                speak("Access approved remotely.")
                print("✅ Remote approval received — granting access.")
                send_arduino_command(ser, "ACCEPT")
                log_attendance("Remote Approval", access_type="Remote", remarks="Access Approved via Pushbullet")
                time.sleep(UNLOCK_DURATION)
                send_arduino_command(ser, "REJECT")
                speak("Door locked.")
            else:
                speak("Access denied. Door remains locked.")
                print("❌ Access denied — no unlock action taken.")
        else:
            speak("Access denied. Pushbullet not configured.")

    video.release()
    cv2.destroyAllWindows()
    if ser:
        ser.close()
    print("✅ System closed successfully.")


if __name__ == "__main__":
    main()
