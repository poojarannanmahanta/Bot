import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import random

TOKEN = os.getenv("BOT_TOKEN")

web = Flask(__name__)
@web.route('/')
def home(): return "Randee is ACTIVE!"
def run_web():
    web.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("🎲 Random", callback_data='random'), InlineKeyboardButton("😂 Joke", callback_data='joke')]]
    await update.message.reply_text(f"Randee is ACTIVE ✅ Hi {update.effective_user.first_name}!", reply_markup=InlineKeyboardMarkup(kb))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Randee heard: {update.message.text}")

async def btns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(f"Random: {random.randint(1,100)}" if q.data=='random' else "Why don't coders like nature? Too many bugs! 😂")

def main():
    threading.Thread(target=run_web, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(btns))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
