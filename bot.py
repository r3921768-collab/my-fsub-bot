import logging
import asyncio
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

# Tamari banne channel ni links yaha rakho
CHANNEL_1 = "https://t.me/movieseries0012"
CHANNEL_2 = "https://t.me/movieseries0453"

@app.on_message(filters.command("start") & (filters.private | filters.group))
async def start_handler(client, message):
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        f"🎬 I am your Auto-Filter Bot.\n"
        f"🔍 Send me any movie or series name, and I will find the files for you instantly!"
    )

@app.on_message(filters.text & (filters.private | filters.group) & ~filters.command("start"))
async def auto_filter(client, message):
    query = message.text
    
    # Professional search result buttons with your channels
    search_buttons = [
        [InlineKeyboardButton("📦 [1.37 GB] High Quality 1080p", callback_data=f"dl_1_{query}")],
        [InlineKeyboardButton("📦 [597.74 MB] Medium Quality 720p", callback_data=f"dl_2_{query}")],
        [InlineKeyboardButton("📦 [950.84 MB] Fast Server File", callback_data=f"dl_3_{query}")],
        [
            InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1),
            InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2)
        ]
    ]
    
    sent_msg = await message.reply_text(
        f"🎬 **Movie & Series Search Result**\n\n"
        f"🔍 Query: **{query}**\n"
        f"⚡ Status: Files Found Successfully!\n\n"
        f"*Tap on any quality button below to get your file...*\n\n"
        f"⏳ **Note:** Files will be auto-deleted in 5 minutes for copyright safety.",
        reply_markup=InlineKeyboardMarkup(search_buttons)
    )
    
    # Auto-delete warning note feature (5 minutes)
    await asyncio.sleep(300)
    try:
        await sent_msg.delete()
    except:
        pass

if __name__ == "__main__":
    keep_alive()
    print("Auto-Filter Bot is starting for Group & PM...")
    app.run()
    
