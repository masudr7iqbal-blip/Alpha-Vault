import telebot
import threading
import time

# --- আপনার তথ্যসমূহ ---
API_TOKEN = '8474826429:AAEH6Dq-e69ucf0keQ8PButpgmexUEE1tqo'
ADMIN_ID = 5716499834 
CHANNEL_ID = -1003319645639 # আপনার ফাইল স্টোরেজ চ্যানেল

# আপনার জয়েন করানোর চ্যানেল লিঙ্ক
MUST_JOIN_CHANNEL_LINK = "https://t.me/+LFEmWRfqWmhjMmZl"
# এই চ্যানেলের সঠিক আইডি (বট অ্যাডমিন থাকলে এটি কাজ করবে)
MUST_JOIN_ID = -1002341517036 

bot = telebot.TeleBot(API_TOKEN)

# অটো-ডিলিট ফাংশন
def auto_delete(chat_id, video_id, warning_id):
    time.sleep(600) # ১০ মিনিট (৬০০ সেকেন্ড)
    try:
        bot.delete_message(chat_id, video_id)
        bot.delete_message(chat_id, warning_id)
    except:
        pass

# সাবস্ক্রিপশন চেক করার ফাংশন
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(MUST_JOIN_ID, user_id)
        if member.status in ['left', 'kicked']:
            return False
        return True
    except:
        # যদি আইডি ভুল হয় বা বট অ্যাডমিন না থাকে তবে ট্রু রিটার্ন করবে যাতে বট আটকে না যায়
        return True 

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text = message.text.split()
    
    # ১. সাবস্ক্রিপশন চেক
    if not is_subscribed(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Join Channel 📢", url=MUST_JOIN_CHANNEL_LINK))
        
        # রি-ভেরিফাই বাটন
        if len(text) > 1:
            markup.add(telebot.types.InlineKeyboardButton("Joined ✅", url=f"https://t.me/{bot.get_me().username}?start={text[1]}"))
        else:
            markup.add(telebot.types.InlineKeyboardButton("Joined ✅", callback_data="check_sub"))

        bot.send_message(
            message.chat.id, 
            f"👋 **Hello {message.from_user.first_name}!**\n\n"
            "🔐 **Secure Your Files in Seconds!**\n"
            "📁 Videos | 📸 Photos | 📄 Documents\n\n"
            "⚠️ **Access Denied!**\n"
            "ফাইলটি দেখতে আগে আমাদের চ্যানেলে জয়েন করুন।",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    # ২. জয়েন থাকলে ফাইল পাঠানো
    if len(text) > 1:
        file_id = text[1]
        try:
            sent_video = bot.copy_message(message.chat.id, CHANNEL_ID, int(file_id))
            warning_msg = bot.send_message(
                message.chat.id,
                "⏳ **This content is available for only 10 minutes!**\n"
                "After that, it will be auto-deleted from your chat 🚫",
                parse_mode="Markdown"
            )
            # ডিলিট টাইমার শুরু
            threading.Thread(target=auto_delete, args=(message.chat.id, sent_video.message_id, warning_msg.message_id)).start()
        except:
            bot.reply_to(message, "❌ ফাইলটি পাওয়া যায়নি।")
    else:
        # সাধারণ স্টার্ট মেসেজ
        welcome_text = (
            f"👋 **Hello {message.from_user.first_name}!**\n\n"
            "🔐 **Secure Your Files in Seconds!**\n"
            "🚀 Generate Safe Links Instantly with Our Drive File Bot\n"
            "💾 Keep your important files protected, anytime & anywhere!\n\n"
            "🔞 **Alpha Vault Storage Active**"
        )
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ ধন্যবাদ! আপনি এখন জয়েন করেছেন।")
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "⚠️ আপনি এখনো জয়েন করেননি!", show_alert=True)

# /make_files কমান্ড
@bot.message_handler(commands=['make_files'])
def make_files_command(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "📤 **Send your files now**")

# ফাইল হ্যান্ডলিং (অ্যাডমিন ফাইল পাঠালে)
@bot.message_handler(content_types=['video', 'photo', 'document'])
def handle_admin_files(message):
    if message.from_user.id == ADMIN_ID:
        try:
            sent_msg = bot.copy_message(CHANNEL_ID, message.chat.id, message.message_id)
            bot_info = bot.get_me()
            share_link = f"https://t.me/{bot_info.username}?start={sent_msg.message_id}"
            bot.reply_to(message, f"✅ **Content Stored!**\n\n🔗 **User Link:** `{share_link}`")
        except Exception as e:
            bot.reply_to(message, f"❌ এরর: {e}")

if __name__ == "__main__":
    bot.infinity_polling()
