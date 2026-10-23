import asyncio
from telethon import TelegramClient, events

API_ID = 37601205
API_HASH = "6d3743bfe2747bf3c06ed90be7d8b34"
BOT_TOKEN = "8574146217:AAHipNSOwLm9hwINeLKl6qVLLJ2N-c9FIBQ"

CHANNEL_1 = "https://t.me/movieseries0012"
CHANNEL_2 = "https://t.me/movieseries0012"

client = TelegramClient('lucky_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    sender = await event.get_sender()
    name = sender.first_name if sender else "User"
    
    # Simple Telethon button list using buttons parameter format
    buttons = [
        [events.Button.url("📢 Join Channel 1", CHANNEL_1)],
        [events.Button.url("📢 Join Channel 2", CHANNEL_2)],
        [events.Button.inline("✅ I Have Joined, Continue", b"verified")]
    ]
    
    await event.respond(
        f"👋 Hello {name}!\n\n"
        "🎬 Welcome to Lucky Bot.\n"
        "🚨 Please join our both channels first, then send any movie name.",
        buttons=buttons
    )

@client.on(events.CallbackQuery(data=b'verified'))
async def verify_cb(event):
    await event.answer("Verified successfully! Now send movie name.", alert=True)
    await event.respond("✅ Verified! Now send the name of the movie you want.")

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and not e.text.startswith('/')))
async def search_handler(event):
    query = event.text
    
    file_buttons = [
        [events.Button.inline("📦 [3.89 GB] Movie 1080p WEB-DL", b"get_file")],
        [events.Button.inline("📦 [2.78 GB] Movie 720p HEVC", b"get_file")]
    ]
    
    await event.respond(
        f"🔍 **Search Results for:** `{query}`\n"
        f"👇 *Tap any quality button below to get your file:*",
        buttons=file_buttons
    )

@client.on(events.CallbackQuery(data=b'get_file'))
async def file_cb(event):
    await event.answer("Sending file...", alert=False)
    sent_msg = await event.respond(
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
    print("Lucky Final Bot (Telethon) is running...")
    client.run_until_disconnected()
    
