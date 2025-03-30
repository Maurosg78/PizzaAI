from typing import Any, Optional
import json
import redis
from datetime import timedelta
from src.core.config import settings

class RedisCache:
    """Implementación de caché usando Redis"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtener valor del caché"""
        value = self.redis_client.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: Any, ttl: timedelta) -> bool:
        """Guardar valor en caché con TTL"""
        return self.redis_client.setex(
            key,
            int(ttl.total_seconds()),
            json.dumps(value)
        )
    
    async def delete(self, key: str) -> bool:
        """Eliminar valor del caché"""
        return bool(self.redis_client.delete(key))
    
    async def clear(self) -> bool:
        """Limpiar todo el caché"""
        return bool(self.redis_client.flushdb())
    
    async def exists(self, key: str) -> bool:
        """Verificar si existe una clave en el caché"""
        return bool(self.redis_client.exists(key)) 