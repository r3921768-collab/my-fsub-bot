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

threading.Thread(target=run_server, daemon=True).start()
# ------------------------------------------------

BOT_TOKEN = "8574146217:AAHKhJS_LoeXKOVQ4mNwPruS_UGHRFywNs8"
CHANNEL_1_URL = "https://t.me/movieseries0453"
CHANNEL_2_URL = "https://t.me/movie_series0012"
DATABASE_CHANNEL_ID = -1003867813389# Tamari database channel ni ID ahiya nakho

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_1_URL)],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_2_URL)],
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
    await query.message.reply_text("✅ Verified! Now send the name of the movie you want to search.")

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    query = update.message.text
    
    file_keyboard = [
        [InlineKeyboardButton("📦 [1080p] Movie File", callback_data="get_file_1080")],
        [InlineKeyboardButton("📦 [720p] Movie File", callback_data="get_file_720")]
    ]
    reply_markup = InlineKeyboardMarkup(file_keyboard)
    
    await update.message.reply_text(
        f"🔍 **Search Results for:** `{query}`\n"
        f"👇 *Tap any quality button below to get your file:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def file_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Fetching movie file from database...")
    
    chat_id = query.message.chat_id
    
    try:
        # Ahiya database channel mathi file direct user na chat ma copy thase
        # (Note: DATABASE_CHANNEL_ID ma tamari channel ni ID ane message_id ma movie message no ID aavse)
        sent_msg = await context.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=DATABASE_CHANNEL_ID,
            message_id=2  # Tamari database channel na message no ID (Test mate 2 lakhelu chhe)
        )
        
        # 5 minute pachi auto-delete note sathe
        await asyncio.sleep(300)
        try:
            await sent_msg.delete()
        except:
            pass
    except Exception as e:
        await query.message.reply_text(f"⚠️ Error fetching file: {e}\n\nPlease make sure bot is admin in the database channel!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(verify_cb, pattern='^verified$'))
    application.add_handler(CallbackQueryHandler(file_cb, pattern='^get_file_'))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_handler))
    print("Lucky Movie Filter Bot is running with database file fetch...")
    application.run_polling()
    
