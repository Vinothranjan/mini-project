import requests

BOT_TOKEN = "  "
MOTHER_CHAT_ID = 7069132483

def send_photo_question(photo_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    caption = (
        "🚨 its vinoth\n\n"
        "❓ Do you know this person?"
    )

    with open(photo_path, "rb") as photo:
        response = requests.post(
            url,
            data={
                "chat_id": MOTHER_CHAT_ID,
                "caption": caption
            },
            files={"photo": photo}
        )

    if response.status_code == 200:
        print("✅ Photo sent to Telegram")
    else:
        print("❌ Failed to send")
        print(response.text)
