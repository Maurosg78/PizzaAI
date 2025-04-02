import logging
import sys
import os
import time

# Configurar logging con más detalle
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agregar el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

logger.info(f"Directorio actual: {current_dir}")
logger.info(f"Directorio raíz: {root_dir}")

try:
    from src.core.services.simple_recommender import SimpleRecommender
    logger.info("Importación de SimpleRecommender exitosa")
except ImportError as e:
    logger.error(f"Error al importar SimpleRecommender: {str(e)}")
    sys.exit(1)

def test_recommender():
    """Prueba el servicio simple de recomendaciones."""
    try:
        logger.info("Iniciando prueba del recomendador...")
        
        # Crear instancia del recomendador
        api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
        logger.info("Creando instancia de SimpleRecommender...")
        recommender = SimpleRecommender(api_key)
        
        # Probar con diferentes ingredientes
        ingredients = ["tomato", "cheese", "pepper"]
        
        for ingredient in ingredients:
            logger.info(f"\nBuscando recomendaciones para: {ingredient}")
            start_time = time.time()
            
            try:
                recommendations = recommender.get_recommendations(ingredient)
                elapsed_time = time.time() - start_time
                logger.info(f"Búsqueda completada en {elapsed_time:.2f} segundos")
                
                if recommendations:
                    logger.info(f"Recomendaciones encontradas para {ingredient}:")
                    for rec in recommendations:
                        logger.info(f"\n- {rec['description']}")
                        # Mostrar algunos nutrientes clave
                        key_nutrients = ['Protein', 'Total lipid (fat)', 'Carbohydrate, by difference', 'Energy']
                        for nutrient in rec['nutrients']:
                            if nutrient.get('nutrient', {}).get('name') in key_nutrients:
                                logger.info(f"  {nutrient.get('nutrient', {}).get('name')}: {nutrient.get('amount')} {nutrient.get('nutrient', {}).get('unitName')}")
                else:
                    logger.warning(f"No se encontraron recomendaciones para {ingredient}")
            except Exception as e:
                logger.error(f"Error al buscar recomendaciones para {ingredient}: {str(e)}")
                continue
        
        logger.info("\n¡Todas las pruebas completadas!")
        
    except Exception as e:
        logger.error(f"Error durante las pruebas: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Iniciando script de prueba...")
    test_recommender() 