import logging
import asyncio
from config.settings import settings
from services.telegram.client import TelegramBot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    bot = TelegramBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())