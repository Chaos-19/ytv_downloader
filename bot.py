import logging
import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request, Response
from telegram import Update, ForceReply
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # Default URL

# Flask App
web_app = Flask(__name__)

# Telegram Application
application = None

# Import handlers
from handlers.start import start
from handlers.help import help_command
from handlers.downloader import select_format, download

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Flask webhook route
@web_app.route('/telegram', methods=['POST'])
async def telegram_webhook():
    """Handles incoming webhook updates from Telegram."""
    global application
    if request.method == 'POST':
        logging.info("Received update: %s", request.json)
        await application.update_queue.put(Update.de_json(request.json, application.bot))
        return Response("ok", status=200)
    return "<h1>Welcome!</h1>"

@web_app.route('/')
def home():
    return "Hello, World!"

async def init_application():
    """Initialize Telegram bot application."""
    global application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(
        MessageHandler(
            filters.Regex(r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|playlist\?list=)|youtu\.be\/)[\w\-]+"),
            select_format
        )
    )
    application.add_handler(CallbackQueryHandler(download))

    # Set webhook
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/telegram")

    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()

async def main():
    """Main entry point for async execution."""
    await init_application()

if __name__ == "__main__":
    asyncio.run(main())