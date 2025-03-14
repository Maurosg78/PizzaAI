import os
from scripts.data_collection import get_nutritional_data, save_to_csv
from scripts.training import formulations, optimize_recipe
from scripts.genetic_optimizer import optimize_genetic

def collect_nutritional_data(ingredients_list):
    """Recolecta datos nutricionales de la API de USDA y los guarda en CSV."""
    print("Recolectando datos nutricionales...")
    for ingredient in ingredients_list:
        data = get_nutritional_data(ingredient)
        if data:
            save_to_csv(data)

def generate_simulated_data():
    """Genera datos simulados si no existen."""
    print("Generando datos simulados...")
    if not os.path.exists('data/experimental_data.csv'):
        from scripts import preprocessing  # Asume que este módulo genera datos simulados

def optimize_traditional(masa_name):
    """Optimiza una receta de forma tradicional y muestra los resultados."""
    masa = formulations[masa_name]
    print(f"\n--- Masa {masa_name} ---")
    result = masa.predict_properties()
    print(f"Elasticidad base: {result['elasticity']:.2f}")
    print(f"Densidad base: {result['density']:.2f}")
    print(f"Calorías base: {result['calories']:.2f}")
    print(f"Proteína base: {result['protein']:.2f}")
    
    print("Mejor receta optimizada (densidad mínima):")
    min_elasticity = 0.4 if masa_name == 'C12' else 0.5  # Ajuste para C12 y G12
    optimal = optimize_recipe(masa_name, target='min_density', min_elasticity=min_elasticity, max_calories=300)
    if optimal:
        print(f"Elasticidad: {optimal['elasticity']:.2f}")
        print(f"Densidad: {optimal['density']:.2f}")
        print(f"Calorías: {optimal['calories']:.2f}")
        print(f"Proteína: {optimal['protein']:.2f}")
        print("Formulación optimizada:", {k: f"{v:.3f}" for k, v in optimal['formulation'].items()})
    else:
        print("No se encontró una receta optimizada.")

def main():
    """Función principal para coordinar el flujo del programa."""
    ingredients_list = [
        'cauliflower', 'chickpea', 'rice flour', 'potato flour', 'corn starch',
        'olive oil', 'xanthan gum', 'sugar', 'salt'
    ]
    collect_nutritional_data(ingredients_list)
    generate_simulated_data()
    for masa_name in ['C12', 'G12']:
        optimize_traditional(masa_name)
        optimize_genetic(masa_name)

if __name__ == "__main__":
    main()