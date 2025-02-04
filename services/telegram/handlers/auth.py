from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from config.settings import Settings

settings = Settings()


async def authenticate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if user_input == settings.BOT_PASSWORD.get_secret_value():
        await update.message.reply_text("✅ Authentication successful!")
        return "AUTHENTICATED"
    else:
        await update.message.reply_text("❌ Incorrect password. Try again or /cancel")
        return "AWAITING_PASSWORD"


auth_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, authenticate)