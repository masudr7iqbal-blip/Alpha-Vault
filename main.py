from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# --- আপনার তথ্য ---
API_ID = 30814403
API_HASH = "5e147d0140da75e56aa54988ad5df6db"
BOT_TOKEN = "8474826429:AAEH6Dq-e69ucf0keQ8PButpgmexUEE1tqo"
CHANNEL_ID = -1003319645639
ADMIN_ID = 5716499834 

app = Client("AlphaVault", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    # ইউজার লিঙ্কে ক্লিক করলে /start 123 ফরম্যাটে আসবে
    if len(message.command) > 1:
        file_id = int(message.command[1])
        
        # ১. চ্যানেল থেকে ভিডিওটি কপি করে ইউজারকে পাঠানো (চ্যানেলে এটি থেকে যাবে)
        sent_video = await client.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=file_id
        )
        
        # ২. ভিডিওর নিচে অটো-ডিলিট ওয়ার্নিং দেওয়া
        warning_msg = await message.reply_text(
            "⏳ **This content is available for only 10 minutes!**\n"
            "After that, it will be auto-deleted from your chat 🚫\n"
            "Save & Download now to keep it forever! 🔥"
        )
        
        # ৩. ১০ মিনিট (৬০০ সেকেন্ড) অপেক্ষা
        await asyncio.sleep(600)
        
        # ৪. ইউজারের ইনবক্স থেকে ভিডিও ও মেসেজ ডিলিট করা
        try:
            await sent_video.delete()
            await warning_msg.delete()
        except:
            pass
    else:
        await message.reply_text("🔞 **Alpha Vault Storage Active**\nঅ্যাডমিন ফাইল পাঠালে লিঙ্ক তৈরি হবে।")

@app.on_message((filters.video | filters.photo | filters.document) & filters.user(ADMIN_ID))
async def save_media(client, message):
    # ফাইলটি চ্যানেলে কপি করা (স্থায়ী স্টোরেজ)
    sent_msg = await message.copy(CHANNEL_ID)
    
    bot_info = await client.get_me()
    # ইউজারের জন্য লিঙ্ক তৈরি
    share_link = f"https://t.me/{bot_info.username}?start={sent_msg.id}"
    
    await message.reply_text(
        f"✅ **Content Saved!**\n\n🔗 **User Link:** `{share_link}`",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🚀 কন্টেন্ট টেস্ট করুন", url=share_link)
        ]])
    )

app.run()
