# 📥 YouTube Playlist Downloader Bot

A Telegram bot that helps you easily download entire YouTube playlists in audio (MP3) or video (MP4) format, bundled neatly into a ZIP file.  
Built using **Python**, **python-telegram-bot**, and **yt-dlp**.

---

## ✨ Features

- Download entire YouTube playlists or single videos.
- Choose between audio (MP3) and video (MP4).
- Files are zipped and sent directly in chat.
- Lightweight and easy to deploy.
- Uses in-memory temporary data (no external database required).

---

## 📦 Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/chaos-19-ytv_downloader.git
   cd chaos-19-ytv_downloader

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create and configure `.env`:**

   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

4. **Run the bot:**

   ```bash
   python bot.py
   ```

---

## 🚀 Usage

1. Start the bot on Telegram: `/start`
2. Send a **YouTube playlist URL** or a video URL.
3. Choose your preferred format:

   * 🎵 Audio (MP3)
   * 📹 Video (MP4)
4. Receive a ZIP file containing the downloaded media.

---

## 🗂 Project Structure

```text
chaos-19-ytv_downloader/
├── bot.py                   # Main bot runner and handler setup
├── config.py                # Reserved for future configuration
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── database/
│   └── db.py                # In-memory temporary data storage
├── handlers/                # Telegram command & callback handlers
│   ├── downloader.py
│   ├── start.py
│   ├── help.py
│   ├── fetch_metadata.py
│   ├── echo.py
│   └── error.py
└── services/                # Downloading, zipping, and utility services
    ├── youtube.py
    ├── utils.py
    └── __init__.py
```

---

## ⚙️ Technologies Used

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Contributing

Pull requests, suggestions, and issues are welcome!
Feel free to open an issue or submit a PR.

---

## 📫 Contact

If you'd like to reach out:
**Chaos** – [Hirekalkidangetachew@outlook.com](mailto:your.email@example.com)

---

**Happy downloading! 🎉**
