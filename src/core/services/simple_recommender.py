import logging
import time
from functools import lru_cache
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class SimpleRecommender:
    """Servicio simple de recomendaciones que usa directamente la API de USDA."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nal.usda.gov/fdc/v1"
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": self.api_key, "Content-Type": "application/json"})

    @lru_cache(maxsize=100)
    def search_foods(self, query: str, page_size: int = 5) -> List[Dict]:
        """Busca alimentos en la base de datos de USDA con caché."""
        try:
            logger.info(f"Buscando alimentos para: {query}")
            start_time = time.time()

            response = self.session.get(
                f"{self.base_url}/foods/search",
                params={
                    "query": query,
                    "pageSize": page_size,
                    "dataType": ["Survey (FNDDS)", "Foundation", "SR Legacy"],
                },
            )
            response.raise_for_status()
            data = response.json()

            elapsed_time = time.time() - start_time
            logger.info(f"Búsqueda completada en {elapsed_time:.2f} segundos")
            return data.get("foods", [])

        except Exception as e:
            logger.error(f"Error al buscar alimentos: {str(e)}")
            return []

    @lru_cache(maxsize=100)
    def get_food_details(self, fdc_id: int) -> Optional[Dict]:
        """Obtiene detalles de un alimento específico con caché."""
        try:
            logger.info(f"Obteniendo detalles para alimento ID: {fdc_id}")
            start_time = time.time()

            response = self.session.get(f"{self.base_url}/food/{fdc_id}")
            response.raise_for_status()
            data = response.json()

            elapsed_time = time.time() - start_time
            logger.info(f"Detalles obtenidos en {elapsed_time:.2f} segundos")
            return data

        except Exception as e:
            logger.error(f"Error al obtener detalles del alimento {fdc_id}: {str(e)}")
            return None

    def get_recommendations(self, base_ingredient: str, limit: int = 3) -> List[Dict]:
        """Genera recomendaciones de ingredientes similares."""
        try:
            logger.info(f"Generando recomendaciones para: {base_ingredient}")
            start_time = time.time()

            # Buscar el ingrediente base y otros ingredientes similares
            foods = self.search_foods(base_ingredient, page_size=limit + 1)
            if not foods:
                logger.warning(f"No se encontraron alimentos para: {base_ingredient}")
                return []

            # Obtener detalles del ingrediente base
            base_food = foods[0]
            base_details = self.get_food_details(base_food["fdcId"])
            if not base_details:
                logger.warning(f"No se pudieron obtener detalles para: {base_ingredient}")
                return []

            # Obtener detalles de los ingredientes similares
            recommendations = []
            for food in foods[1:]:  # Excluir el ingrediente base
                details = self.get_food_details(food["fdcId"])
                if details:
                    recommendations.append(
                        {
                            "fdc_id": food["fdcId"],
                            "description": food["description"],
                            "nutrients": details.get("foodNutrients", []),
                        }
                    )

            elapsed_time = time.time() - start_time
            logger.info(f"Recomendaciones generadas en {elapsed_time:.2f} segundos")
            return recommendations[:limit]

        except Exception as e:
            logger.error(f"Error al generar recomendaciones: {str(e)}")
            return []
