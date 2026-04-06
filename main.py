
import os
from flask import Flask
from threading import Thread
import telebot
import random

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

messages = [
    "🦅 Falcons جاهز للمضاربة",
    "🚀 تم تشغيل البوت بنجاح",
    "📡 بدء مراقبة السوق",
]

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, random.choice(messages))

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
