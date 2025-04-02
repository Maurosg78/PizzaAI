import logging
import time
from src.core.services.simple_recommender import SimpleRecommender

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_recommender():
    """Prueba el servicio de recomendaciones."""
    try:
        # Crear instancia del recomendador
        api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
        recommender = SimpleRecommender(api_key)
        
        # Probar con diferentes ingredientes
        ingredients = ["tomato", "cheese", "pepper"]
        
        for ingredient in ingredients:
            logger.info(f"\nBuscando recomendaciones para: {ingredient}")
            start_time = time.time()
            
            recommendations = recommender.get_recommendations(ingredient)
            elapsed_time = time.time() - start_time
            
            if recommendations:
                logger.info(f"Recomendaciones encontradas para {ingredient} (tiempo: {elapsed_time:.2f}s):")
                for rec in recommendations:
                    logger.info(f"\n- {rec['description']}")
                    # Mostrar algunos nutrientes clave
                    key_nutrients = ['Protein', 'Total lipid (fat)', 'Carbohydrate, by difference', 'Energy']
                    for nutrient in rec['nutrients']:
                        if nutrient.get('nutrient', {}).get('name') in key_nutrients:
                            logger.info(f"  {nutrient.get('nutrient', {}).get('name')}: {nutrient.get('amount')} {nutrient.get('nutrient', {}).get('unitName')}")
            else:
                logger.warning(f"No se encontraron recomendaciones para {ingredient}")
        
        logger.info("\n¡Todas las pruebas completadas!")
        
    except Exception as e:
        logger.error(f"Error durante las pruebas: {str(e)}")
        raise

if __name__ == "__main__":
    test_recommender() 