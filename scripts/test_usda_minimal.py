import requests
import json

def test_usda_api():
    print("Iniciando prueba de la API de USDA...")
    
    api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    
    try:
        print("Haciendo petición a la API...")
        response = requests.get(
            url,
            params={
                "api_key": api_key,
                "query": "tomato",
                "pageSize": 1
            }
        )
        
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("¡Conexión exitosa!")
            data = response.json()
            print(f"Total de resultados: {data.get('totalHits', 0)}")
            
            if data.get('foods'):
                food = data['foods'][0]
                print(f"\nPrimer resultado:")
                print(f"Descripción: {food.get('description')}")
                print(f"ID: {food.get('fdcId')}")
            else:
                print("No se encontraron alimentos")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")

if __name__ == "__main__":
    test_usda_api() 