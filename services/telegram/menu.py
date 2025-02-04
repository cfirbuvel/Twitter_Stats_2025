from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔐 Authenticate", callback_data="auth")],
        [InlineKeyboardButton("📊 Analyze Mentions", callback_data="analyze")]
    ]
    await update.message.reply_text(
        "Main Menu:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

menu_handler = CommandHandler("menu", main_menu)