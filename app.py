from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
import random
import os
from dotenv import load_dotenv

# โหลดตัวแปรจากไฟล์ .env
load_dotenv()

# ใช้ Channel Access Token และ Channel Secret จาก Environment Variable
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

# ตรวจสอบว่า Token และ Secret ถูกต้อง
if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise ValueError("❌ CHANNEL_ACCESS_TOKEN หรือ CHANNEL_SECRET ไม่มีค่า กรุณาตั้งค่า Environment Variables")

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# คำตอบสำหรับกิจกรรมวาดรูป
DRAWING_WORDS = ["ช้าง", "ผีเสื้อ", "ปลา", "แอปเปิ้ล", "กล้วย", "หวี", "ต้นไม้", "ดินสอ"]
IMAGE_RESPONSES = [
    "คุณมีความละเอียดและความคิดสร้างสรรค์ที่น่าทึ่ง",
    "ฉันรู้สึกชื่นชมผลงานของคุณมากจริงๆ ค่ะ"
]

@app.route("/")
def home():
    return "Hello, Render!"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK", 200  # ✅ ต้องคืนค่า 200 เสมอ

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_text = event.message.text.strip()

    if user_text == "กิจกรรมวาดรูป":
        reply_text = random.choice(DRAWING_WORDS)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    reply_text = random.choice(IMAGE_RESPONSES)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # ✅ ใช้พอร์ต 8080 ตาม Render
    app.run(host="0.0.0.0", port=port)
