from huey import RedisHuey
import redis
import json
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables for Redis configuration
# REDIS_HOST = os.getenv("REDIS_HOST", "redis")
# REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
# REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Initialize Huey with Redis backend
huey = RedisHuey('my-huey-app', host='redis', port=6379, db=0)
# Redis connection
red = redis.Redis(host='redis', port=6379, db=0)
logger.info("Connection to Redis established")

@huey.task()
def store_key_value_to_redis(key, value):
    try:
        logger.info(f"Inside store_key_value_to_redis: {key}: {value}")

        if not isinstance(value, (str, bytes)):
            value = json.dumps(value)
        red.set(key, value)
        logger.info(f"Successfully stored key-value pair: {key}: {value}")
    except Exception as e:
        logger.error(f"Error storing key-value: {e}")

@huey.task()
def retrieve_value_from_redis(key):
    try:
        value = red.get(key)
        if value is not None:
            value = json.loads(value)
        else:
            logger.info(f"Key {key} does not exist in Redis")
        return value
    except (TypeError, json.JSONDecodeError) as e:
        logger.error(f"Error retrieving key {key} from Redis: {e}")
        return None

@huey.task()
def delete_key_from_redis(key):
    try:
        result = red.delete(key)
        if result > 0:
            logger.info(f"Successfully deleted key: {key}")
            return True
        else:
            logger.info(f"Key {key} does not exist. Nothing to delete.")
            return False
    except Exception as e:
        logger.error(f"Error deleting key {key}: {e}")
        return False
