import random
import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
import matplotlib
matplotlib.use('TkAgg')  # Backend estable para evitar bloqueos
import matplotlib.pyplot as plt
from functools import partial
import os

# Inicializar generador de números aleatorios
rng = random.Random()

# Constantes para ingredientes
CORN_STARCH = 'corn starch'
XANTHAN_GUM = 'xanthan gum'

# Diccionario de ingredientes base para cada masa
BASE_INGREDIENTS = {
    'G12': 'chickpea_flour',  # Harina de garbanzo para G12
    'C12': 'cauliflower'      # Coliflor para C12
}

# Lista de ingredientes ajustables comunes
ADJUSTABLE_INGREDIENTS = [
    'rice_flour',
    'potato_flour',
    CORN_STARCH,
    'olive_oil',
    XANTHAN_GUM,
    'sugar',
    'salt',
    'vinegar'  # Para reducir sabor a legumbre
]

# Sustitutos para ciertos ingredientes
SUBSTITUTES = {
    'chickpea_flour': ['almond_flour', 'coconut_flour'],
    'rice_flour': ['potato_flour', CORN_STARCH]
}

# ----------------------------------------------------------------------
# 1. Cargar datos y preparar diccionarios
# ----------------------------------------------------------------------
try:
    print("Cargando el archivo CSV 'ingredients_data_gluten_free.csv'...")
    df = pd.read_csv('./data/processed/ingredients_data_gluten_free.csv', encoding='utf-8', delimiter=',')
    print("Archivo cargado correctamente. Contenido del DataFrame:")
    print(df)
    df['ingredient'] = df['ingredient'].str.strip().str.lower()
    ingredients_data = df.set_index('ingredient').to_dict('index')
    print("Datos de ingredientes procesados:", ingredients_data)
except FileNotFoundError:
    print("Error: No se encontró './data/processed/ingredients_data_gluten_free.csv'. Creando datos simulados.")
    df = pd.DataFrame([
        ['chickpea_flour', 400.0, 16.67, 70.0, 5.0, 16.7, 0.0],
        ['white_rice_flour', 375.0, 7.5, 82.5, 0.0, 0.0, 0.0],
        ['tapioca_starch', 375.0, 0.0, 87.5, 0.0, None, 300.0],
        ['potato_starch', 333.0, 0.0, 83.33, 0.0, 0.0, 0.0],
        ['corn_starch', 350.0, 0.0, 90.0, 0.0, None, 0.0],
        ['xanthan_gum', 625.0, 0.0, 125.0, 0.0, None, 3125.0],
        ['guar_gum', 357.0, 0.0, 71.43, 0.0, 71.4, 0.0],
        ['water', 42.0, 0.0, 10.83, 0.0, None, 8.0],
        ['olive_oil', 900.0, 0.0, 0.0, 100.0, 0.0, 2.0],
        ['dry_yeast', 1361.0, 40.44, 41.22, 7.61, 26.9, 51.0]
    ], columns=['ingredient', 'calories', 'protein', 'carbs', 'fat', 'fiber', 'sodium'])
    os.makedirs('./data/processed', exist_ok=True)
    df.to_csv('./data/processed/ingredients_data_gluten_free.csv', index=False)
    df['ingredient'] = df['ingredient'].str.strip().str.lower()
    ingredients_data = df.set_index('ingredient').to_dict('index')
    print("Datos simulados generados y guardados en './data/processed/ingredients_data_gluten_free.csv'.")
except Exception as e:
    print(f"Error inesperado al cargar el archivo CSV: {e}")
    raise

print("Ingredientes disponibles:", list(ingredients_data.keys()))

# ----------------------------------------------------------------------
# 2. Configurar DEAP para optimización multiobjetivo
# ----------------------------------------------------------------------
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))  # Minimizar densidad, maximizar elasticidad
creator.create("Individual", list, fitness=creator.FitnessMulti)

# ----------------------------------------------------------------------
# 3. Funciones auxiliares
# ----------------------------------------------------------------------
def get_ingredients_for_masa(masa_name):
    """Devuelve lista de ingredientes para la masa especificada."""
    base_ing = ['water', BASE_INGREDIENTS[masa_name]]
    return base_ing + ADJUSTABLE_INGREDIENTS

def estimar_densidad_ingrediente(ingrediente):
    """Estima la densidad del ingrediente."""
    ingrediente = ingrediente.lower()
    data = ingredients_data.get(ingrediente, {})
    return data.get('density', 1 / (1 + data.get('fiber', 0) * 0.1)) if 'density' in data else 0.5

def estimar_elasticidad_ingrediente(ingrediente):
    """Estima la elasticidad del ingrediente."""
    ingrediente = ingrediente.lower()
    data = ingredients_data.get(ingrediente, {})
    if 'elasticity' in data:
        return data['elasticity']
    carbs = data.get('carbs', 0)
    protein = data.get('protein', 0)
    fat = data.get('fat', 0)
    return min(1.0, (carbs * 0.01) + (protein * 0.02) + (fat * 0.005))

def calcular_sodio(receta):
    """Calcula sodio total en mg/100g."""
    sodio_total = 0.0
    for ingrediente, proporcion in receta.items():
        sodio_ing = ingredients_data.get(ingrediente, {}).get('sodium', 0)
        sodio_total += sodio_ing * proporcion
    return sodio_total

def calcular_proteinas(receta):
    """Calcula proteínas en %."""
    proteinas_total = 0.0
    for ingrediente, proporcion in receta.items():
        proteinas_ing = ingredients_data.get(ingrediente, {}).get('protein', 0)
        proteinas_total += proteinas_ing * proporcion
    return proteinas_total

def check_ingredient_constraints(receta, masa_name):
    """Verifica restricciones de proporciones."""
    if masa_name == 'G12':
        if not (0.2 <= receta.get('chickpea_flour', 0) <= 0.4):
            return False
    elif masa_name == 'C12':
        if masa_name == 'G12' and not (0.2 <= receta.get('chickpea_flour', 0) <= 0.4):
            return False
    if not (0.4 <= receta.get('water', 0) <= 0.6):
        return False
    if receta.get(CORN_STARCH, 0) < 0.05:
        return False
    if receta.get(XANTHAN_GUM, 0) < 0.005:
        return False
    return True

def calcular_contribuciones(receta):
    """Calcula densidad y elasticidad total."""
    densidad_total = 0.0
    elasticidad_total = 0.0
    for ingrediente, proporcion in receta.items():
        d_i = estimar_densidad_ingrediente(ingrediente)
        e_i = estimar_elasticidad_ingrediente(ingrediente)
        densidad_total += d_i * proporcion
        elasticidad_total += e_i * proporcion
    return densidad_total, elasticidad_total

def evaluate_individual(individual, masa_name, all_ingredients):
    """Evalúa un individuo para DEAP."""
    receta = dict(zip(all_ingredients, individual))
    if not check_ingredient_constraints(receta, masa_name):
        return (float('inf'), -float('inf'))  # Penalización máxima

    densidad, elasticidad = calcular_contribuciones(receta)

    # Penalizar exceso de sodio
    sodio = calcular_sodio(receta)
    if sodio > 400:
        densidad += 1000  # Penalización alta

    # Penalizar falta de proteínas
    proteinas = calcular_proteinas(receta)
    if proteinas < 6:
        elasticidad -= 1000  # Penalización alta

    # Bonus por vinagre
    if receta.get('vinegar', 0) > 0:
        elasticidad += 0.05

    return (densidad, elasticidad)

def repair_individual(individual, masa_name, all_ingredients):
    """Ajusta proporciones para cumplir restricciones y normaliza."""
    individual = [max(0, prop) for prop in individual]

    for i, ing in enumerate(all_ingredients):
        if ing == BASE_INGREDIENTS[masa_name]:
            if masa_name == 'G12':
                individual[i] = min(0.4, max(0.2, individual[i]))
            elif masa_name == 'C12':
                individual[i] = min(0.5, max(0.3, individual[i]))
        elif ing == 'water':
            individual[i] = min(0.6, max(0.4, individual[i]))
        elif ing == CORN_STARCH:
            individual[i] = max(0.05, individual[i])
        elif ing == XANTHAN_GUM:
            individual[i] = max(0.005, individual[i])
        elif ing == 'vinegar':
            individual[i] = max(0.01, individual[i])

    total = sum(individual)
    if total > 0:
        individual = [prop / total for prop in individual]
    else:
        individual = [0.02 if ing in ['vinegar', 'olive_oil'] else 0.1 for ing in all_ingredients]
        total = sum(individual)
        individual = [prop / total for prop in individual]

    return individual

def crear_receta_inicial(masa_name, all_ingredients):
    """Genera receta inicial aleatoria normalizada."""
    proporciones = []
    for ingredient in all_ingredients:
        if ingredient == BASE_INGREDIENTS[masa_name]:
            if masa_name == 'G12':
                prop = random.uniform(0.2, 0.4)
            elif masa_name == 'C12':
                prop = random.uniform(0.3, 0.5)
        elif ingredient == 'water':
            prop = random.uniform(0.4, 0.6)
        elif ingredient == CORN_STARCH:
            prop = random.uniform(0.05, 0.15)
        elif ingredient == XANTHAN_GUM:
            prop = random.uniform(0.005, 0.02)
        elif ingredient == 'vinegar':
            prop = random.uniform(0.01, 0.02)
        else:
            prop = random.uniform(0.02, 0.1)
        proporciones.append(prop)
    total = sum(proporciones)
    return [p / total for p in proporciones]

def suggest_substitutes(ingredient):
    """Sugiere sustituto basado en densidad y elasticidad."""
    if ingredient not in SUBSTITUTES:
        return ingredient
    original_density = estimar_densidad_ingrediente(ingredient)
    original_elasticity = estimar_elasticidad_ingrediente(ingredient)
    subs = SUBSTITUTES[ingredient]
    best_sub = subs[0]
    min_diff = float('inf')
    for sub in subs:
        sub_density = estimar_densidad_ingrediente(sub)
        sub_elasticity = estimar_elasticidad_ingrediente(sub)
        diff = abs(original_density - sub_density) + abs(original_elasticity - sub_elasticity)
        if diff < min_diff:
            min_diff = diff
            best_sub = sub
    return best_sub

# ----------------------------------------------------------------------
# 4. Función principal de optimización
# ----------------------------------------------------------------------
def optimize_genetic(masa_name, pop_size=50, ngen=30):
    """Optimización genética multiobjetivo para la masa especificada."""
    print(f"\n[INFO] Optimizando masa '{masa_name}' con pop_size={pop_size}, ngen={ngen}...")
    all_ingredients = get_ingredients_for_masa(masa_name)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual,
                     partial(crear_receta_inicial, masa_name, all_ingredients))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", partial(evaluate_individual, masa_name=masa_name, all_ingredients=all_ingredients))
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.05, indpb=0.3)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("repair", partial(repair_individual, masa_name=masa_name, all_ingredients=all_ingredients))

    pop = toolbox.population(n=pop_size)
    hof = tools.ParetoFront()

    algorithms.eaMuPlusLambda(pop, toolbox, mu=pop_size, lambda_=pop_size, cxpb=0.7, mutpb=0.3, ngen=ngen,
                              stats=None, halloffame=hof, verbose=True)

    best_ind = hof[0]
    best_recipe = dict(zip(all_ingredients, best_ind))
    print("[INFO] Mejor receta encontrada:", best_recipe)

    for ing in best_recipe.keys():
        maybe_sub = suggest_substitutes(ing)
        if maybe_sub != ing:
            print(f"   - Sugerencia: sustituir '{ing}' por '{maybe_sub}'")

    fronts = tools.sortNondominated(pop, len(pop), first_front_only=False)
    for front in fronts:
        densities = [ind.fitness.values[0] for ind in front]
        elasticities = [ind.fitness.values[1] for ind in front]  # Elasticidad ya no se niega aquí
        plt.scatter(densities, elasticities, label=f'Front {fronts.index(front) + 1}')
    plt.xlabel('Densidad')
    plt.ylabel('Elasticidad')
    plt.title(f'Fronteras de Pareto para {masa_name}')
    plt.legend()
    plt.show()

    return best_recipe

# ----------------------------------------------------------------------
# 5. Ejemplo de uso
# ----------------------------------------------------------------------
if __name__ == "__main__":
    best_g12 = optimize_genetic('G12', pop_size=50, ngen=30)
    print("\nResultados finales:")
    print("Masa G12 ->", best_g12)