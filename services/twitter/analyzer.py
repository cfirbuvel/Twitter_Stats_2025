from datetime import datetime
from typing import Dict, List
from collections import defaultdict
from models.redis_client import RedisManager


class MentionAnalyzer:
    def __init__(self, raw_data: dict):
        self.raw_data = raw_data
        self.mentions = defaultdict(self._new_mention_entry)

    async def analyze(self, min_mentions: int = 1, max_results: int = 50) -> List[Dict]:
        await self._process_data()
        filtered = self._filter(min_mentions)
        return self._sort_and_limit(filtered, max_results)

    def _new_mention_entry(self) -> dict:
        return {
            "count": 0,
            "first_seen": None,
            "last_seen": None,
            "example_tweet": None
        }

    async def _process_data(self):
        for tweet in self.raw_data.get("data", []):
            created_at = datetime.fromisoformat(tweet["created_at"].rstrip("Z"))
            for mention in tweet.get("entities", {}).get("mentions", []):
                await self._update_mention(mention["username"], created_at, tweet["id"])

    async def _update_mention(self, username: str, timestamp: datetime, tweet_id: str):
        entry = self.mentions[username]
        entry["count"] += 1

        if not entry["first_seen"] or timestamp < entry["first_seen"]:
            entry["first_seen"] = timestamp

        if not entry["last_seen"] or timestamp > entry["last_seen"]:
            entry["last_seen"] = timestamp
            entry["example_tweet"] = f"https://twitter.com/i/status/{tweet_id}"