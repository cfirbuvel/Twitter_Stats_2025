from services.twitter.client import TwitterClient
from services.twitter.analyzer import MentionAnalyzer
from config.settings import settings

class TwitterScraper:
    def __init__(self):
        self.client = TwitterClient(settings.TWITTER_BEARER_TOKEN.get_secret_value())

    def scrape_mentions(self, username, min_mentions=10, results_limit=50, duration="Last Week", keywords=None,
                        hashtags=None):
        if not username:
            return "⚠️ Please provide a valid username."
        try:
            twitter_user_id = self.client.get_user_id(username)
            if not twitter_user_id:
                return "❌ Error: Unable to retrieve user ID. Please check the username."

            tweets = self.client.get_tweets(twitter_user_id)
            if not tweets or "data" not in tweets:
                return "📭 No tweets found for the given duration."
            if "errors" in tweets:
                return f"❌ Twitter API Error: {tweets['errors']}"
        except Exception as e:
            return f"❌ Unexpected error occurred: {str(e)}"