import asyncio
import logging
from pyrogram import Client, filters
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

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n🎬 Bot is online and working perfectly!"
    )

@app.on_message(filters.text & filters.private & ~filters.command("start"))
async def auto_filter(client, message):
    query = message.text
    await message.reply_text(f"🔍 Searching for **'{query}'**...")

async def main():
    # Start web server for Render port binding in background
    keep_alive()
    print("Bot is starting with asyncio...")
    # Start Pyrogram client properly
    await app.start()
    print("Bot started successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
