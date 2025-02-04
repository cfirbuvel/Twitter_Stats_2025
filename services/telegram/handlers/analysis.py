from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler

async def set_min_mentions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter minimum number of mentions (default: 1):")
    return "SETTING_MIN_MENTIONS"

async def set_result_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter number of results to show (default: 50):")
    return "SETTING_RESULT_LIMIT"

async def start_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
        [InlineKeyboardButton("🚀 Start Analysis", callback_data="start")]
    ]
    await update.message.reply_text(
        "Choose an action:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

analysis_handler = CallbackQueryHandler(start_analysis, pattern="^analysis_")