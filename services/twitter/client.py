import httpx
from tenacity import retry, wait_exponential, stop_after_attempt
from typing import Optional, Tuple
from pydantic import BaseModel


class TwitterError(BaseModel):
    code: int
    message: str
    type: str  # "api", "network", or "validation"


class TwitterClient:
    def __init__(self, bearer_token: str):
        self.client = httpx.AsyncClient(
            base_url="https://api.twitter.com/2",
            headers={"Authorization": f"Bearer {bearer_token}"},
            timeout=None
        )

    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3)
    )
    async def get_user_id(self, username: str) -> Tuple[Optional[str], Optional[TwitterError]]:
        if not self._validate_username(username):
            return None, TwitterError(
                code=400,
                message="Invalid username format",
                type="validation"
            )

        try:
            response = await self.client.get(f"/users/by/username/{username}")
            response.raise_for_status()
            return response.json()["data"]["id"], None
        except httpx.HTTPStatusError as e:
            return None, TwitterError(
                code=e.response.status_code,
                message=e.response.text,
                type="api"
            )
        except Exception as e:
            return None, TwitterError(
                code=500,
                message=str(e),
                type="network"
            )

    def _validate_username(self, username: str) -> bool:
        return bool(re.match(r'^[A-Za-z0-9_]{1,15}$', username))