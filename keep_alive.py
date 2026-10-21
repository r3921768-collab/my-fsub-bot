import os
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is Active!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    import threading
    t = threading.Thread(target=run)
    t.start()
