from ...common._redis_client import RedisClient
import redis
import os

def save_progress(
    file_key: str,
    progress: str,
) -> None:
    # client = RedisClient.get_instance()
    client = redis.StrictRedis(
        host=os.getenv("REDIS_HOST"),
        password=os.getenv("REDIS_PASSWORD"),
    )
    client.set(
        key=f"pms:encoder:progress:{file_key}",
        value=progress,
        ex=1800
    )