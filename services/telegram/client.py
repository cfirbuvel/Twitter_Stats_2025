from telethon import TelegramClient, events
from redis.asyncio import Redis
from config.settings import settings


class TelegramBot:
    def __init__(self):
        self.client = TelegramClient(
            'bot_session',
            settings.TG_API_ID,
            settings.TG_API_HASH.get_secret_value()
        )
        self.redis = Redis.from_url(settings.REDIS_URL)

        self.client.add_event_handler(self.start_handler, events.NewMessage(pattern='/start'))
        self.client.add_event_handler(self.auth_handler, events.NewMessage(pattern='/auth'))
        self.client.add_event_handler(self.analyze_handler, events.NewMessage(pattern='/analyze'))

    async def start_handler(self, event):
        await event.reply("🚀 Welcome! Use /auth to authenticate")

    async def auth_handler(self, event):
        if ' ' in event.text:
            _, password = event.text.split(' ', 1)
            if password == settings.BOT_PASSWORD.get_secret_value():
                await self.redis.setex(f"auth:{event.sender_id}", 86400, "authenticated")
                await event.reply("✅ Authentication successful!")
                return
        await event.reply("🔑 Please use: /auth your_password")

    async def analyze_handler(self, event):
        if await self.redis.exists(f"auth:{event.sender_id}"):
            await event.reply("🔍 Starting analysis...")
        else:
            await event.reply("❌ Please authenticate first with /auth")

    async def start(self):
        await self.client.start(bot_token=settings.TG_BOT_TOKEN.get_secret_value())
        await self.client.run_until_disconnected()