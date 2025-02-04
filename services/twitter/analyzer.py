from collections import defaultdict
from datetime import datetime


class MentionAnalyzer:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.mentions = defaultdict(self._create_mention_entry)

    def analyze(self, min_mentions=1, max_results=50):
        """Process mentions with filtering and sorting"""
        self._process_raw_data()
        filtered = self._filter_mentions(min_ments)
        return self._sort_and_limit(filtered, max_results)

    def _create_mention_entry(self):
        return {"count": 0, "first": None, "last": None, "example": None}

    def _process_raw_data(self):
        for tweet in self.raw_data.get("data", []):
            created_at = datetime.fromisoformat(tweet["created_at"].rstrip("Z"))
            for mention in tweet.get("entities", {}).get("mentions", []):
                self._update_mention_entry(mention["username"], created_at, tweet["id"])

    def _update_mention_entry(self, username, timestamp, tweet_id):
        entry = self.mentions[username]
        entry["count"] += 1
        if not entry["first"] or timestamp < entry["first"]:
            entry["first"] = timestamp
        if not entry["last"] or timestamp > entry["last"]:
            entry["last"] = timestamp
            entry["example"] = f"https://twitter.com/i/status/{tweet_id}"

    def _filter_mentions(self, min_mentions):
        return {k: v for k, v in self.mentions.items() if v["count"] >= min_ments}

    @staticmethod
    def _sort_and_limit(mentions, max_results):
        return sorted(mentions.items(),
                      key=lambda x: x[1]["count"],
                      reverse=True)[:max_results]