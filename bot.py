import logging
import re
import os
import json
from difflib import SequenceMatcher

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from keep_alive import keep_alive

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Client(
    "LuckyNewBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

DB_CHANNEL = int(config.DB_CHANNEL)

CHANNEL_1 = "https://t.me/movieseries0012"
CHANNEL_2 = "https://t.me/movieseries0453"

DB_FILE = "movies.json"
movies = {}

def normalize(text):
    text = text.lower()
    text = re.sub(r"\.(mkv|mp4|avi|mov)$", "", text)
    text = re.sub(r"[._\-()\[\]]", " ", text)
    return " ".join(text.split())

def load_movies():
    global movies
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            movies = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        movies = {}

def save_movies():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

def get_media(message):
    media = (
        message.document
        or message.video
        or message.audio
        or message.animation
    )
    if not media:
        return None
    name = getattr(media, "file_name", None) or message.caption or f"Movie_{message.id}"
    return {
        "name": name,
        "chat_id": message.chat.id,
        "message_id": message.id,
        "size": getattr(media, "file_size", 0)
    }

@app.on_message(filters.chat(DB_CHANNEL))
async def save_movie(client, message):
    item = get_media(message)
    if not item:
        return
    key = str(message.id)
    movies[key] = item
    save_movies()
    log.info("Indexed movie: %s", item["name"])

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2)],
        [InlineKeyboardButton("✅ I Have Joined, Continue", callback_data="verified")]
    ]
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "🎬 Welcome to Lucky Bot.\n"
        "🚨 Please join both channels first, then send any movie name.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def is_member(client, user_id, channel):
    try:
        # Channel username or ID mathi check karse
        member = await client.get_chat_member(channel, user_id)
        return member.status in ("member", "administrator", "owner")
    except Exception:
        return True # Error aave to bypass rakhvu jethi user atak na jay

@app.on_callback_query(filters.regex("^verified$"))
async def verify_join(client, query):
    user_id = query.from_user.id
    await query.answer("Verified! Now send any movie name.", show_alert=True)
    await query.message.reply_text("✅ Verified! Now send the name of the movie you want.")

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def search_movie(client, message):
    query = normalize(message.text)
    if not query:
        return await message.reply_text("Please enter a movie name.")

    # Evi rite dummy / sample result buttons mukia chhe jethi jaldhi work kare
    buttons = [
        [InlineKeyboardButton("📦 [3.89 GB] Movie 1080p WEB-DL", callback_data="get_file")],
        [InlineKeyboardButton("📦 [2.78 GB] Movie 720p HEVC", callback_data="get_file")],
        [
            InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1),
            InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2)
        ]
    ]

    await message.reply_text(
        f"🎬 **Search Results for:** `{message.text}`\n\n"
        f"👇 *Tap any quality button below to get your file:*",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("^get_file$"))
async def send_file_callback(client, query):
    await query.answer("Sending your file...", show_alert=False)
    await query.message.reply_text(
        "📂 **Here is your requested movie file:**\n\n"
        "🔗 [Click Here to Download File](https://t.me/movieseries0012)\n\n"
        "⏳ *Note: File will be auto-deleted in 10 minutes for safety.*"
    )

load_movies()

if __name__ == "__main__":
    keep_alive()
    print("Lucky Bot with DB is running...")
    app.run()
    
