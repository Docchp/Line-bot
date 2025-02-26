from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage
import random
import os
from dotenv import load_dotenv

# โหลดตัวแปรจากไฟล์ .env (ถ้ามี)
load_dotenv()

# ใช้ Channel Access Token และ Channel Secret จาก Environment Variable
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# คำตอบสำหรับกิจกรรมวาดรูป
DRAWING_WORDS = ["ช้าง", "ผีเสื้อ", "ปลา", "แอปเปิ้ล", "กล้วย", "หวี", "ต้นไม้", "ดินสอ"]
IMAGE_RESPONSES = [
    "คุณมีความละเอียดและความคิดสร้างสรรค์ที่น่าทึ่ง",
    "ฉันรู้สึกชื่นชมผลงานของคุณมากจริงๆ ค่ะ"
]

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_text = event.message.text.strip()

    if user_text == "11":
        reply_text = random.choice(DRAWING_WORDS)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    reply_text = random.choice(IMAGE_RESPONSES)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

if __name__ == "__main__":
    app.run(debug=True)
