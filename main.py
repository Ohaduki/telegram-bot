import logging
import time
from datetime import datetime
import os

from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from config import TELEGRAM_TOKEN
from upload import upload
from db import add_file

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Gargir Photo Bot!")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.photo[-1].file_id
    new_file = await context.bot.get_file(file_id)
    extension = new_file.file_path.split(".")[-1]
    ts = time.time()
    await new_file.download_to_drive(f"files//{ts}.{extension}")
    caption = update.message.caption
    url = upload(path=f"files//{ts}.{extension}", id=f"{ts}")
    photo = {
        "file_id": ts,
        "extension": extension,
        "caption": caption,
        "type": "photo",
        "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "url": url
    }
    add_file(photo)
    os.remove(f"files//{ts}.{extension}")

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.video.file_id
    new_file = await context.bot.get_file(file_id)
    extension = new_file.file_path.split(".")[-1]
    ts = time.time()
    await new_file.download_to_drive(f"files//{ts}.{extension}")
    caption = update.message.caption
    url = upload(f"files//{ts}.{extension}", ts)
    video = {
        "file_id": ts,
        "extension": extension,
        "caption": caption,
        "type": "photo",
        "timestamp": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        "url": url
    }
    add_file(video)
    os.remove(f"files//{ts}.{extension}")


start_handler = CommandHandler('start', start)
photo_handler = MessageHandler(filters=filters.PHOTO, callback=photo)
video_handler = MessageHandler(filters=filters.VIDEO, callback=video)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(start_handler)
    application.add_handler(photo_handler)
    application.add_handler(video_handler)
    
    application.run_polling()