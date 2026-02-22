import telebot
import time
from flask import Flask
from threading import Thread

# আপনার স্টোরেজ বটের টোকেন
API_TOKEN = '8530900754:AAH-xyYJ1etm88QW2A_O3CabD5heC0-1Asc' 
STORAGE_CHANNEL_ID = -1003319645639 
DELETE_AFTER = 600 # ১০ মিনিট

bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = Flask('')

@app.route('/')
def home():
    return "Storage Bot is Ready and Waiting for Video!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def delete_later(chat_id, message_id):
    time.sleep(DELETE_AFTER)
    try:
        bot.delete_message(chat_id, message_id)
    except: pass

@bot.message_handler(commands=['start'])
def handle_start(message):
    # আপনি যখন ভিডিও যোগ করবেন, তখন এই ID টি আপডেট করে দেবেন
    file_msg_id = None 
    
    if file_msg_id is None:
        bot.send_message(message.chat.id, "👋 **বট সচল আছে!**\n\nএডমিন এখনো কোনো ভিডিও সেট করেনি। ভিডিও যোগ করার পর এটি কাজ শুরু করবে।", parse_mode="Markdown")
        return

    try:
        sent_msg = bot.copy_message(message.chat.id, STORAGE_CHANNEL_ID, file_msg_id)
        bot.send_message(message.chat.id, "🎬 ভিডিওটি ১০ মিনিট পর ডিলিট হয়ে যাবে।")
        Thread(target=delete_later, args=(message.chat.id, sent_msg.message_id)).start()
    except Exception as e:
        bot.send_message(message.chat.id, "❌ ফাইল পাওয়া যায়নি।")

if __name__ == "__main__":
    keep_alive()
    print("Storage Bot is running...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
