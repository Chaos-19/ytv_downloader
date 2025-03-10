from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """*Welcome to the YouTube Playlist Downloader Bot*

Send me a YouTube playlist link, and I'll fetch the videos for you\. You can choose to download them as audio or video\.

*How to use:*  
\- Send a *playlist URL* to start\.  
\- Choose your preferred format  \(audio/video\)\.  
\- Wait for your download link\!  

If you need help, type /help\. Happy downloading\!""",
        parse_mode="MarkdownV2",
    )