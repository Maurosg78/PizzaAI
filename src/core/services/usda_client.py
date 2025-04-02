import logging
import requests
from typing import Dict, Optional
from src.core.config import settings

logger = logging.getLogger(__name__)

class USDAClient:
    """Cliente para interactuar con la API de USDA."""
    
    def __init__(self):
        """Inicializa el cliente con la configuración necesaria."""
        self.api_key = settings.USDA_API_KEY
        self.base_url = settings.USDA_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        })
        self._cache = {}  # Cache simple en memoria para pruebas
    
    def search_foods(self, query: str, page_size: int = 5) -> Dict:
        """Busca alimentos en la base de datos de USDA."""
        try:
            # Verificar cache
            cache_key = f"search:{query}:{page_size}"
            if cache_key in self._cache:
                logger.info(f"Usando búsqueda en caché para: {query}")
                return self._cache[cache_key]
            
            response = self.session.get(
                f"{self.base_url}/foods/search",
                params={
                    "query": query,
                    "pageSize": page_size,
                    "dataType": ["Survey (FNDDS)", "Foundation", "SR Legacy"]
                }
            )
            response.raise_for_status()
            result = response.json()
            
            # Almacenar en caché
            self._cache[cache_key] = result
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al buscar alimentos: {str(e)}")
            return {"foods": [], "totalHits": 0, "currentPage": 1, "totalPages": 0}
    
    def get_food_details(self, fdc_id: int) -> Dict:
        """Obtiene detalles de un alimento específico."""
        try:
            # Verificar cache
            cache_key = f"food:{fdc_id}"
            if cache_key in self._cache:
                logger.info(f"Usando detalles en caché para alimento: {fdc_id}")
                return self._cache[cache_key]
            
            response = self.session.get(f"{self.base_url}/food/{fdc_id}")
            response.raise_for_status()
            result = response.json()
            
            # Almacenar en caché
            self._cache[cache_key] = result
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener detalles del alimento {fdc_id}: {str(e)}")
            return {}
    
    def parse_nutrition_data(self, food_data: Dict) -> Dict:
        """Parsea los datos nutricionales de la respuesta de USDA."""
        nutrients = {}
        
        # Mapeo de nutrientes clave
        nutrient_map = {
            "Energy": "calories",
            "Protein": "protein",
            "Carbohydrate, by difference": "carbs",
            "Total lipid (fat)": "fat",
            "Fiber, total dietary": "fiber",
            "Sugars, total including NLEA": "sugar",
            "Sodium, Na": "sodium"
        }
        
        for nutrient in food_data.get("foodNutrients", []):
            nutrient_name = nutrient.get("nutrientName")
            if nutrient_name in nutrient_map:
                nutrients[nutrient_map[nutrient_name]] = nutrient.get("value", 0)
        
        return {
            "name": food_data.get("description", ""),
            "fdc_id": food_data.get("fdcId"),
            "nutrients": nutrients
        }
    
    def get_food_by_name(self, name: str) -> Optional[Dict]:
        """Busca un alimento por nombre y devuelve sus detalles nutricionales."""
        try:
            search_results = self.search_foods(name, page_size=1)
            if search_results.get("foods"):
                fdc_id = search_results["foods"][0]["fdcId"]
                food_details = self.get_food_details(fdc_id)
                return self.parse_nutrition_data(food_details)
        except Exception as e:
            logger.error(f"Error al buscar alimento por nombre: {str(e)}")
        return None 