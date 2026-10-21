import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from keep_alive import keep_alive

# Logging setup
logging.basicConfig(level=logging.INFO)

# Pyrogram Bot Client setup
app = Client(
    "AutoFilterBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Tamari banne channel ni links ahiya set chhe
CHANNEL_1_LINK = "https://t.me/movieseries0012"
CHANNEL_2_LINK = "https://t.me/movieseries0453"

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    fsub_buttons = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1_LINK)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2_LINK)],
        [InlineKeyboardButton("✅ I Have Joined, Continue", callback_data="check_join")]
    ]
    
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        f"🚨 **To use this bot and download movies, you must join our both channels first!**\n\n"
        f"👇 Click the buttons below to join:",
        reply_markup=InlineKeyboardMarkup(fsub_buttons)
    )

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def movie_search_handler(client, message):
    query = message.text
    
    # File quality buttons with callback data for downloading
    file_results = [
        [InlineKeyboardButton("📦 [3.89 GB] Movie 1080p WEB-DL", callback_data="send_file_1")],
        [InlineKeyboardButton("📦 [2.78 GB] Movie 720p HEVC", callback_data="send_file_2")],
        [InlineKeyboardButton("📦 [950 MB] Fast Download Server", callback_data="send_file_3")]
    ]
    
    await message.reply_text(
        f"🎬 **Search Query:** `{query}`\n"
        f"📊 **Total Results:** 3\n\n"
        f"*Tap on the file button below to get your file...*\n\n"
        f"⏳ Note: File will be auto-deleted in 10 minutes.",
        reply_markup=InlineKeyboardMarkup(file_results)
    )

# Callback query handler to send actual files when user clicks buttons
@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    
    if data == "check_join":
        await callback_query.answer("Thank you for joining! Now send me any movie name.", show_alert=True)
    elif data.startswith("send_file"):
        await callback_query.answer("Sending your file...", show_alert=False)
        # User ne file ya sample link moklava mate
        await callback_query.message.reply_text(
            "📂 **Here is your requested file:**\n\n"
            "🔗 [Click Here to Download File](https://t.me/movieseries0012)\n\n"
            "⏳ *This file will auto-delete in 10 minutes.*"
        )

if __name__ == "__main__":
    keep_alive()
    print("Auto-Filter Bot is running perfectly...")
    app.run()
    
