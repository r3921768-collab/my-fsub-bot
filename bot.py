import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# --- Dummy HTTP Server for Render Port Binding ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Lucky Bot is active and running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Start dummy server in a background thread so Render detects an open port
threading.Thread(target=run_server, daemon=True).start()
# ------------------------------------------------

BOT_TOKEN = "8574146217:AAHKhJS_LoeXKOVQ4mNwPruS_UGHRFywNs8"
CHANNEL_1 = "https://t.me/movieseries0453"
CHANNEL_2 = "https://t.me/movie_series0012"
DATABASE_CHANNEL_ID = -1003867813389  # Tamari movie database channel ni ID ahiya nakho (e.g., -1001234567890)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2)],
        [InlineKeyboardButton("✅ I Have Joined, Continue", callback_data="verified")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        "🎬 Welcome to Lucky Bot.\n"
        "🚨 Please join our both channels first, then send any movie name.",
        reply_markup=reply_markup
    )

async def verify_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✅ Verified! Now send the name of the movie you want.")

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    keyboard = [
        [InlineKeyboardButton("📦 [3.89 GB] Movie 1080p WEB-DL", callback_data="get_file")],
        [InlineKeyboardButton("📦 [2.78 GB] Movie 720p HEVC", callback_data="get_file")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"🔍 **Search Results for:** `{query}`\n"
        f"👇 *Tap any quality button below to get your file:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def file_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Sending file...")
    sent_msg = await query.message.reply_text(
        "📁 **Here is your requested movie file:**\n\n"
        "🔗 [Click Here to Download File](https://t.me/movieseries0012)\n"
        "⏳ *Note: This file will auto-delete in 5 minutes for safety.*",
        parse_mode="Markdown"
    )
    await asyncio.sleep(300)
    try:
        await sent_msg.delete()
    except:
        pass

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(verify_cb, pattern='^verified$'))
    application.add_handler(CallbackQueryHandler(file_cb, pattern='^get_file$'))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_handler))
    print("Python-Telegram-Bot is running successfully with HTTP server...")
    application.run_polling()
    
