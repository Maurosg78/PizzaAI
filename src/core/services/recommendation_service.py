from typing import List, Dict, Optional
import logging
from src.core.services.usda_service import USDAService
from src.core.config import settings

logger = logging.getLogger(__name__)

class RecommendationService:
    """Servicio para generar recomendaciones de ingredientes."""
    
    def __init__(self):
        """Inicializa el servicio con las dependencias necesarias."""
        self.usda_service = USDAService()
        self._cache = {}  # Cache simple en memoria para pruebas
        
    def _calculate_similarity_score(self, food1: Dict, food2: Dict) -> float:
        """Calcula un puntaje de similitud entre dos alimentos basado en sus nutrientes."""
        try:
            # Obtener nutrientes clave para comparación
            nutrients1 = {n.get('nutrient', {}).get('name'): n.get('amount', 0) 
                         for n in food1.get('foodNutrients', [])}
            nutrients2 = {n.get('nutrient', {}).get('name'): n.get('amount', 0) 
                         for n in food2.get('foodNutrients', [])}
            
            # Calcular similitud basada en nutrientes comunes
            common_nutrients = set(nutrients1.keys()) & set(nutrients2.keys())
            if not common_nutrients:
                return 0.0
                
            # Calcular diferencia promedio de nutrientes
            total_diff = sum(abs(nutrients1[n] - nutrients2[n]) for n in common_nutrients)
            avg_diff = total_diff / len(common_nutrients)
            
            # Convertir a puntaje de similitud (menor diferencia = mayor similitud)
            max_diff = 100  # Valor máximo esperado de diferencia
            similarity = 1 - (avg_diff / max_diff)
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            logger.error(f"Error al calcular similitud: {str(e)}")
            return 0.0
    
    def get_ingredient_recommendations(self, base_ingredient: str, limit: int = 5) -> List[Dict]:
        """Genera recomendaciones de ingredientes similares."""
        try:
            # Verificar cache
            cache_key = f"recs:{base_ingredient}"
            if cache_key in self._cache:
                logger.info(f"Usando recomendaciones en caché para: {base_ingredient}")
                return self._cache[cache_key]
            
            # Buscar el ingrediente base
            search_results = self.usda_service.search_foods(base_ingredient, page_size=5)  # Reducir resultados iniciales
            if not search_results.get('foods'):
                logger.warning(f"No se encontraron resultados para: {base_ingredient}")
                return []
            
            # Obtener detalles del ingrediente base
            base_food = search_results['foods'][0]
            base_food_details = self.usda_service.get_food_details(base_food['fdcId'])
            
            # Buscar ingredientes similares
            similar_foods = []
            for food in search_results['foods'][1:]:  # Excluir el ingrediente base
                food_details = self.usda_service.get_food_details(food['fdcId'])
                similarity_score = self._calculate_similarity_score(base_food_details, food_details)
                
                if similarity_score > 0.3:  # Umbral mínimo de similitud
                    similar_foods.append({
                        'fdc_id': food['fdcId'],
                        'description': food['description'],
                        'similarity_score': similarity_score,
                        'nutrients': food_details.get('foodNutrients', [])
                    })
            
            # Ordenar por puntaje de similitud
            similar_foods.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Almacenar en caché
            self._cache[cache_key] = similar_foods[:limit]
            
            return similar_foods[:limit]
            
        except Exception as e:
            logger.error(f"Error al generar recomendaciones: {str(e)}")
            return []
    
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
            
            if not search1.get('foods') or not search2.get('foods'):
                return {}
            
            details1 = self.usda_service.get_food_details(search1['foods'][0]['fdcId'])
            details2 = self.usda_service.get_food_details(search2['foods'][0]['fdcId'])
            
            # Comparar nutrientes clave
            key_nutrients = {
                'Protein': 'Proteína',
                'Total lipid (fat)': 'Grasa total',
                'Carbohydrate, by difference': 'Carbohidratos',
                'Energy': 'Calorías',
                'Fiber, total dietary': 'Fibra',
                'Sodium, Na': 'Sodio'
            }
            
            comparison = {}
            for nutrient_id, nutrient_name in key_nutrients.items():
                value1 = next((n.get('amount', 0) for n in details1.get('foodNutrients', [])
                             if n.get('nutrient', {}).get('name') == nutrient_id), 0)
                value2 = next((n.get('amount', 0) for n in details2.get('foodNutrients', [])
                             if n.get('nutrient', {}).get('name') == nutrient_id), 0)
                
                comparison[nutrient_name] = {
                    'ingredient1': value1,
                    'ingredient2': value2,
                    'difference': value2 - value1
                }
            
            # Almacenar en caché
            self._cache[cache_key] = comparison
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error al comparar ingredientes: {str(e)}")
            return {} 