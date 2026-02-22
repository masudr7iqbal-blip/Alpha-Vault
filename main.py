import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
# আপনার মেইন বটের টোকেন
API_TOKEN = '8530900754:AAFk6vnn6oM8GYNynGuon_Z0PfgdiKnhKk4'

CHANNELS = ['-1003731836152', '-1003831376808'] 
CHANNEL_LINKS = ['https://t.me/+YJGx3ZCvX1g5Yzlh', 'https://t.me/+YlNW7n3rYsE4M2Mx']

# আপনার প্রিমিয়াম ইউজারনেম ও স্টোরেজ বটের ইউজারনেম
PREMIUM_ADMIN_USERNAME = "@XpremiumB" 
STORAGE_BOT_USERNAME = "@PAlphaStorage_Bot" # আপনার স্টোরেজ বটের আসল ইউজারনেম দিন

bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = Flask('')

@app.route('/')
def home():
    return "Main Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def is_subscribed(user_id):
    for chat_id in CHANNELS:
        try:
            member = bot.get_chat_member(chat_id, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False 
    return True

@bot.message_handler(commands=['start'])
def welcome(message):
    # আপনার দেওয়া টেক্সটটি এখানে উপরে রাখা হয়েছে
    welcome_text = (
        "🔐 **Secure Your Files in Seconds!**\n"
        "📁 Videos | 📸 Photos | 📄 Documents\n"
        "🚀 Generate Safe Links Instantly with Our Drive File Bot\n"
        "💾 Keep your important files protected, anytime & anywhere!\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    if is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        demo_btn = types.InlineKeyboardButton("🎬 ফ্রি ডেমো দেখুন", url=f"https://t.me/{STORAGE_BOT_USERNAME}?start=demo")
        premium_btn = types.InlineKeyboardButton("💎 প্রিমিয়াম মেম্বারশিপ কিনুন", url=f"https://t.me/{PREMIUM_ADMIN_USERNAME}")
        markup.add(demo_btn, premium_btn)
        
        bot.send_message(
            message.chat.id, 
            f"{welcome_text}\n\n✅ **স্বাগতম {message.from_user.first_name}!**\nনিচের বাটন থেকে আপনার অপশন বেছে নিন।", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )
    else:
        markup = types.InlineKeyboardMarkup()
        for i, link in enumerate(CHANNEL_LINKS):
            markup.add(types.InlineKeyboardButton(f"Join Channel {i+1} 📢", url=link))
        markup.add(types.InlineKeyboardButton("Joined ✅", callback_data="verify"))
        
        bot.send_message(
            message.chat.id, 
            f"{welcome_text}\n\n⚠️ **এক্সেস ডিনাইড!**\nবটটি ব্যবহার করতে আমাদের চ্যানেলগুলোতে জয়েন করুন।", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )

@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "ধন্যবাদ! ✅")
            welcome(call.message)
        else:
            bot.answer_callback_query(call.id, "⚠️ আপনি এখনো সব চ্যানেলে জয়েন করেননি!", show_alert=True)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
