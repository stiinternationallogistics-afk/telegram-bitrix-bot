import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request

TOKEN = os.getenv("TG_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")

app = Flask(__name__)
telegram_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот запущен и работает")

telegram_app.add_handler(CommandHandler("start", start))

@app.route("/", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

@app.route("/", methods=["GET"])
def health():
    return "Bot is running"

if __name__ == "__main__":
    telegram_app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path="",
        webhook_url=WEBHOOK_URL
    )
