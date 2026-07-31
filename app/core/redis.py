import json
import logging
import os
from typing import Any

import redis

logger = logging.getLogger(__name__)

# db: số thứ tự của database logic bên trong Redis (Redis chia nhiền phân vùng: DB 0, DB 1, DB2,... )
# decode_response: Redis lưu DL dưới dạng bytes, nếu không bật lên thì nó vẫn giữ dạng bytes
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=os.getenv("REDIS_PORT", "6379"),
    db=os.getenv("REDIS_DB", "0"),
    decode_responses=True,
)


class CacheService:
    @staticmethod
    def get(key: str) -> Any | None:
        try:
            data = redis_client.get(key)
            return json.loads(data) if data else None
        except (redis.RedisError, json.JSONDecodeError, TypeError) as e:
            logger.warning(f"Redis get error: {e}")
            return None

    @staticmethod
    def set(key: str, value: Any, ttl_seconds: int = 300) -> None:
        try:
            redis_client.setex(key, ttl_seconds, json.dumps(value, default=str))
        except (redis.RedisError, TypeError) as e:
            logger.warning(f"Redis set error: {e}")

    @staticmethod
    def delete_pattern(pattern: str) -> None:
        """
        Tìm tất cả các cache key khớp với một mẫu pattern rồi xóa toàn bộ các key đó
        *keys: tách các phần tử trong list thành từng đối số riêng
        """
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
        except redis.RedisError as e:
            logger.warning(f"Redis delete error: {e}")
