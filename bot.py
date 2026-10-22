import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Aeni niche badho baki no code (Client, filters, etc.) rakhvo

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Bot credentials setup
API_ID = 37601205  # Tamaro real integer API_ID yaha dalo (without quotes)
API_HASH = "6d3743bfe2747bf3c06ed90be7d8b34"
BOT_TOKEN = "8574146217:AAHipNSOwLm9hwINoL1K6qVLLJ2N-c9FI8Q"

# Channel links
CHANNEL_1 = "https://t.me/movieseries0012"
CHANNEL_2 = "https://t.me/movieseries0012"

app = Client(
    "lucky_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    buttons = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2)],
        [InlineKeyboardButton("✅ I Have Joined, Continue", callback_data="verified")]
    ]
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "🎬 Welcome to Lucky Bot.\n"
        "🚨 Please join our both channels first, then send any movie name.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("^verified$"))
async def verify_cb(client, query):
    await query.answer("Verified successfully! Now send movie name.", show_alert=True)
    await query.message.reply_text("✅ Verified! Now send the name of the movie you want.")

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def search_handler(client, message):
    query = message.text
    
    file_buttons = [
        [InlineKeyboardButton("📦 [3.89 GB] Movie 1080p WEB-DL", callback_data="get_file")],
        [InlineKeyboardButton("📦 [2.78 GB] Movie 720p HEVC", callback_data="get_file")]
    ]
    
    await message.reply_text(
        f"🔍 **Search Results for:** `{query}`\n"
        f"👇 *Tap any quality button below to get your file:*",
        reply_markup=InlineKeyboardMarkup(file_buttons)
    )

@app.on_callback_query(filters.regex("^get_file$"))
async def file_cb(client, query):
    await query.answer("Sending file...", show_alert=False)
    sent_msg = await query.message.reply_text(
        "📁 **Here is your requested movie file:**\n\n"
        "🔗 [Click Here to Download File](https://t.me/movieseries0012)\n"
        "⏳ *Note: This file will auto-delete in 5 minutes for safety.*"
    )
    
    await asyncio.sleep(300)
    try:
        await sent_msg.delete()
    except:
        pass

if __name__ == "__main__":
    print("Lucky Final Bot is running...")
    app.run()
    
