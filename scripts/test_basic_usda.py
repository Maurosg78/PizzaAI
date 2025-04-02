import requests
import json

def test_basic_usda_connection():
    """Prueba la conexión básica con USDA API."""
    api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
    base_url = "https://api.nal.usda.gov/fdc/v1"
    
    # Búsqueda simple
    search_url = f"{base_url}/foods/search"
    params = {
        "api_key": api_key,
        "query": "pizza",
        "pageSize": 1
    }
    
    print("Realizando consulta a USDA API...")
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        print("\nConsulta exitosa!")
        print(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f} segundos")
        
        if data.get('foods'):
            food = data['foods'][0]
            print(f"\nPrimer resultado:")
            print(f"Descripción: {food.get('description')}")
            print(f"ID: {food.get('fdcId')}")
            
            # Obtener detalles del alimento
            food_url = f"{base_url}/food/{food['fdcId']}"
            food_response = requests.get(food_url, params={"api_key": api_key})
            food_response.raise_for_status()
            
            food_details = food_response.json()
            print(f"\nNutrientes encontrados: {len(food_details.get('foodNutrients', []))}")
            
            # Mostrar algunos nutrientes clave
            for nutrient in food_details.get('foodNutrients', [])[:5]:
                print(f"{nutrient.get('nutrient', {}).get('name')}: {nutrient.get('amount')} {nutrient.get('nutrient', {}).get('unitName')}")
        
    except requests.exceptions.RequestException as e:
        print(f"\nError en la consulta: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Respuesta del servidor: {e.response.text}")

if __name__ == "__main__":
    test_basic_usda_connection() 