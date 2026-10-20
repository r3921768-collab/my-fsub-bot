import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import config
from keep_alive import keep_alive

# Logging setup
logging.basicConfig(level=logging.INFO)

# Pyrogram Bot Client setup with explicit bot_token
app = Client(
    "AutoFilterBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Function to check if user joined both FSUB channels
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
            [InlineKeyboardButton("📢 Join Channel 1", url=f"https://t.me/c/{str(config.FSUB_CHANNEL_1)[4:]}")],
            [InlineKeyboardButton("📢 Join Channel 2", url=f"https://t.me/c/{str(config.FSUB_CHANNEL_2)[4:]}")],
            [InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{client.me.username}?start=start")]
        ]
        await message.reply_text(
            "⚠️ **Please join both of our update channels below to use this bot!**\n\nAfter joining both channels, click 'Try Again'.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\nI am your custom Auto-Filter bot. Send me the name of the movie or file you are looking for!"
    )

# Start web server for Render port binding
keep_alive()

# Run the bot
print("Bot is starting...")
app.run()
