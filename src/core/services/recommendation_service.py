import logging
from typing import Dict, List

from src.core.services.usda_service import USDAService

logger = logging.getLogger(__name__)


class RecommendationService:
    """Servicio para generar recomendaciones de ingredientes."""

    def __init__(self, usda_service: USDAService):
        """Inicializa el servicio con las dependencias necesarias."""
        self.usda_service = usda_service
        self._cache = {}  # Cache simple en memoria para pruebas

    def get_recommendations(self, base_ingredient: str, limit: int = 5) -> List[Dict]:
        """
        Genera recomendaciones basadas en un ingrediente base.

        Args:
            base_ingredient: Nombre del ingrediente base
            limit: Número máximo de recomendaciones

        Returns:
            Lista de ingredientes recomendados
        """
        # Obtener datos del ingrediente base
        base_data = self.usda_service.get_food_nutrition(base_ingredient)
        if not base_data:
            return []

        # Buscar ingredientes similares
        similar_foods = self.usda_service.search_foods(base_ingredient, page_size=limit + 1)

        # Filtrar el ingrediente base y limitar resultados
        recommendations = [
            food for food in similar_foods if str(food["fdcId"]) != str(base_data.get("fdcId"))
        ][:limit]

        # Enriquecer con detalles nutricionales
        return [self._enrich_recommendation(food) for food in recommendations]

    def _enrich_recommendation(self, food: Dict) -> Dict:
        """Enriquece una recomendación con datos nutricionales."""
        details = self.usda_service.get_food_details(str(food["fdcId"]))

        return {
            "id": food["fdcId"],
            "name": food["description"],
            "score": self._calculate_similarity_score(details),
            "nutrients": self._extract_key_nutrients(details),
        }

    def _calculate_similarity_score(self, food_details: Dict) -> float:
        """Calcula un puntaje de similitud basado en nutrientes."""
        nutrients = food_details.get("foodNutrients", [])
        if not nutrients:
            return 0.0

        # Puntaje basado en presencia de nutrientes clave
        score = 0.0
        total_nutrients = len(nutrients)

        for nutrient in nutrients:
            if nutrient.get("nutrientName", "").lower() in {
                "protein",
                "total lipid (fat)",
                "carbohydrate",
                "fiber",
                "calcium",
                "iron",
                "magnesium",
                "phosphorus",
                "potassium",
                "sodium",
                "zinc",
                "vitamin c",
                "vitamin b6",
                "vitamin b12",
            }:
                score += 1

        return score / max(total_nutrients, 1) * 10

    def _extract_key_nutrients(self, food_details: Dict) -> Dict[str, float]:
        """Extrae los nutrientes clave de los detalles del alimento."""
        nutrients = {}
        for nutrient in food_details.get("foodNutrients", []):
            name = nutrient.get("nutrientName", "").lower()
            if name in {
                "protein",
                "total lipid (fat)",
                "carbohydrate",
                "fiber",
                "calcium",
                "iron",
                "magnesium",
                "potassium",
                "sodium",
            }:
                nutrients[name] = nutrient.get("value", 0.0)

        return nutrients

    def get_nutritional_comparison(self, ingredient1: str, ingredient2: str) -> Dict:
        """Compara el perfil nutricional de dos ingredientes."""
        try:
            # Verificar cache
            cache_key = f"comp:{ingredient1}:{ingredient2}"
            if cache_key in self._cache:
                logger.info(f"Usando comparación en caché para: {ingredient1} y {ingredient2}")
                return self._cache[cache_key]

            # Obtener detalles de ambos ingredientes
            search1 = self.usda_service.search_foods(ingredient1, page_size=1)
            search2 = self.usda_service.search_foods(ingredient2, page_size=1)

            if not search1.get("foods") or not search2.get("foods"):
                return {}

            details1 = self.usda_service.get_food_details(search1["foods"][0]["fdcId"])
            details2 = self.usda_service.get_food_details(search2["foods"][0]["fdcId"])

            # Comparar nutrientes clave
            key_nutrients = {
                "Protein": "Proteína",
                "Total lipid (fat)": "Grasa total",
                "Carbohydrate, by difference": "Carbohidratos",
                "Energy": "Calorías",
                "Fiber, total dietary": "Fibra",
                "Sodium, Na": "Sodio",
            }

            comparison = {}
            for nutrient_id, nutrient_name in key_nutrients.items():
                value1 = next(
                    (
                        n.get("amount", 0)
                        for n in details1.get("foodNutrients", [])
                        if n.get("nutrient", {}).get("name") == nutrient_id
                    ),
                    0,
                )
                value2 = next(
                    (
                        n.get("amount", 0)
                        for n in details2.get("foodNutrients", [])
                        if n.get("nutrient", {}).get("name") == nutrient_id
                    ),
                    0,
                )

                comparison[nutrient_name] = {
                    "ingredient1": value1,
                    "ingredient2": value2,
                    "difference": value2 - value1,
                }

            # Almacenar en caché
            self._cache[cache_key] = comparison

            return comparison

        except Exception as e:
            logger.error(f"Error al comparar ingredientes: {str(e)}")
            return {}
