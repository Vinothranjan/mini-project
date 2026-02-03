import os
from telegram_alert import send_photo_question

# -----------------------------
# CONFIG
# -----------------------------
UNKNOWN_FACES_DIR = "unknown_faces"
TEST_IMAGE_NAME = "test_person.jpg"   # <-- name of the image you pasted

def main():
    photo_path = os.path.join(UNKNOWN_FACES_DIR, TEST_IMAGE_NAME)

    if not os.path.exists(photo_path):
        print("❌ Image not found!")
        print(f"👉 Please place '{TEST_IMAGE_NAME}' inside '{UNKNOWN_FACES_DIR}' folder")
        return

    print("📤 Sending unknown person photo to Telegram...")
    send_photo_question(photo_path)
    print("✅ Done")

if __name__ == "__main__":
    main()
