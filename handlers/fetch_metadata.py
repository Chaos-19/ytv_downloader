from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import yt_dlp

async def fetch_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch YouTube metadata asynchronously."""
    ytv_url = "https://youtube.com/watch?v=-qjE8JkIVoQ&si=QeI-Vt4JGxV6Sr9Y"
    with yt_dlp.YoutubeDL({}) as ydl:
        result = ydl.extract_info(ytv_url, download=False)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result.get("title", "Unknown Playlist"))