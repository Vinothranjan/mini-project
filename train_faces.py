import cv2
import os
import time

def capture_faces():
    # Create directory if it doesn't exist
    if not os.path.exists('known_faces'):
        os.makedirs('known_faces')

    name = input("Enter the name of the person: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print(f"Capturing faces for {name}. Look at the camera.")
    print("Press 'c' to capture a photo. Capture at least 5 photos for better accuracy.")
    print("Press 'q' to finish.")

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('Training Phase - Capture Faces', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            timestamp = int(time.time())
            filename = f"known_faces/{name}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            count += 1
            print(f"Captured {count}: {filename}")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Training finished. {count} photos captured for {name}.")

if __name__ == "__main__":
    capture_faces()
