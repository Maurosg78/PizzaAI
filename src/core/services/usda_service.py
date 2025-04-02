from typing import Dict, List, Optional
import httpx
from pydantic import BaseModel
from ..config import settings
import logging
from ..cache.redis_cache import RedisCache
from .usda_client import USDAClient

logger = logging.getLogger(__name__)

class NutrientInfo(BaseModel):
    """Información nutricional de un alimento"""
    nutrient_id: int
    nutrient_name: str
    value: float
    unit: str

class FoodItem(BaseModel):
    """Información de un alimento"""
    fdc_id: int
    description: str
    nutrients: List[NutrientInfo]
    serving_size: float
    serving_size_unit: str

class USDAService:
    """Servicio para interactuar con la API de USDA."""
    
    def __init__(self):
        """Inicializa el servicio con el cliente USDA y caché Redis."""
        self.client = USDAClient()
        self.cache = RedisCache()
        
    def _generate_cache_key(self, prefix: str, params: Dict) -> str:
        """Genera una clave de caché única basada en los parámetros."""
        return f"usda:{prefix}:{':'.join(f'{k}={v}' for k, v in sorted(params.items()))}"
    
    def search_foods(self, query: str, page_size: int = 10) -> Dict:
        """Busca alimentos en la USDA API con caché."""
        cache_key = self._generate_cache_key("search", {"query": query, "page_size": page_size})
        
        # Intentar obtener de caché
        cached_result = self.cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit para búsqueda: {query}")
            return cached_result
        
        # Si no está en caché, hacer la petición
        logger.info(f"Realizando búsqueda en USDA API: {query}")
        result = self.client.search_foods(query, page_size)
        
        # Almacenar en caché por 1 hora
        self.cache.set(cache_key, result, expire=3600)
        return result
    
    def get_food_details(self, fdc_id: int) -> Dict:
        """Obtiene detalles de un alimento específico con caché."""
        cache_key = self._generate_cache_key("food", {"fdc_id": fdc_id})
        
        # Intentar obtener de caché
        cached_result = self.cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit para alimento: {fdc_id}")
            return cached_result
        
        # Si no está en caché, hacer la petición
        logger.info(f"Obteniendo detalles de alimento: {fdc_id}")
        result = self.client.get_food_details(fdc_id)
        
        # Almacenar en caché por 24 horas
        self.cache.set(cache_key, result, expire=86400)
        return result
    
    def get_nutrient_info(self, fdc_id: int) -> List[Dict]:
        """Obtiene información nutricional de un alimento específico."""
        food_details = self.get_food_details(fdc_id)
        return food_details.get('foodNutrients', [])

# Crear una instancia global del servicio
usda_service = USDAService() 