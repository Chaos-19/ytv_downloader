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
            "http_headers": {
              "Cookie": """# Netscape HTTP Cookie File
# http://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file!  Do not edit.

.youtube.com	TRUE	/	TRUE	1776323670	PREF	f6=40000000&tz=Africa.Addis_Ababa
.youtube.com	TRUE	/	TRUE	1760796504	__Secure-1PSIDTS	sidts-CjIBQlrA-JtW02JE3Taaj1vXxRohkKmZPn7enOccZJ6g5_2f1i-zZDyziVkA0-xBzrG7HBAA
.youtube.com	TRUE	/	TRUE	1760796504	__Secure-3PSIDTS	sidts-CjIBQlrA-JtW02JE3Taaj1vXxRohkKmZPn7enOccZJ6g5_2f1i-zZDyziVkA0-xBzrG7HBAA
.youtube.com	TRUE	/	FALSE	1776323665	HSID	Aki7yurhf9YrAmIgz
.youtube.com	TRUE	/	TRUE	1776323665	SSID	ACZOzEo2Busi4jVb9
.youtube.com	TRUE	/	FALSE	1776323665	APISID	tku2teAIKVn8lKrt/AX03tJBA68ExAnhns
.youtube.com	TRUE	/	TRUE	1776323665	SAPISID	qwAtVDoIKi17qSc7/AknLiEDUjwG1qnhiB
.youtube.com	TRUE	/	TRUE	1776323665	__Secure-1PAPISID	qwAtVDoIKi17qSc7/AknLiEDUjwG1qnhiB
.youtube.com	TRUE	/	TRUE	1776323665	__Secure-3PAPISID	qwAtVDoIKi17qSc7/AknLiEDUjwG1qnhiB
.youtube.com	TRUE	/	TRUE	1765114121	LOGIN_INFO	AFmmF2swRQIhAI7yRymmBvrYpGjS_woIbLoTN6WBQ61GFopvn0OapK9rAiAthvpMT0tRI0WF5EazahAnpr9XWFTnRR6T5KpV4hpPyg:QUQ3MjNmem5DVmNzV1lMaW5iVFNJd2c3YVFjbFhIYWRzVEttUjlZZjFvLWhzT3dGUWZSUUk4VWtEaUdpUzhUcndibEFNNlpZbjVyZm5NNktCOWd6UUFISzROdHRSNWI2azRtRUJTTUY4MWZDelFTT0VuR2lxRzk1M29pVVRXWkZaWmpIdnBhTXpRak12RDJkTndlZFhpa3RiUEo1YjlxRmZB
.youtube.com	TRUE	/	FALSE	1776323665	SID	g.a000ugjQARHL5P_ogxgpiRgTPzT8fMe7mL-0kKoAtd4T2lmsj_qlQy3WszDviedByxIEjwM7KgACgYKARYSAQ8SFQHGX2MiTbQ_2dipFP1mzt6AV5wscRoVAUF8yKqr-4-AMsPu9wp_K7ChFYpB0076
.youtube.com	TRUE	/	TRUE	1776323665	__Secure-1PSID	g.a000ugjQARHL5P_ogxgpiRgTPzT8fMe7mL-0kKoAtd4T2lmsj_ql4i7K6rz0zt1lD1-rbxHPbgACgYKAcsSAQ8SFQHGX2MiP1RgMBNQr8Cw_vVQELMEIxoVAUF8yKotUr1OFcVTZXNRiCbp5elA0076
.youtube.com	TRUE	/	TRUE	1776323665	__Secure-3PSID	g.a000ugjQARHL5P_ogxgpiRgTPzT8fMe7mL-0kKoAtd4T2lmsj_qlfWA98fr8Ht96-_TFNvBgUgACgYKAcASAQ8SFQHGX2MiXnkIBBE2878wfYY2dMYfNxoVAUF8yKr4xDk6RUnYdXMtyilIhvAQ0076
.youtube.com	TRUE	/	FALSE	1773299666	SIDCC	AKEyXzVWOXhLXtZta2ttOGL_dRJqFqP2u7wf29t9apns_Ev7602pqgCVQio_K9M4fKFObSO1
.youtube.com	TRUE	/	TRUE	1773299666	__Secure-1PSIDCC	AKEyXzXUHXvgywAPjENYMS4hS1GdWmdwV3R65ZSKgobVqHzfm5Pd7A26UeAcKP9gBUWtxIlH
.youtube.com	TRUE	/	TRUE	1773299666	__Secure-3PSIDCC	AKEyXzVOnBsNzT5M6grzjOSaP3lH4QgF4DVN7PqaqxHUWWf_Nf3aJLBOF3WChmYFEy2Vmajh
 """,
            },
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





