from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.youtube import download_ytv_and_zip
from database.db import set_data,get_data

import os
from services.utils import delete_playlist_data


async def select_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a format selection menu."""
    # Get the URL sent by the user
    url = update.message.text
    
    set_data(update.effective_chat.id, {
        "url":url,
        "status": "started"  # Custom status
    })
    
    keyboard = [
        [
            InlineKeyboardButton("Audio", callback_data="mp3"),
            InlineKeyboardButton("Video", callback_data="mp4"),
        ],
        [InlineKeyboardButton("Cancel", callback_data="cancel")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Great\! How would you like to download your video?\n\n"
        "🎵 *Audio \(MP3\)* – Best for music and podcasts\.\n"
        "📹 *Video \(MP4\)* – Watch in full quality\.\n\n"
        "Tap a button below to choose:",
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles user selection for audio/video format."""
    query = update.callback_query
    selected_format = query.data  # Get the selected format (mp3 or mp4)

    await query.answer()  # Acknowledge the button press
    chat_id = update.effective_chat.id
    
    user_data = get_data(chat_id)

    if selected_format == "mp3":
        await update.callback_query.edit_message_text(
            "🎶 *You chose Audio \(MP3\)\!* Preparing your download\.\.\.",
            parse_mode="MarkdownV2",
        )
    elif selected_format == "mp4":
        await update.callback_query.edit_message_text(
            "📺 *You chose Video \(MP4\)\!* Fetching your file\.\.\.",
            parse_mode="MarkdownV2",
        )
    else:
        await update.callback_query.edit_message_text(
            "❌ *Download canceled\.* Let me know if you need anything else\!"
             ,parse_mode="MarkdownV2"
             )
    if selected_format in ["mp4","mp3"]:
        # Specify the path to your zip file
        zip_file_path = await download_ytv_and_zip(user_data.get("url"),selected_format)
        
        # Send the zip file to the user
        await context.bot.send_document(
            chat_id=chat_id,
            document=open(zip_file_path, 'rb'),
            filename=os.path.basename(zip_file_path),
            caption="Here is your zip file!",
            read_timeout=60,  # Increase timeout
            write_timeout=60,  # Increase timeout
        )
        try:
          os.remove(zip_file_path)
          delete_playlist_data("download")
        except Exception as e:
          print("Error happened " + e.__str__())