from typing import Dict, List, Optional
import httpx
from pydantic import BaseModel
from ..config import settings

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
    """Servicio para interactuar con la API de USDA"""
    
    def __init__(self):
        self.api_key = settings.USDA_API_KEY.get_secret_value()
        self.base_url = settings.USDA_API_BASE_URL
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
    
    async def search_foods(self, query: str, page_size: int = 25) -> List[Dict]:
        """
        Busca alimentos en la base de datos de USDA
        
        Args:
            query: Término de búsqueda
            page_size: Número de resultados por página
            
        Returns:
            Lista de alimentos encontrados
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/foods/search",
                headers=self.headers,
                params={
                    "query": query,
                    "pageSize": page_size
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("foods", [])
    
    async def get_food_details(self, fdc_id: int) -> Optional[Dict]:
        """
        Obtiene detalles de un alimento específico
        
        Args:
            fdc_id: ID del alimento en la base de datos de USDA
            
        Returns:
            Detalles del alimento o None si no se encuentra
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/food/{fdc_id}",
                headers=self.headers
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
    
    async def get_nutrient_info(self, fdc_id: int) -> List[NutrientInfo]:
        """
        Obtiene información nutricional de un alimento
        
        Args:
            fdc_id: ID del alimento en la base de datos de USDA
            
        Returns:
            Lista de nutrientes con sus valores
        """
        food_data = await self.get_food_details(fdc_id)
        if not food_data:
            return []
        
        nutrients = []
        for nutrient_data in food_data.get("foodNutrients", []):
            # Verificar que todos los campos requeridos estén presentes y sean válidos
            nutrient = nutrient_data.get("nutrient", {})
            nutrient_id = nutrient.get("id")
            nutrient_name = nutrient.get("name")
            value = nutrient_data.get("amount")
            unit = nutrient.get("unitName")
            
            if all([nutrient_id, nutrient_name, value is not None, unit]):
                try:
                    nutrients.append(NutrientInfo(
                        nutrient_id=nutrient_id,
                        nutrient_name=nutrient_name,
                        value=float(value),
                        unit=unit
                    ))
                except (ValueError, TypeError):
                    continue  # Ignorar nutrientes con valores inválidos
        
        return nutrients

# Crear una instancia global del servicio
usda_service = USDAService() 