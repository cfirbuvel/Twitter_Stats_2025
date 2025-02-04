from telethon import TelegramClient, events, Button
from redis.asyncio import Redis, RedisError
from config.settings import settings
from services.telegram.menu import MenuHandler
from services.twitter.twitter_scraper import TwitterScraper
import logging

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.client = TelegramClient(
            'bot_session',
            settings.TG_API_ID,
            settings.TG_API_HASH.get_secret_value()
        )
        try:
            self.redis = Redis.from_url(settings.REDIS_URL)
        except RedisError as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.redis = None  # Allow bot to run without Redis

        self.menu_handler = MenuHandler(self.redis) if self.redis else None
        self.twitter_scraper = TwitterScraper()

        self.client.add_event_handler(self.start_handler, events.NewMessage(pattern='/start'))
        self.client.add_event_handler(self.analyze_handler, events.NewMessage(pattern='/analyze'))
        self.client.add_event_handler(self.button_handler, events.CallbackQuery())

    async def start(self):
        """Start the bot by connecting and running it."""
        try:
            await self.client.start(bot_token=settings.TG_BOT_TOKEN.get_secret_value())
            logger.info("✅ Telegram bot started successfully!")
            await self.client.run_until_disconnected()
        except Exception as e:
            logger.error(f"❌ Error starting the bot: {str(e)}")

    async def auth_handler(self, event):
        try:
            user_id = event.sender_id
            user_input = event.text.strip()
        except Exception as e:
            logger.error(f"❌ Error in auth_handler: {str(e)}")
            await event.reply("❌ An error occurred. Please try again later.")

    async def analyze_handler(self, event):
        try:
            username = event.text.split("/analyze ", 1)[-1].strip()
            response = self.twitter_scraper.scrape_mentions(username)
            await event.reply(response)
        except Exception as e:
            logger.error(f"❌ Error in analyze_handler: {str(e)}")
            await event.reply("❌ An error occurred. Please try again later.")

    async def start_handler(self, event):
        """Handles the /start command and sends an inline button menu."""
        try:
            buttons = [
                [Button.inline("🔍 Search Username", b"search_username")],
                [Button.inline("📢 Min Mentions", b"min_mentions"), Button.inline("🔢 Results Limit", b"results_limit")],
                [Button.inline("⏳ Duration", b"duration")],
                [Button.inline("🏷️ Keywords", b"keywords"), Button.inline("#️⃣ Hashtags", b"hashtags")],
                [Button.inline("🚀 Start Scrape", b"start_scrape")],
                [Button.inline("⬅️ Back", b"back")]
            ]
            await event.respond(
                 "✅ **Authentication successful!**\n\n"
            "📌 **Current Selections:**\n"
            f"🔍 **Username:** None\n"
            f"📣 **Min Mentions:**\n"
            f"🔢 **Results Limit:**\n"
            f"⏳ **Duration:**\n"
            f"🏷️ **Keywords:**\n"
            f"#️⃣ **Hashtags:**\n\n"
            "📌 **Please select an option:**",
                buttons=buttons,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"❌ Error in start_handler: {str(e)}")

    async def button_handler(self, event):
        """Handles button clicks."""
        try:
            data = event.data.decode("utf-8")
            if data == "search_username":
                await event.respond("🔍 Please enter the Twitter username you want to analyze.")
            elif data == "min_mentions":
                await event.respond("📢 Set the minimum number of mentions.")
            elif data == "results_limit":
                await event.respond("🔢 Set the results limit.")
            elif data == "duration":
                await event.respond("⏳ Select the time duration for analysis.")
            elif data == "keywords":
                await event.respond("🏷️ Enter keywords to filter results.")
            elif data == "hashtags":
                await event.respond("#️⃣ Enter hashtags to filter results.")
            elif data == "start_scrape":
                await event.respond("🚀 Starting analysis...")
            elif data == "back":
                await event.respond("⬅️ Going back.")
        except Exception as e:
            logger.error(f"❌ Error in button_handler: {str(e)}")
