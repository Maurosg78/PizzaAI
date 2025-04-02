import logging
import os
import sys

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.config import settings
from src.core.services.usda_service import USDAService

# Configurar logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def test_usda_connection():
    """Prueba la conexión con USDA API y el sistema de caché."""
    try:
        # Crear instancia del servicio
        usda_service = USDAService()

        # Prueba 1: Búsqueda de alimentos
        logger.info("Probando búsqueda de alimentos...")
        search_results = usda_service.search_foods("pizza")
        logger.info(
            f"Resultados de búsqueda: {len(search_results.get('foods', []))} alimentos encontrados"
        )

        # Prueba 2: Obtener detalles de un alimento
        if search_results.get("foods"):
            fdc_id = search_results["foods"][0]["fdcId"]
            logger.info(f"Obteniendo detalles del alimento con FDC ID: {fdc_id}")
            food_details = usda_service.get_food_details(fdc_id)
            logger.info(f"Detalles del alimento: {food_details.get('description')}")

            # Prueba 3: Obtener información nutricional
            logger.info("Obteniendo información nutricional...")
            nutrient_info = usda_service.get_nutrient_info(fdc_id)
            logger.info(f"Nutrientes encontrados: {len(nutrient_info)}")

            # Mostrar algunos nutrientes clave
            for nutrient in nutrient_info[:5]:
                logger.info(f"{nutrient.nutrient_name}: {nutrient.value} {nutrient.unit}")

        logger.info("¡Todas las pruebas completadas exitosamente!")

    except Exception as e:
        logger.error(f"Error durante las pruebas: {str(e)}")
        raise


if __name__ == "__main__":
    test_usda_connection()
