import os

from aiocache import Cache
from aiocache.serializers import JsonSerializer

REDIS_ENDPOINT = os.getenv("REDIS_ENDPOINT") or "redis-image"
REDIS_CONF = {
    "ttl": 864000,
    "cache": Cache.REDIS,
    "endpoint": "redis-image",
    "serializer": JsonSerializer()
}