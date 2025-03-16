import os
from scripts.data_collection import get_nutritional_data, save_to_csv
from scripts.training import formulations, optimize_recipe
from scripts.genetic_optimizer import optimize_genetic

def collect_nutritional_data(ingredients_list):
    """Recolecta datos nutricionales y los guarda en CSV."""
    print("Recolectando datos nutricionales...")
    nutritional_data = []
    for ingredient in ingredients_list:
        data = get_nutritional_data(ingredient)
        if data:
            nutritional_data.append(data)
    if nutritional_data:
        os.makedirs('./data/processed', exist_ok=True)
        save_to_csv(nutritional_data, './data/processed/nutritional_data.csv')

def main():
    """Función principal."""
    os.makedirs('./data/processed', exist_ok=True)

    ingredients_list = [
        'cauliflower', 'chickpea', 'rice flour', 'potato flour', 'corn starch',
        'olive oil', 'xanthan gum', 'sugar', 'salt'
    ]
    collect_nutritional_data(ingredients_list)
    
    for masa_name in ['C12', 'G12']:
        optimize_genetic(masa_name)

if __name__ == "__main__":
    main()