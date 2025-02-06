from redis.asyncio import Redis, ConnectionPool
from config.settings import settings

class RedisManager:
    _pool: ConnectionPool = None

    @classmethod
    async def get_client(cls) -> Redis:
        if not cls._pool:
            cls._pool = ConnectionPool.from_url(
                str(settings.REDIS_URL),
                max_connections=20,
                decode_responses=True
            )
        return Redis(connection_pool=cls._pool)