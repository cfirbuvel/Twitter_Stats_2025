from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler
from .handlers import auth, analysis, menu

AUTH, ANALYSIS = range(2)

def create_bot():
    application = ApplicationBuilder().token(settings.TG_BOT_TOKEN.get_secret_value()).build()

    # Add conversation handler with authentication
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", menu.main_menu)],
        states={
            AUTH: [auth.auth_handler],
            ANALYSIS: [analysis.analysis_handler]
        },
        fallbacks=[CommandHandler("cancel", menu.main_menu)]
    ))

    return application