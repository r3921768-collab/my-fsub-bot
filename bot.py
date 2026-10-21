import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
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

# Function to check Force-Subscribe (FSUB)
async def check_fsub(client, user_id):
    try:
        await client.get_chat_member(config.FSUB_CHANNEL_1, user_id)
    except UserNotParticipant:
        return 1
    except Exception:
        pass

    try:
        await client.get_chat_member(config.FSUB_CHANNEL_2, user_id)
    except UserNotParticipant:
        return 2
    except Exception:
        pass

    return 0

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    fsub_status = await check_fsub(client, user_id)
    
    if fsub_status != 0:
        buttons = [
            [InlineKeyboardButton("📢 Request to Join Channel 1", url=f"https://t.me/c/{str(config.FSUB_CHANNEL_1)[4:]}")],
            [InlineKeyboardButton("📢 Request to Join Channel 2", url=f"https://t.me/c/{str(config.FSUB_CHANNEL_2)[4:]}")],
            [InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{client.me.username}?start=start")]
        ]
        await message.reply_text(
            "⚠️ **To use this bot, you must join our update channels first!**\n\nClick below to send join requests, then click 'Try Again'.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n🎬 Send me the name of the movie or series you are looking for, and I will find it for you!"
    )

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def auto_filter(client, message):
    user_id = message.from_user.id
    fsub_status = await check_fsub(client, user_id)
    
    if fsub_status != 0:
        buttons = [
            [InlineKeyboardButton("📢 Request to Join Channel", url=f"https://t.me/c/{str(config.FSUB_CHANNEL_1)[4:]}")],
            [InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{client.me.username}?start=start")]
        ]
        await message.reply_text("⚠️ Please join our channels first before searching for files!", reply_markup=InlineKeyboardMarkup(buttons))
        return
        
    query = message.text
    
    # Simulated professional movie result buttons (similar to your video clip)
    file_buttons = [
        [InlineKeyboardButton("📦 [1.37 GB] High Quality 1080p", callback_data="file_1")],
        [InlineKeyboardButton("📦 [597.74 MB] Medium Quality 720p", callback_data="file_2")],
        [InlineKeyboardButton("📦 [950.84 MB] Fast Download File", callback_data="file_3")]
    ]
    
    await message.reply_text(
        f"🔍 Search Query: **{query}**\nTotal Results: **3**\n\n*Tap on the file button below to get the download link...*\n\n⏳ Note: Files will be auto-deleted in 10 minutes.",
        reply_markup=InlineKeyboardMarkup(file_buttons)
    )

if __name__ == "__main__":
    # Start web server in background thread for Render port binding
    keep_alive()
    print("Bot is starting...")
    # Start Pyrogram bot
    app.run()
    
