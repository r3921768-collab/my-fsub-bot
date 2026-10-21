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

# TAMARI BANE CHANNEL NI LINK AHIYA LAKHO
CHANNEL_1_LINK = "https://t.me/movie_series0012"
CHANNEL_2_LINK = "https://t.me/movieseries0453"
CHANNEL_NAME = "Movie & series 🤩"

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n🎬 Send me the name of the movie or series you are looking for, and I will find it for you!"
    )

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def auto_filter(client, message):
    query = message.text
    
    # Banne channel na buttons ahiya set karya chhe
    buttons = [
        [InlineKeyboardButton("📦 [1.37 GB] High Quality 1080p", callback_data="file_1")],
        [InlineKeyboardButton("📦 [597.74 MB] Medium Quality 720p", callback_data="file_2")],
        [
            InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1_LINK),
            InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2_LINK)
        ]
    ]
    
    await message.reply_text(
        f"🎬 **{CHANNEL_NAME}**\n\n🔍 Search Query: **{query}**\n\n*Tap on the buttons below to get your files or join channels...*\n\n⏳ Note: Files will be auto-deleted in 5 minutes.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    app.run()
    
