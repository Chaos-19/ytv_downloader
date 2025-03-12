from telegram import  Update
from telegram.ext import ContextTypes

import yt_dlp
import os
from .utils import zip_folder


async def fetch_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch YouTube metadata asynchronously."""
    ytv_url = "https://youtube.com/watch?v=-qjE8JkIVoQ&si=QeI-Vt4JGxV6Sr9Y"
    with yt_dlp.YoutubeDL({}) as ydl:
        result = ydl.extract_info(ytv_url, download=False)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=result.get("title", "Unknown Playlist"))
        
        
async def download_ytv_and_zip(ytv_url,format_choice):
    """Download and ZIP videos asynchronously."""
    #ydl_opts = {"outtmpl": "download/%(title)s.%(ext)s"}
    ydl_opts = {
            "cookiefile": "./cookies.txt",
            "outtmpl": "download/%(title)s.%(ext)s",
        }
        
    if format_choice == "mp3":
        ydl_opts = {
           **ydl_opts,
           'extract_audio': True,
           'format': 'bestaudio/best',
        }
    
    download_title = ""
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(ytv_url, download=False)
        download_title = info.get("title", "Unknown Playlist")
    
        ydl.download([ytv_url])
    
    zip_path = os.path.join(f"{download_title}.zip")
    #zip_folder.apply_async(args=["download", zip_path])
    await zip_folder("download", zip_path)
    
    return zip_path





