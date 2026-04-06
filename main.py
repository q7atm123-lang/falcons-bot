import os
import time
import random
from threading import Thread

from flask import Flask
import telebot

TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))  # مهم من Render

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

messages = [
    "🦅 Falcons جاهز للمضاربه",
    "🚀 تم تشغيل البوت بنجاح",
    "📡 بدء مراقبة السوق",
]

# ====== الاعدادات ======
MIN_PRICE = 1.20
MAX_PRICE = 10.00
scan_running = False

# ====== الموقع ======
@app.route("/")
def home():
    return "Bot is running"

# ====== اوامر البوت ======

# تشغيل
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, random.choice(messages))

# ايدي الشات
@bot.message_handler(commands=["id"])
def get_id(message):
    bot.reply_to(message, str(message.chat.id))

# اختبار القروب 🔥
@bot.message_handler(commands=["testgroup"])
def test_group(message):
    bot.send_message(GROUP_ID, "🔥 تم ربط القروب بنجاح")

# تنبيه تجريبي
@bot.message_handler(commands=["signal"])
def signal(message):
    text = (
        "🦅 تنبيه جديد\n\n"
        "الرمز: TEST\n"
        "السعر: 2.45\n"
        "اختراق: نعم\n"
        "السيوله: قويه\n"
        "خبر: ايجابي"
    )
    bot.send_message(GROUP_ID, text)

# الحالة
@bot.message_handler(commands=["status"])
def status(message):
    bot.reply_to(message, f"📊 البوت شغال\nالقروب: {GROUP_ID}")

# المساعدة
@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.reply_to(message,
        "/start تشغيل البوت\n"
        "/id اظهار الايدي\n"
        "/testgroup اختبار القروب\n"
        "/signal تنبيه تجريبي\n"
        "/scan تشغيل الفحص\n"
        "/stopscan ايقاف الفحص\n"
    )

# تشغيل الفحص
@bot.message_handler(commands=["scan"])
def scan(message):
    global scan_running
    scan_running = True
    bot.reply_to(message, "🚀 بدء الفحص")

# ايقاف الفحص
@bot.message_handler(commands=["stopscan"])
def stopscan(message):
    global scan_running
    scan_running = False
    bot.reply_to(message, "🛑 تم الايقاف")

# ====== فحص تجريبي ======
def fake_scan():
    while True:
        if scan_running:
            text = (
                "🦅 تنبيه اختراق\n\n"
                "سهم: ABCD\n"
                "السعر: 1.80\n"
                "سيوله قويه\n"
                "خبر ايجابي"
            )
            bot.send_message(GROUP_ID, text)
            time.sleep(20)
        time.sleep(10)

# ====== تشغيل ======
def run_bot():
    bot.remove_webhook()
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=fake_scan, daemon=True).start()
    Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
