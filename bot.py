import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
import config

# Logging setup
logging.basicConfig(level=logging.INFO)

# Pyrogram Bot Client setup
app = Client(
    "AutoFilterBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,  # String ma hovu joiye
    bot_token=config.BOT_TOKEN
)

# Function to check if user joined both FSUB channels
async def check_fsub(client, user_id):
    # Check Channel 1
    try:
        await client.get_chat_member(config.FSUB_CHANNEL_1, user_id)
    except UserNotParticipant:
        return 1  # Not joined channel 1
    except Exception:
        pass

    # Check Channel 2
    try:
        await client.get_chat_member(config.FSUB_CHANNEL_2, user_id)
    except UserNotParticipant:
        return 2  # Not joined channel 2
    except Exception:
        pass

    return 0  # Joined both channels


# Start Command with Dual Force-Subscribe
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id

    # Check subscription status for both channels
    fsub_status = await check_fsub(client, user_id)

    if fsub_status != 0:
        # User has not joined one or both channels, send join buttons
        buttons = [
            [InlineKeyboardButton("Join Channel 1", url=f"https://t.me/{config.FSUB_CHANNEL_1}")],
            [InlineKeyboardButton("Join Channel 2", url=f"https://t.me/{config.FSUB_CHANNEL_2}")],
            [InlineKeyboardButton("🔄 Try Again", callback_data="check_subscription")]
        ]
        
        await message.reply_text(
            "⚠️ **Please join our update channels first to use this bot!**\n\n"
            "After joining both channels, click on the **Try Again** button below.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    # If user joined both channels
    await message.reply_text("👋 Welcome! You have successfully joined all channels. Now you can use the bot.")


# Callback query handler for "Try Again" button
@app.on_callback_query(filters.regex("check_subscription"))
async def cb_try_again(client, callback_query):
    user_id = callback_query.from_user.id
    fsub_status = await check_fsub(client, user_id)

    if fsub_status != 0:
        await callback_query.answer("❌ You still haven't joined both channels!", show_alert=True)
    else:
        await callback_query.message.delete()
        await callback_query.message.reply_text("✅ Thank you for joining! You can now use the bot.")


# Run the bot
if __name__ == "__main__":
    app.run()
    
