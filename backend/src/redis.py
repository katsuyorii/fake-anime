from redis.asyncio import Redis

from .config import settings


redis_client = Redis.from_url(
    url=settings.REDIS_URL,
)

async def get_redis():
    async with redis_client.client() as redis:
        yield redis