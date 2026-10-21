
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

# Private movie channel ID config.py માં ઉમેરો
DB_CHANNEL = int(config.DB_CHANNEL)

CHANNEL_1 = "https://t.me/movieseries0012"
CHANNEL_2 = "https://t.me/movieseries0453"

DB_FILE = "movies.json"
movies = {}
pending = {}


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

    name = getattr(media, "file_name", None)
    if not name:
        name = message.caption or f"Movie_{message.id}"

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
        [InlineKeyboardButton("✅ Continue", callback_data="verified")]
    ]

    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "🎬 Welcome to Lucky Bot.\n"
        "Join both channels, then send a movie name.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def is_member(client, user_id, channel):
    try:
        member = await client.get_chat_member(channel, user_id)
        return member.status in ("member", "administrator", "owner")
    except Exception:
        return False


@app.on_callback_query(filters.regex("^verified$"))
async def verify_join(client, query):
    user_id = query.from_user.id

    # Membership verify કરવા માટે public usernames અથવા
    # numeric channel IDs config.py માં યોગ્ય હોવા જોઈએ.
    joined1 = await is_member(client, user_id, CHANNEL_1)
    joined2 = await is_member(client, user_id, CHANNEL_2)

    if joined1 and joined2:
        await query.answer("Verified! Send a movie name.")
        await query.message.reply_text("✅ Verified! Now send a movie name.")
    else:
        await query.answer(
            "Please join both channels first.",
            show_alert=True
        )


@app.on_message(filters.command("index") & filters.private)
async def index_status(client, message):
    if message.from_user.id != int(config.OWNER_ID):
        return await message.reply_text("Not allowed.")

    await message.reply_text(
        f"📚 Indexed movie records: {len(movies)}\n"
        "New files in the database channel are indexed automatically."
    )


@app.on_message(
    filters.text & filters.private & ~filters.command(["start", "index"])
)
async def search_movie(client, message):
    user_id = message.from_user.id

    joined1 = await is_member(client, user_id, CHANNEL_1)
    joined2 = await is_member(client, user_id, CHANNEL_2)

    if not (joined1 and joined2):
        return await message.reply_text(
            "🚨 Please join both channels first.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1)],
                [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2)]
            ])
        )

    query = normalize(message.text)

    if not query:
        return await message.reply_text("Please enter a movie name.")

    results = []
    for key, item in movies.items():
        name = normalize(item["name"])
        score = SequenceMatcher(None, query, name).ratio()

        if query in name or score >= 0.55:
            results.append((score, key, item))

    results.sort(key=lambda x: x[0], reverse=True)
    results = results[:10]

    if not results:
        return await message.reply_text(
            "❌ Movie not found in the indexed files.\n"
            "Check the spelling or try another name."
        )

    buttons = []
    for score, key, item in results:
        label = item["name"][:60]
        buttons.append([
            InlineKeyboardButton(
                f"🎬 {label}",
                callback_data=f"movie_{key}"
            )
        ])

    await message.reply_text(
        f"🔎 Results for: {message.text}\n"
        f"📊 Matches found: {len(results)}\n\n"
        "👇 Select your movie:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(r"^movie_(\d+)$"))
async def send_movie(client, query):
    key = query.data.split("_", 1)[1]
    item = movies.get(key)

    if not item:
        return await query.answer(
            "Movie record not found.",
            show_alert=True
        )

    await query.answer("Sending your movie...")
    try:
        await client.copy_message(
            chat_id=query.from_user.id,
            from_chat_id=int(item["chat_id"]),
            message_id=int(item["message_id"])
        )
    except Exception as exc:
        log.exception("Could not copy movie: %s", exc)
        await query.message.reply_text(
            "❌ Could not send this file. "
            "Check bot permissions in the private channel."
        )


load_movies()


if __name__ == "__main__":
    keep_alive()
    print("Lucky Bot is starting...")
    app.run()
