# train_faces.py
import face_recognition
import os
import pickle

FACES_DIR = "faces"
ENCODINGS_FILE = "encodings.face"

def train_faces():
    known_encodings = []
    known_names = []

    if not os.path.exists(FACES_DIR):
        print(f"❌ Folder '{FACES_DIR}' not found. Please create it and add faces inside subfolders.")
        return

    print("📦 Starting training from folder:", FACES_DIR)
    for name in os.listdir(FACES_DIR):
        person_dir = os.path.join(FACES_DIR, name)
        if not os.path.isdir(person_dir):
            continue

        print(f"🧠 Processing {name}...")
        for filename in os.listdir(person_dir):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            image_path = os.path.join(person_dir, filename)
            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if len(encodings) > 0:
                    known_encodings.append(encodings[0])
                    known_names.append(name)
                    print(f"   ✅ Encoded {filename}")
                else:
                    print(f"   ⚠ No face detected in {filename}")
            except Exception as e:
                print(f"   ❌ Error reading {filename}: {e}")

    if not known_encodings:
        print("❌ No encodings found. Please check your face images.")
        return

    data = {"encodings": known_encodings, "names": known_names}
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    print(f"\n✅ Training complete! Saved {len(known_encodings)} encodings to '{ENCODINGS_FILE}'")

if __name__ == "__main__":
    train_faces()
