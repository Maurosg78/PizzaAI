import os
import sys
import logging

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.services.recommendation_service import RecommendationService
from src.core.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_recommendations():
    """Prueba rápida del servicio de recomendaciones."""
    try:
        service = RecommendationService()
        
        # Prueba simple de recomendaciones
        ingredient = "tomato"
        logger.info(f"Buscando recomendaciones para: {ingredient}")
        recommendations = service.get_ingredient_recommendations(ingredient, limit=3)
        
        if recommendations:
            logger.info("\nRecomendaciones encontradas:")
            for rec in recommendations:
                logger.info(f"- {rec['description']} (Similitud: {rec['similarity_score']:.2f})")
        else:
            logger.warning("No se encontraron recomendaciones")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    test_recommendations() 