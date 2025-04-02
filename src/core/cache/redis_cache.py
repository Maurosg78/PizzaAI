import json
import logging
from typing import Any, Optional

import redis
from pydantic import BaseModel

from ..config import get_settings

logger = logging.getLogger(__name__)


class RedisCache:
    """Servicio de caché usando Redis."""

    def __init__(self):
        settings = get_settings()
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
        )

    def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor de la caché."""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Error al obtener valor de caché: {str(e)}")
        return None

    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Almacena un valor en la caché."""
        try:
            if isinstance(value, BaseModel):
                value = value.dict()
            self.redis_client.setex(key, expire, json.dumps(value))
            return True
        except Exception as e:
            logger.error(f"Error al almacenar valor en caché: {str(e)}")
            return False

    def delete(self, key: str) -> bool:
        """Elimina un valor de la caché."""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error al eliminar valor de caché: {str(e)}")
            return False

    def exists(self, key: str) -> bool:
        """Verifica si una clave existe en la caché."""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error al verificar existencia en caché: {str(e)}")
            return False
