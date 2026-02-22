import telebot
import threading
import time

# --- আপনার তথ্যসমূহ ---
API_TOKEN = '8474826429:AAEH6Dq-e69ucf0keQ8PButpgmexUEE1tqo'
ADMIN_ID = 5716499834 
CHANNEL_ID = -1003319645639 

# Force Join চ্যানেল তথ্য
MUST_JOIN_CHANNEL_LINK = "https://t.me/+LFEmWRfqWmhjMmZl"
MUST_JOIN_ID = -1002341517036 # আপনার দেওয়া চ্যানেলের আইডি

bot = telebot.TeleBot(API_TOKEN)

def auto_delete(chat_id, video_id, warning_id):
    time.sleep(600) # ১০ মিনিট
    try:
        bot.delete_message(chat_id, video_id)
        bot.delete_message(chat_id, warning_id)
    except:
        pass

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(MUST_JOIN_ID, user_id)
        if member.status in ['left', 'kicked']:
            return False
        return True
    except:
        return True 

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text = message.text.split()
    
    if not is_subscribed(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Join Channel 📢", url=MUST_JOIN_CHANNEL_LINK))
        if len(text) > 1:
            markup.add(telebot.types.InlineKeyboardButton("Joined ✅", url=f"https://t.me/{bot.get_me().username}?start={text[1]}"))
        else:
            markup.add(telebot.types.InlineKeyboardButton("Joined ✅", callback_data="check_sub"))

        bot.send_message(
            message.chat.id, 
            f"👋 **Hello {message.from_user.first_name}!**\n\n"
            "🔐 **Secure Your Files in Seconds!**\n"
            "⚠️ **Access Denied!**\nজয়েন না করলে ফাইল ওপেন হবে না।",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    if len(text) > 1:
        file_id = text[1]
        try:
            sent_video = bot.copy_message(message.chat.id, CHANNEL_ID, int(file_id))
            warning_msg = bot.send_message(
                message.chat.id,
                "⏳ **This content is available for only 10 minutes!**",
                parse_mode="Markdown"
            )
            threading.Thread(target=auto_delete, args=(message.chat.id, sent_video.message_id, warning_msg.message_id)).start()
        except:
            bot.reply_to(message, "❌ ফাইলটি পাওয়া যায়নি।")
    else:
        welcome_text = (
            f"👋 **Welcome {message.from_user.first_name}!**\n\n"
            "🔐 **Secure Your Files in Seconds!**\n"
            "📁 Videos | 📸 Photos | 📄 Documents\n\n"
            "🚀 Generate Safe Links Instantly with Our Drive File Bot\n"
            "💾 Keep your important files protected, anytime & anywhere!"
        )
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_callback(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ ধন্যবাদ!")
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "⚠️ আগে জয়েন করুন!", show_alert=True)

@bot.message_handler(commands=['make_files'])
def make_files(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "📤 **Send your files now**")

@bot.message_handler(content_types=['video', 'photo', 'document'])
def handle_docs(message):
    if message.from_user.id == ADMIN_ID:
        sent_msg = bot.copy_message(CHANNEL_ID, message.chat.id, message.message_id)
        share_link = f"https://t.me/{bot.get_me().username}?start={sent_msg.message_id}"
        bot.reply_to(message, f"✅ **Content Stored!**\n\n🔗 **User Link:** `{share_link}`")

bot.infinity_polling()
