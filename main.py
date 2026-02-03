import cv2
import face_recognition
import os
import time
import numpy as np
from telegram_alert import send_photo_question

# ==========================================
# 1. SETUP
# ==========================================

# Digital Key for Guests
GUEST_QR_CODE = "WELCOME_FRIEND_2024"

qr_detector = cv2.QRCodeDetector()

# State Management
state = {
    "last_alert_time": 0,
    "qr_verified": False
}

# ==========================================
# 2. CAMERA ENGINE (Face + QR + Detection)
# ==========================================
def run_security_ai():
    print("AI System Loading...")
    
    # Ensure directories exist
    if not os.path.exists("known_faces"):
        os.makedirs("known_faces")
    if not os.path.exists("unknown_faces"):
        os.makedirs("unknown_faces")

    known_encodings = []
    known_names = []

    # Load known faces from the folder
    print("Loading known faces...")
    for file in os.listdir("known_faces"):
        if file.endswith((".jpg", ".png", ".jpeg")):
            path = f"known_faces/{file}"
            try:
                img = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(img)
                
                if encodings:
                    encoding = encodings[0]
                    known_encodings.append(encoding)
                    
                    # Extract name from filename (Name_Timestamp.jpg -> Name)
                    clean_name = file.split(".")[0]
                    if "_" in clean_name and clean_name.split("_")[-1].isdigit():
                         clean_name = "_".join(clean_name.split("_")[:-1])
                    
                    known_names.append(clean_name.capitalize())
                    print(f"Loaded: {clean_name}")
                else:
                    print(f"Warning: No face found in {file}")
            except Exception as e:
                print(f"Error loading {file}: {e}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Security System Active. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # STEP A: Check for Guest QR Code
        data, _, _ = qr_detector.detectAndDecode(frame)
        if data == GUEST_QR_CODE:
            state["qr_verified"] = True
            cv2.putText(frame, "GUEST QR VERIFIED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            state["qr_verified"] = False

        # STEP B: Face Recognition (only if QR is not used)
        if not state["qr_verified"]:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                matches = face_recognition.compare_faces(known_encodings, encoding)
                name = "Unknown Stranger"
                color = (0, 0, 255) # Red for stranger

                if True in matches:
                    # Find the best match
                    face_distances = face_recognition.face_distance(known_encodings, encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                        color = (0, 255, 0) # Green for family

                if name == "Unknown Stranger":
                    # Logic: If stranger detected, alert family (once every 2 minutes)
                    if time.time() - state["last_alert_time"] > 120:
                        timestamp = int(time.time())
                        # Save capture to unknown_faces
                        capture_path = f"unknown_faces/stranger_{timestamp}.jpg"
                        cv2.imwrite(capture_path, frame)
                        print(f"Unknown detected! Saved to {capture_path}")
                        
                        print("Unknown person! Sending Telegram alert...")
                        state["last_alert_time"] = time.time()
                        
                        # Send Alert
                        try:
                            send_photo_question(capture_path)
                        except Exception as e:
                            print(f"Telegram Error: {e}")

                # Draw Visual Box
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow('Smart Home Security (Face + QR)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

# ==========================================
# 3. EXECUTION
# ==========================================
if __name__ == "__main__":
    run_security_ai()
