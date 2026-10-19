import os

# Telegram API credentials
API_ID = int(os.environ.get("37601205", 0))
API_HASH = os.environ.get("6d73743bfe27-47bf3c06ed90be7d8b34", "")
BOT_TOKEN = os.environ.get("8574146217:AAHipNSOwLm9hwIMeLKl6qVLLJ2N-c9FIBQ", "")

# Database connection URL (MongoDB)
DATABASE_URI = os.environ.get("mongodb+srv://r3921768_db_user:<db_password>@rajveer.ttckgz3.mongodb.net/", "")

# Main Movie Database Channel ID
DB_CHANNEL = int(os.environ.get("-1003867813389", 0))

# Two Force-Subscribe Channels (Banne channel IDs)
FSUB_CHANNEL_1 = int(os.environ.get("-1003932990702", 0))
FSUB_CHANNEL_2 = int(os.environ.get("-1003395311841", 0))

