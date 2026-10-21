
import logging
import json
import os
import re
from difflib import SequenceMatcher

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import config
from keep_alive import keep_alive

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Client(
    "LuckyNewBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Your correct channel usernames
CHANNEL_1 = "@movieseries0453"
CHANNEL_2 = "@movie_series0012"

# Private movie database channel ID
DB_CHANNEL = int(config.DB_CHANNEL)

DB_FILE = "movies.json"
movies = {}


def normalize(text):
    text = (text or "").lower()
    text = re.sub(
        r"\.(mkv|mp4|avi|mov|webm)$",
        "",
        text
    )
    text = re.sub(r"[._\-()\[\]]", " ", text)
    return " ".join(text.split())


def load_movies():
    global movies

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            movies = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        movies = {}


def save_movies():
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(
            movies,
            file,
            ensure_ascii=False,
            indent=2
        )


def get_movie_file(message):
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
        "message_id": message.id
    }


async def is_member(client, user_id, channel):
    try:
        member = await client.get_chat_member(
            chat_id=channel,
            user_id=user_id
        )

        status = str(member.status).lower()

        return status in (
            "member",
            "administrator",
            "owner",
            "creator",
            "chatmemberstatus.member",
            "chatmemberstatus.administrator",
            "chatmemberstatus.owner",
            "chatmemberstatus.creator"
        )

    except Exception as error:
        logger.error(
            "Membership check failed for %s: %s",
            channel,
            error
        )
        return False


async def check_both_channels(client, user_id):
    first = await is_member(client, user_id, CHANNEL_1)
    second = await is_member(client, user_id, CHANNEL_2)

    return first and second


def join_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 Join Channel 1",
                url="https://t.me/movieseries0453"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Join Channel 2",
                url="https://t.me/movie_series0012"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ I Have Joined, Continue",
                callback_data="verified"
            )
        ]
    ])


@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_text(
        f"👋 Hello {message.from_user.first_name}!\n\n"
        "🎬 Welcome to Lucky Bot!\n\n"
        "🚨 Join both channels before searching for movies.",
        reply_markup=join_buttons()
    )


@app.on_callback_query(filters.regex("^verified$"))
async def verify_join(client, query):
    joined = await check_both_channels(
        client,
        query.from_user.id
    )

    if joined:
        await query.answer("Membership verified!")
        await query.message.reply_text(
            "✅ Verification successful!\n\n"
            "🎬 Now send me a movie name."
        )
    else:
        await query.answer(
            "Please join both channels first.",
            show_alert=True
        )


# Automatically index new media posted in the private database channel
@app.on_message(filters.chat(DB_CHANNEL))
async def index_new_movie(client, message):
    item = get_movie_file(message)

    if not item:
        return

    movies[str(message.id)] = item
    save_movies()

    logger.info("Indexed movie: %s", item["name"])


@app.on_message(
    filters.command("index") & filters.private
)
async def index_status(client, message):
    if message.from_user.id != int(config.OWNER_ID):
        return

    await message.reply_text(
        f"📚 Indexed movie files: {len(movies)}\n\n"
        "New media posted in the database channel "
        "will be indexed automatically."
    )


@app.on_message(
    filters.text
    & filters.private
    & ~filters.command(["start", "index"])
)
async def search_movie(client, message):
    user_id = message.from_user.id

    joined = await check_both_channels(client, user_id)

    if not joined:
        await message.reply_text(
            "🚨 Please join both channels first.",
            reply_markup=join_buttons()
        )
        return

    query = normalize(message.text)

    if not query:
        await message.reply_text("Please enter a movie name.")
        return

    results = []

    for key, item in movies.items():
        movie_name = normalize(item.get("name", ""))

        score = SequenceMatcher(
            None,
            query,
            movie_name
        ).ratio()

        if query in movie_name or score >= 0.55:
            results.append((score, key, item))

    results.sort(key=lambda result: result[0], reverse=True)
    results = results[:10]

    if not results:
        await message.reply_text(
            "❌ Movie not found in the indexed files.\n\n"
            "Try another spelling or check whether "
            "the file is saved in the private database channel."
        )
        return

    buttons = []

    for score, key, item in results:
        name = item["name"][:55]

        buttons.append([
            InlineKeyboardButton(
                f"🎬 {name}",
                callback_data=f"movie_{key}"
            )
        ])

    await message.reply_text(
        f"🔎 Search: {message.text}\n"
        f"📊 Results: {len(results)}\n\n"
        "👇 Select your movie:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(r"^movie_(\d+)$"))
async def send_movie(client, query):
    key = query.data.split("_", 1)[1]
    item = movies.get(key)

    if not item:
        await query.answer(
            "Movie record not found.",
            show_alert=True
        )
        return

    await query.answer("Sending movie...")

    try:
        await client.copy_message(
            chat_id=query.from_user.id,
            from_chat_id=int(item["chat_id"]),
            message_id=int(item["message_id"])
        )

    except Exception:
        logger.exception("Movie delivery failed")

        await query.message.reply_text(
            "❌ Could not send the movie.\n"
            "Please check the bot's private-channel access."
        )


load_movies()


if __name__ == "__main__":
    keep_alive()
    logger.info("Lucky Bot starting...")
    app.run()
