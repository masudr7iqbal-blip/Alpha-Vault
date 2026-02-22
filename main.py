import telebot
import asyncio
import threading
from telebot import types

# --- আপনার তথ্যসমূহ ---
API_TOKEN = '8474826429:AAEH6Dq-e69ucf0keQ8PButpgmexUEE1tqo'
CHANNEL_ID = -1003319645639 # আপনার স্থায়ী স্টোরেজ চ্যানেল আইডি
ADMIN_ID = 5716499834 

bot = telebot.TeleBot(API_TOKEN)

# অটো-ডিলিট ফাংশন
def auto_delete(chat_id, video_id, warning_id):
    import time
    time.sleep(600) # ১০ মিনিট (৬০০ সেকেন্ড)
    try:
        bot.delete_message(chat_id, video_id)
        bot.delete_message(chat_id, warning_id)
    except:
        pass

@bot.message_handler(commands=['start'])
def start(message):
    text = message.text.split()
    # যদি ইউজার লিঙ্কের মাধ্যমে আসে (যেমন: /start 123)
    if len(text) > 1:
        file_id = text[1]
        try:
            # ১. চ্যানেল থেকে ফাইলটি কপি করে ইউজারকে পাঠানো
            sent_video = bot.copy_message(message.chat.id, CHANNEL_ID, int(file_id))
            
            # ২. অটো-ডিলিট ওয়ার্নিং মেসেজ
            warning_msg = bot.send_message(
                message.chat.id,
                "⏳ **This content is available for only 10 minutes!**\n"
                "After that, it will be auto-deleted from your chat 🚫\n"
                "Save & Download now to keep it forever! 🔥",
                parse_mode="Markdown"
            )
            
            # ৩. ডিলিট করার জন্য আলাদা থ্রেড চালানো
            threading.Thread(target=auto_delete, args=(message.chat.id, sent_video.message_id, warning_msg.message_id)).start()
            
        except Exception as e:
            bot.reply_to(message, "❌ ফাইলটি পাওয়া যায়নি বা কোনো সমস্যা হয়েছে।")
    else:
        bot.reply_to(message, "🔞 **Alpha Vault Storage Active**\nঅ্যাডমিন ফাইল পাঠালে লিঙ্ক তৈরি হবে।")

# অ্যাডমিন ফাইল পাঠালে লিঙ্ক তৈরি করা
@bot.message_handler(content_types=['video', 'photo', 'document'])
def handle_admin_files(message):
    if message.from_user.id == ADMIN_ID:
        try:
            # ফাইলটি চ্যানেলে সেভ করা
            sent_msg = bot.copy_message(CHANNEL_ID, message.chat.id, message.message_id)
            
            bot_info = bot.get_me()
            # শেয়ার লিঙ্ক তৈরি
            share_link = f"https://t.me/{bot_info.username}?start={sent_msg.message_id}"
            
            bot.reply_to(message, f"✅ **Content Saved!**\n\n🔗 **User Link:** `{share_link}`")
        except Exception as e:
            bot.reply_to(message, f"❌ এরর: বটকে চ্যানেলে অ্যাডমিন করেছেন তো?\n{e}")

if __name__ == "__main__":
    bot.infinity_polling()
