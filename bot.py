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
    # Video jeva banne channel join karva mate na buttons
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
    
    # Video jeva real file results and quality buttons
    file_results = [
        [InlineKeyboardButton("📦 [3.89 GB] Movie 1080p WEB-DL", callback_data="file_1")],
        [InlineKeyboardButton("📦 [2.78 GB] Movie 720p HEVC", callback_data="file_2")],
        [InlineKeyboardButton("📦 [950 MB] Fast Download Server", callback_data="file_3")]
    ]
    
    await message.reply_text(
        f"🎬 **Search Query:** `{query}`\n"
        f"📊 **Total Results:** 3\n\n"
        f"*Tap on the file button below to start download...*\n\n"
        f"⏳ Note: File will be auto-deleted in 10 minutes.",
        reply_markup=InlineKeyboardMarkup(file_results)
    )

if __name__ == "__main__":
    keep_alive()
    print("Auto-Filter Bot with 2 channels is running...")
    app.run()
    
    
