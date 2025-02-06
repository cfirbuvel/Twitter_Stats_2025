from telegram.ext import Application, CommandHandler, MessageHandler, filters
from services.telegram.handlers import (
    start_handler,
    analyze_handler,
    auth_handler
)

class TelegramBot:
    def __init__(self):
        self.app = Application.builder().token(settings.TG_BOT_TOKEN.get_secret_value()).build()
        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", start_handler))
        self.app.add_handler(CommandHandler("analyze", analyze_handler))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auth_handler))

    async def start(self):
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def stop(self):
        await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()