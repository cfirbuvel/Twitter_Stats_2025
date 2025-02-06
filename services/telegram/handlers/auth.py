from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from models.redis_client import RedisManager
import hashlib


def rate_limit(key: str, limit: int = 5):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            redis = await RedisManager.get_client()
            user_id = update.effective_user.id
            count = await redis.incr(f"rate_limit:{key}:{user_id}")

            if count > limit:
                await update.message.reply_text("⚠️ Too many requests. Please try again later.")
                return

            return await func(update, context)

        return wrapper

    return decorator


@rate_limit("auth")
async def auth_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    stored_hash = hashlib.sha256(settings.BOT_PASSWORD.get_secret_value().encode()).hexdigest()
    user_hash = hashlib.sha256(user_input.encode()).hexdigest()

    if user_hash == stored_hash:
        await update.message.reply_text("✅ Authentication successful!")
        return "AUTHENTICATED"

    await update.message.reply_text("❌ Invalid credentials. Try again.")
    return "AUTH_FAILED"