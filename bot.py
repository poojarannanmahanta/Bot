import os, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set!")

app = Flask(__name__)

@app.route('/')
def home():
    return "Randee is ACTIVE ✅"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Randee is ACTIVE ✅\nBot is Live on Render!")

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Bot polling started...")
    application.run_polling()

if __name__ == "__main__":
    # Start telegram bot in background thread
    threading.Thread(target=run_bot, daemon=True).start()
    # Start Flask web server on Render's PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
