import os
import sys
import logging

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.services.recommendation_service import RecommendationService
from src.core.config import settings

# Configurar logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

def test_recommendations():
    """Prueba el servicio de recomendaciones."""
    try:
        # Crear instancia del servicio
        service = RecommendationService()
        
        # Prueba 1: Obtener recomendaciones para un ingrediente
        base_ingredient = "tomato"
        logger.info(f"Buscando recomendaciones para: {base_ingredient}")
        recommendations = service.get_ingredient_recommendations(base_ingredient)
        
        if recommendations:
            logger.info(f"\nRecomendaciones encontradas para {base_ingredient}:")
            for rec in recommendations:
                logger.info(f"\n- {rec['description']}")
                logger.info(f"  Similitud: {rec['similarity_score']:.2f}")
                logger.info(f"  ID: {rec['fdc_id']}")
                
                # Mostrar algunos nutrientes clave
                key_nutrients = ['Protein', 'Total lipid (fat)', 'Carbohydrate, by difference', 'Energy']
                for nutrient in rec['nutrients']:
                    if nutrient.get('nutrient', {}).get('name') in key_nutrients:
                        logger.info(f"  {nutrient.get('nutrient', {}).get('name')}: {nutrient.get('amount')} {nutrient.get('nutrient', {}).get('unitName')}")
        else:
            logger.warning("No se encontraron recomendaciones")
        
        # Prueba 2: Comparar dos ingredientes
        ingredient1 = "tomato"
        ingredient2 = "bell pepper"
        logger.info(f"\nComparando {ingredient1} con {ingredient2}")
        comparison = service.get_nutritional_comparison(ingredient1, ingredient2)
        
        if comparison:
            logger.info("\nComparación nutricional:")
            for nutrient, values in comparison.items():
                logger.info(f"\n{nutrient}:")
                logger.info(f"  {ingredient1}: {values['ingredient1']}")
                logger.info(f"  {ingredient2}: {values['ingredient2']}")
                logger.info(f"  Diferencia: {values['difference']}")
        else:
            logger.warning("No se pudo realizar la comparación")
        
        logger.info("\n¡Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        logger.error(f"Error durante las pruebas: {str(e)}")
        raise

if __name__ == "__main__":
    test_recommendations() 