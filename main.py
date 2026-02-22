import telebot
import time
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
API_TOKEN = '8530900754:AAH-xyYJ1etm88QW2A_O3CabD5heC0-1Asc' # নিশ্চিত করুন এটি আলাদা টোকেন
STORAGE_CHANNEL_ID = -1003319645639 # আপনার দেওয়া আইডি
DELETE_AFTER = 600 # ১০ মিনিট (৬০০ সেকেন্ড)

bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = Flask('')

@app.route('/')
def home():
    return "Alpha Vault with Auto-Delete is Active!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- অটো ডিলিট ফাংশন ---
def auto_delete(chat_id, message_id):
    time.sleep(DELETE_AFTER)
    try:
        bot.delete_message(chat_id, message_id)
        print(f"Message {message_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting message: {e}")

# --- ফাইল পাঠানো এবং ডিলিট শিডিউল করা ---
@bot.message_handler(commands=['start'])
def send_file(message):
    file_msg_id = 43 # আপনার চ্যানেলের মেসেজ আইডি
    
    try:
        # ফাইলটি চ্যানেল থেকে কপি করে পাঠানো
        sent_msg = bot.copy_message(
            chat_id=message.chat.id, 
            from_chat_id=STORAGE_CHANNEL_ID, 
            message_id=file_msg_id
        )
        
        bot.send_message(message.chat.id, "🎬 **ভিডিওটি পাঠানো হয়েছে!**\n\nএটি ১০ মিনিট পর অটোমেটিক ডিলিট হয়ে যাবে। এখনই দেখে নিন।", parse_mode="Markdown")
        
        # অটো ডিলিট চালু করা
        t = Thread(target=auto_delete, args=(message.chat.id, sent_msg.message_id))
        t.start()
        
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "❌ ফাইলটি পাওয়া যায়নি। বটকে চ্যানেলে এডমিন দিন।")

if __name__ == "__main__":
    keep_alive() # রেন্ডারের স্লিপ মোড প্রতিরোধ
    print("Storage Bot Starting...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
