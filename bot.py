import logging
import os
import asyncio
from dotenv import load_dotenv
from threading import Thread

from flask import Flask, request, Response, abort
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

import uvicorn

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your bot's public URL
PORT = int(os.getenv("PORT", 8000))  # Port number
TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token

# Initialize Flask app
app = Flask(__name__)

# Telegram Application
application = Application.builder().token(TOKEN).updater(None).build()

# Handlers
application.add_handler(CommandHandler(["start", "help"], start))
application.add_handler(MessageHandler(filters.Regex(r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|playlist\?list=)|youtu\.be\/)[\w\-]+"), select_format))
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

def run_flask():
    """Run the Flask app."""
    app.run(host="0.0.0.0", port=PORT)

async def main():
    """Start the bot and web server."""
    # Set webhook
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run bot application
    async with application:
        await application.start()
        await asyncio.Event().wait() #keep the async loop running.
        await application.stop()

if __name__ == "__main__":
    asyncio.run(main())