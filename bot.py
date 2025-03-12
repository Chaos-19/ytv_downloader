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

from keep_alive import keep_alive

keep_alive()

load_dotenv()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).read_timeout(30).write_timeout(30).build()
    
    start_handler = CommandHandler('start', start)
    
    application.add_handler(CommandHandler(['start','help'], start))
    application.add_handler(MessageHandler(filters.Regex(r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|playlist\?list=)|youtu\.be\/)[\w\-]+"),select_format))
    application.add_handler(CallbackQueryHandler(download))
    
    application.run_polling()