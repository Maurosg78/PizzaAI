import requests

def test_simple_usda_query():
    """Realiza una consulta simple a la API de USDA."""
    api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
    base_url = "https://api.nal.usda.gov/fdc/v1"
    
    # Búsqueda simple de pizza
    search_url = f"{base_url}/foods/search"
    params = {
        "api_key": api_key,
        "query": "pizza",
        "pageSize": 1
    }
    
    print("Realizando consulta a USDA API...")
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print("\nConsulta exitosa!")
        print(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f} segundos")
        if data.get('foods'):
            food = data['foods'][0]
            print(f"\nPrimer resultado:")
            print(f"Descripción: {food.get('description')}")
            print(f"ID: {food.get('fdcId')}")
    else:
        print(f"\nError en la consulta: {response.status_code}")
        print(f"Mensaje: {response.text}")

if __name__ == "__main__":
    test_simple_usda_query() 