import datetime

import pytz
from telegram.ext import ContextTypes
from telegram import Update

async def reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(job.chat_id, text="Hi Noa! This is your daily reminder to send me a photo or video! Love you <3")

async def set_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        set_time = [13,0]
        time_input = context.args[0]
        set_time = time_input.split(":")
        context.job_queue.run_daily(reminder, time=datetime.time(int(set_time[0]), int(set_time[1]), tzinfo=pytz.timezone('Asia/Jerusalem')), chat_id=update.effective_chat.id, data=f"{set_time[0]}:{set_time[1]}")
        message = f"Reminder set to {set_time[0]}:{set_time[1]} every day!"
        await context.bot.send_message(update.effective_chat.id, text=message)
    except:
        await context.bot.send_message(update.effective_chat.id, text="Error setting reminder. Please try again. Make sure to use the format HH:MM (24 hour clock)")

async def check_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.job_queue.jobs()) == 0:
        message = "You have no reminders set!"
    else:
        message = "You have reminders set for: \n"
        for job in context.job_queue.jobs():
            message += f"{job.data}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def cancel_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for job in context.job_queue.jobs():
        job.schedule_removal()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Reminders cancelled!")