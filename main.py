import logging
import time

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from config import TELEGRAM_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Gargir Photo Bot!")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.photo[-1].file_id
    new_file = await context.bot.get_file(file_id)
    ts = time.time()
    await new_file.download_to_drive(f"files//{ts}.jpg")

start_handler = CommandHandler('start', start)
photo_handler = MessageHandler(filters=filters.PHOTO, callback=photo)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(start_handler)
    application.add_handler(photo_handler)
    
    application.run_polling()