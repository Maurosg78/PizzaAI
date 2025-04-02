import os
import sys
import logging

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.services.usda_service import USDAService
from src.core.config import settings

# Configurar logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

def test_usda_service():
    """Prueba el servicio USDA optimizado."""
    try:
        # Crear instancia del servicio
        service = USDAService()
        
        # Prueba 1: Búsqueda rápida
        logger.info("Realizando búsqueda rápida...")
        search_results = service.search_foods("pizza", page_size=1)
        logger.info(f"Resultados de búsqueda: {len(search_results.get('foods', []))} alimentos encontrados")
        
        # Prueba 2: Obtener detalles si hay resultados
        if search_results.get('foods'):
            fdc_id = search_results['foods'][0]['fdcId']
            logger.info(f"Obteniendo detalles del alimento con FDC ID: {fdc_id}")
            food_details = service.get_food_details(fdc_id)
            logger.info(f"Detalles del alimento: {food_details.get('description')}")
            
            # Prueba 3: Obtener información nutricional
            logger.info("Obteniendo información nutricional...")
            nutrient_info = service.get_nutrient_info(fdc_id)
            logger.info(f"Nutrientes encontrados: {len(nutrient_info)}")
            
            # Mostrar algunos nutrientes clave
            for nutrient in nutrient_info[:5]:
                logger.info(f"{nutrient.get('nutrient', {}).get('name')}: {nutrient.get('amount')} {nutrient.get('nutrient', {}).get('unitName')}")
        
        logger.info("¡Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        logger.error(f"Error durante las pruebas: {str(e)}")
        raise

if __name__ == "__main__":
    test_usda_service() 