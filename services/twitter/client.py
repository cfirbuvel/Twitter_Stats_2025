import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

class TwitterClient:
    def __init__(self, bearer_token: str):
        self.client = httpx.AsyncClient(
            base_url="https://api.twitter.com/2",
            headers={
                "Authorization": f"Bearer {bearer_token}",
                "User-Agent": "MentionAnalyzer/4.0"
            },
            timeout=30
        )

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
    async def get_user_id(self, username: str) -> str:
        try:
            response = await self.client.get(f"/users/by/username/{username}")
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("id")
        except httpx.HTTPStatusError as e:
            return f"❌ Twitter API error: {e.response.text}"
        except httpx.RequestError as e:
            return f"❌ Network error: {str(e)}"

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
    async def get_tweets(self, user_id: str):
        """Fetch recent tweets for a user."""
        try:
            response = await self.client.get(f"/users/{user_id}/tweets")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return f"❌ Twitter API error: {e.response.text}"
        except httpx.RequestError as e:
            return f"❌ Network error: {str(e)}"