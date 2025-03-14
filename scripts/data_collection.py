import requests
import csv
import os
import pandas as pd

API_KEY = 'Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4'
BASE_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'

def get_nutritional_data(ingredient):
    params = {
        'query': ingredient,
        'api_key': API_KEY,
        'pageSize': 1
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Respuesta de la API para {ingredient}: {data}")  # Depuración
        if data['foods']:
            food = data['foods'][0]
            nutrients = {n['nutrientName']: n['value'] for n in food['foodNutrients']}
            result = {
                'ingredient': ingredient,
                'calories': nutrients.get('Energy', 0),
                'protein': nutrients.get('Protein', 0),
                'carbs': nutrients.get('Carbohydrate, by difference', 0),
                'fat': nutrients.get('Total lipid (fat)', 0)
            }
            print(f"Datos recolectados para {ingredient}: {result}")
            return result
        else:
            print(f"No se encontraron datos para {ingredient}")
            return None
    except requests.RequestException as e:
        print(f"Error al consultar {ingredient}: {e}")
        return None

def save_to_csv(data, filename='nutritional_data.csv'):
    filepath = os.path.join('data', filename)
    fieldnames = ['ingredient', 'calories', 'protein', 'carbs', 'fat']
    
    if os.path.exists(filepath):
        try:
            existing_data = pd.read_csv(filepath)
            if existing_data.empty or set(existing_data.columns) != set(fieldnames):
                print(f"Archivo {filename} vacío o con estructura incorrecta. Regenerando.")
                os.remove(filepath)
            elif data['ingredient'] in existing_data['ingredient'].values:
                print(f"{data['ingredient']} ya está en el archivo, no se añadirá.")
                return
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            print(f"Archivo {filename} corrupto. Regenerando.")
            os.remove(filepath)

    with open(filepath, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)
        print(f"Datos guardados para {data['ingredient']}")

if __name__ == "__main__":
    ingredients = [
        'cauliflower', 'chickpea', 'rice flour', 'potato flour', 'corn starch',
        'olive oil', 'xanthan gum', 'sugar', 'salt'
    ]
    for ingredient in ingredients:
        data = get_nutritional_data(ingredient)
        if data:
            save_to_csv(data)