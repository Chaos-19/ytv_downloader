import logging
import os
import asyncio
from dotenv import load_dotenv

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
from asgiref.wsgi import WsgiToAsgi

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
flask_app = Flask(__name__)

# Telegram Application
application = Application.builder().token(TOKEN).updater(None).build()

# Handlers
application.add_handler(CommandHandler(["start", "help"], start))
application.add_handler(MessageHandler(filters.Regex(r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|playlist\?list=)|youtu\.be\/)[\w\-]+"), select_format))
application.add_handler(CallbackQueryHandler(download))

@flask_app.post(f"/{TOKEN}")  # Webhook endpoint for Telegram updates
async def telegram_webhook() -> Response:
    """Handle Telegram webhook updates."""
    update = Update.de_json(request.json, application.bot)
    await application.update_queue.put(update)
    return Response(status=HTTPStatus.OK)

@flask_app.get("/healthcheck")
async def healthcheck() -> Response:
    """Health check endpoint."""
    return Response("Bot is running fine!", status=HTTPStatus.OK)

async def main():
    """Start the bot and web server."""
    # Set webhook
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

    # Wrap Flask app to ASGI
    asgi_app = WsgiToAsgi(flask_app)

    # Start web server
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=asgi_app,  # Ensure you're passing the ASGI-wrapped Flask app
            port=PORT,
            host="0.0.0.0",
        )
    )

    # Run bot application and web server
    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()

if __name__ == "__main__":
    asyncio.run(main())