import requests
import json
import time
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_usda_api():
    """Prueba directa de la API de USDA."""
    try:
        # Configuración
        api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
        base_url = "https://api.nal.usda.gov/fdc/v1"
        
        # Headers
        headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Probar búsqueda de alimentos
        logger.info("Probando búsqueda de alimentos...")
        start_time = time.time()
        
        response = requests.get(
            f"{base_url}/foods/search",
            headers=headers,
            params={
                "query": "tomato",
                "pageSize": 1,
                "dataType": ["Survey (FNDDS)", "Foundation", "SR Legacy"]
            }
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"Búsqueda completada en {elapsed_time:.2f} segundos")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("¡Búsqueda exitosa!")
            logger.info(f"Total de resultados: {data.get('totalHits', 0)}")
            
            if data.get('foods'):
                food = data['foods'][0]
                logger.info(f"\nPrimer resultado:")
                logger.info(f"Descripción: {food.get('description')}")
                logger.info(f"ID: {food.get('fdcId')}")
                
                # Obtener detalles del alimento
                logger.info("\nObteniendo detalles del alimento...")
                fdc_id = food['fdcId']
                detail_response = requests.get(
                    f"{base_url}/food/{fdc_id}",
                    headers=headers
                )
                
                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    logger.info("¡Detalles obtenidos exitosamente!")
                    
                    # Mostrar algunos nutrientes clave
                    key_nutrients = ['Protein', 'Total lipid (fat)', 'Carbohydrate, by difference', 'Energy']
                    logger.info("\nNutrientes principales:")
                    for nutrient in detail_data.get('foodNutrients', []):
                        if nutrient.get('nutrient', {}).get('name') in key_nutrients:
                            logger.info(f"{nutrient.get('nutrient', {}).get('name')}: {nutrient.get('amount')} {nutrient.get('nutrient', {}).get('unitName')}")
                else:
                    logger.error(f"Error al obtener detalles: {detail_response.status_code}")
            else:
                logger.warning("No se encontraron alimentos")
        else:
            logger.error(f"Error en la búsqueda: {response.status_code}")
            logger.error(f"Respuesta: {response.text}")
            
    except Exception as e:
        logger.error(f"Error durante la prueba: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Iniciando prueba directa de la API de USDA...")
    test_usda_api() 