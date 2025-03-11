import logging
from telegram import Update
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,CallbackQueryHandler,ConversationHandler,MessageHandler,filters,CallbackQueryHandler)


from dotenv import load_dotenv # type: ignore
import os
import yt_dlp

import zipfile
import os
import json
import asyncio


from handlers.start import start
from handlers.help import help_command
from handlers.downloader import select_format,download

load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



async def fetch_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch YouTube metadata asynchronously."""
    ytv_url = "https://youtube.com/watch?v=-qjE8JkIVoQ&si=QeI-Vt4JGxV6Sr9Y"
    with yt_dlp.YoutubeDL({}) as ydl:
        result = ydl.extract_info(ytv_url, download=False)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result.get("title", "Unknown Playlist"))
        
        
async def download_ytv_and_zip(ytv_url):
    """Download and ZIP videos asynchronously."""
    ydl_opts = {"outtmpl": "download/%(title)s.%(ext)s"}
    
    download_title = ""
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(ytv_url, download=False)
        download_title = info.get("title", "Unknown Playlist")
        
        ydl.download([ytv_url])
    
    zip_path = os.path.join(f"{download_title}.zip")
    #zip_folder.apply_async(args=["download", zip_path])
    
    return f"Downloading {download_title} and zipping..."




if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).read_timeout(30).write_timeout(30).build()
    
    start_handler = CommandHandler('start', start)
    #ytv_metadata_handler = CommandHandler('info', fetch_metadata)
    
    application.add_handler(CommandHandler(['start','help'], start))
    #application.add_handler(CommandHandler('download', select_format))
    application.add_handler(MessageHandler(filters.Regex(r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|playlist\?list=)|youtu\.be\/)[\w\-]+"),select_format))
    
    application.add_handler(CallbackQueryHandler(download))
    #application.add_handler(CommandHandler('help', help_command))
    
    application.run_polling()