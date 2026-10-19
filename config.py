import os

# Telegram API credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Database connection URL (MongoDB)
DATABASE_URI = os.environ.get("DATABASE_URI", "")

# Main Movie Database Channel ID
DB_CHANNEL = int(os.environ.get("DB_CHANNEL", 0))

# Two Force-Subscribe Channels (Banne channel IDs)
FSUB_CHANNEL_1 = int(os.environ.get("FSUB_CHANNEL_1", 0))
FSUB_CHANNEL_2 = int(os.environ.get("FSUB_CHANNEL_2", 0))

