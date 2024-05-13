import redis
import os

class RedisClient:
    _instasnce = None
    
    @staticmethod
    def get_instance():
        if RedisClient._instance is None:
            RedisClient._instance = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                password=os.getenv("REDIS_PASSWORD"),
                db=0,
            )
        
        return RedisClient._instance