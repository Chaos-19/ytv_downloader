import logging
import os
import asyncio
import threading
from dotenv import load_dotenv

from flask import Flask, request, Response
from http import HTTPStatus

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from handlers.start import start
from handlers.downloader import select_format, download

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your bot's public URL (e.g. https://yourdomain.com)
PORT = int(os.getenv("PORT", 8000))       # Port number (should match your Render or deployment config)
TOKEN = os.getenv("BOT_TOKEN")            # Telegram Bot Token

# Initialize Flask app (this variable is required by Gunicorn)
app = Flask(__name__)

# Create Telegram application (async)
application = Application.builder().token(TOKEN).updater(None).build()

# Add Telegram handlers
application.add_handler(CommandHandler(["start", "help"], start))
application.add_handler(
    MessageHandler(
        filters.Regex(
            r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|playlist\?list=)|youtu\.be\/)[\w\-]+"
        ),
        select_format,
    )
)
application.add_handler(CallbackQueryHandler(download))

@app.post(f"/{TOKEN}")  # Webhook endpoint for Telegram updates
async def telegram_webhook() -> Response:
    """Handle Telegram webhook updates."""
    update = Update.de_json(request.json, application.bot)
    await application.update_queue.put(update)
    return Response(status=HTTPStatus.OK)

@app.get("/healthcheck")
async def healthcheck() -> Response:
    """Health check endpoint."""
    return Response("Bot is running fine!", status=HTTPStatus.OK)

def start_telegram_bot():
    """Run the Telegram bot asynchronously in a background thread."""
    async def run_bot():
        # Set the webhook (Telegram will call your /{TOKEN} endpoint)
        await application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
        # Start the bot's application (this will run indefinitely)
        async with application:
            await application.start()
            # Wait forever; you can use an asyncio.Event if needed
            await asyncio.Event().wait()
            await application.stop()
    asyncio.run(run_bot())

# Ensure the Telegram bot starts only once.
telegram_bot_started = False

@app.before_first_request
def init_telegram_bot():
    """Start the Telegram bot in a background thread once before the first request."""
    global telegram_bot_started
    if not telegram_bot_started:
        telegram_bot_started = True
        thread = threading.Thread(target=start_telegram_bot, daemon=True)
        thread.start()

# When running locally (e.g. via "python bot.py") start both Flask and the Telegram bot.
if __name__ == "__main__":
    # Start the Telegram bot in a background thread
    thread = threading.Thread(target=start_telegram_bot, daemon=True)
    thread.start()
    # Run the Flask development server
    app.run(host="0.0.0.0", port=PORT)