class MenuHandler:
    def __init__(self, redis):
        self.redis = redis

    async def show_main_menu(self, event, user_id):
        """Displays the main menu with live-updating user selections."""

        # Fetch user preferences from Redis
        username = await self.redis.get(f"username:{user_id}") or "Not Set"
        min_mentions = await self.redis.get(f"min_mentions:{user_id}") or "10"
        results_limit = await self.redis.get(f"results_limit:{user_id}") or "50"
        duration = await self.redis.get(f"duration:{user_id}") or "Last Week"
        keywords = await self.redis.get(f"keywords:{user_id}") or "None"
        hashtags = await self.redis.get(f"hashtags:{user_id}") or "None"

        # Ensure Redis values are properly decoded
        username = username.decode() if isinstance(username, bytes) else username
        min_mentions = min_mentions.decode() if isinstance(min_mentions, bytes) else min_mentions
        results_limit = results_limit.decode() if isinstance(results_limit, bytes) else results_limit
        duration = duration.decode() if isinstance(duration, bytes) else duration
        keywords = keywords.decode() if isinstance(keywords, bytes) else keywords
        hashtags = hashtags.decode() if isinstance(hashtags, bytes) else hashtags

        # Construct the menu message
        menu_text = (
            "✅ *Authentication successful!*\n\n"
            "📌 *Current Selections:*\n"
            f"🔍 *Username:* {username}\n"
            f"📣 *Min Mentions:* {min_mentions}\n"
            f"🔢 *Results Limit:* {results_limit}\n"
            f"⏳ *Duration:* {duration}\n"
            f"🏷️ *Keywords:* {keywords}\n"
            f"#️⃣ *Hashtags:* {hashtags}\n\n"
            "📌 *Please select an option:*"
        )

        # Define the inline keyboard layout
        buttons = [
            [Button.inline(f"🔍 Search Username: {username}", b"search_username")],
            [Button.inline(f"📢 Min Mentions: {min_mentions}", b"min_mentions"),
             Button.inline(f"🔢 Results Limit: {results_limit}", b"results_limit")],
            [Button.inline(f"⏳ Duration: {duration}", b"duration")],
            [Button.inline(f"🏷️ Keywords: {keywords}", b"keywords"),
             Button.inline(f"#️⃣ Hashtags: {hashtags}", b"hashtags")],
            [Button.inline("🚀 Start Scrape", b"start_scrape")],
            [Button.inline("⬅️ Back", b"back")]
        ]

        # Send the menu message with buttons
        await event.respond(menu_text, buttons=buttons, parse_mode="Markdown")
