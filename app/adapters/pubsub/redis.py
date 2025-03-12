import redis.asyncio as redis

from app.business_logic.models import PubSubChannel
from app.business_logic.ports import PubSubManager


class RedisPubSubManager(PubSubManager):
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        if not self.redis:
            self.redis = await redis.from_url(self.redis_url)

    async def subscribe(self, channel: PubSubChannel):
        await self.connect()
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel.value)
        return pubsub  # ❌ Don't store pubsub globally (fixed)

    async def unsubscribe(self, pubsub, channel: PubSubChannel):
        await pubsub.unsubscribe(channel.value)
        await pubsub.close()

    async def publish(self, channel: PubSubChannel, message: str):
        await self.connect()
        await self.redis.publish(channel.value, message)

    async def close(self):
        if self.redis:
            await self.redis.close()
            self.redis = None
