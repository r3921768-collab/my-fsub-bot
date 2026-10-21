import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from keep_alive import keep_alive

# Logging setup
logging.basicConfig(level=logging.INFO)

# Pyrogram Bot Client setup (Naya Bot Instance)
app = Client(
    "LuckyNewBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Tamari banne channels
CHANNEL_1 = "https://t.me/movieseries0012"
CHANNEL_2 = "https://t.me/movieseries0453"

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2)],
        [InlineKeyboardButton("✅ I Have Joined, Continue", callback_data="verified")]
    ]
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        f"🎬 Welcome to **Lucky Bot**.\n"
        f"🚨 **To use this bot, please join our both channels first:**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def search_movie(client, message):
    query = message.text
    
    # Naya clean quality buttons
    file_buttons = [
        [InlineKeyboardButton("📦 [3.89 GB] Full HD 1080p", callback_data="dl_1")],
        [InlineKeyboardButton("📦 [2.78 GB] HD 720p", callback_data="dl_2")],
        [InlineKeyboardButton("📦 [950 MB] Fast Server", callback_data="dl_3")]
    ]
    
    await message.reply_text(
        f"🎬 **Search Results for:** `{query}`\n\n"
        f"👇 *Tap any quality button below to get your file:*",
        reply_markup=InlineKeyboardMarkup(file_buttons)
    )

@app.on_callback_query()
async def callbacks(client, query):
    if query.data == "verified":
        await query.answer("Thank you! Now send me any movie name.", show_alert=True)
    elif query.data.startswith("dl_"):
        await query.answer("Here is your file link!", show_alert=False)
        await query.message.reply_text(
            "📂 **Your file is ready:**\n\n"
            "🔗 [Click Here to Download](https://t.me/movieseries0012)\n\n"
            "⏳ *Auto-deletes in 10 minutes.*"
        )

if __name__ == "__main__":
    keep_alive()
    print("New Lucky Bot is starting fresh...")
    app.run()
    
    
