import random
import pandas as pd
from deap import base, creator, tools, algorithms
from functools import partial

# Inicializar el generador de números aleatorios
rng = random.Random()

# ----------------------------------------------------------------------
# 1. Cargar datos y preparar diccionarios
# ----------------------------------------------------------------------
try:
    print("Intentando cargar el archivo CSV 'ingredients_data_gluten_free.csv'...")
    df = pd.read_csv('data/ingredients_data_gluten_free.csv', encoding='utf-8', delimiter=',')
    print("Archivo CSV cargado. Contenido del DataFrame:")
    print(df)
    df['ingredient'] = df['ingredient'].str.strip().str.lower()
    ingredients_data = df.set_index('ingredient').to_dict('index')
    print("Contenido de ingredients_data después de indexar:")
    print({k: v for k, v in ingredients_data.items()})
except Exception as e:
    print(f"Error al cargar el archivo CSV: {e}")
    raise

print("Ingredientes cargados:", list(ingredients_data.keys()))

# Diccionarios y listas de referencia
BASE_INGREDIENTS = {
    'C12': 'cauliflower',
    'G12': 'chickpea_flour'
}

ADJUSTABLE_INGREDIENTS = [
    'rice flour',
    'potato flour',
    'corn starch',
    'olive oil',
    'xanthan gum',
    'sugar',
    'salt'
]

SUBSTITUTES = {
    'chickpea_flour': ['almond flour', 'coconut flour'],
    'rice flour': ['potato flour', 'corn starch']
}

# ----------------------------------------------------------------------
# 2. Configurar DEAP
# ----------------------------------------------------------------------
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# ----------------------------------------------------------------------
# 3. Funciones auxiliares
# ----------------------------------------------------------------------
def get_ingredients_for_masa(masa_name):
    """Devuelve la lista de ingredientes base + ajustables según la masa (C12 o G12)."""
    base_ing = ['water', BASE_INGREDIENTS[masa_name]]
    return base_ing + ADJUSTABLE_INGREDIENTS

def estimar_densidad_ingrediente(ingrediente):
    """Estima la densidad si no está en los datos."""
    ingrediente = ingrediente.lower()
    data = ingredients_data.get(ingrediente, {})
    return 1 / (1 + data.get('fiber', 0) * 0.1) if 'fiber' in data else 0.5

def estimar_elasticidad(ingrediente):
    """Estima la elasticidad basada en carbohidratos y grasas."""
    data = ingredients_data.get(ingrediente, {})
    carbs = data.get('carbs', 0)
    fat = data.get('fat', 0)
    return min(1.0, (carbs * 0.01) + (fat * 0.02))

def check_ingredient_constraints(receta, masa_name):
    """Verifica restricciones mínimas."""
    if masa_name == 'C12' and receta.get('cauliflower', 0) <= 0:
        return False
    if masa_name == 'G12' and receta.get('chickpea_flour', 0) <= 0:
        return False
    if receta.get('water', 0) <= 0:
        return False
    return True

def calcular_contribuciones(receta):
    """Suma densidad y elasticidad total de la receta."""
    densidad_total = 0.0
    elasticidad_total = 0.0
    for ingrediente, proporcion in receta.items():
        d_contrib, e_contrib = obtener_metricas_ingrediente(ingrediente, proporcion)
        densidad_total += d_contrib
        elasticidad_total += e_contrib
    return densidad_total, elasticidad_total

def obtener_metricas_ingrediente(ingrediente, proporcion):
    """Devuelve métricas (densidad * proporción, elasticidad * proporción)."""
    ing_lower = ingrediente.lower()
    if ing_lower not in ingredients_data:
        return 0.5 * proporcion, 0.1 * proporcion
    d_i = ingredients_data[ing_lower].get('density', estimar_densidad_ingrediente(ing_lower))
    e_i = estimar_elasticidad(ing_lower)
    return d_i * proporcion, e_i * proporcion

def calcular_penalizacion_proporciones(receta):
    """Penaliza proporciones bajas (< 2%)."""
    penalty = 0.0
    for ingrediente, prop in receta.items():
        if ingrediente in ADJUSTABLE_INGREDIENTS and prop < 0.02:
            penalty += 0.2
    return penalty

def calcular_penalizacion_elasticidad(elasticidad_total):
    """Penaliza elasticidad baja (< 0.3)."""
    return max(0, (0.3 - elasticidad_total) * 10)

def calcular_densidad(individual, masa_name, all_ingredients):
    """Función de evaluación DEAP."""
    receta = dict(zip(all_ingredients, individual))
    if not check_ingredient_constraints(receta, masa_name):
        return (float('inf'),)
    densidad_total, elasticidad_total = calcular_contribuciones(receta)
    zero_penalty = calcular_penalizacion_proporciones(receta)
    elasticity_penalty = calcular_penalizacion_elasticidad(elasticidad_total)
    score = densidad_total + zero_penalty + elasticity_penalty
    return (score,)

def repair_individual(individual, masa_name, all_ingredients):
    """Ajusta proporciones para cumplir restricciones y normaliza."""
    fixed_indices = [i for i, ing in enumerate(all_ingredients) if ing in ['cauliflower', 'chickpea_flour', 'water']]
    adjustable_indices = [i for i, ing in enumerate(all_ingredients) if ing in ADJUSTABLE_INGREDIENTS]

    # Ajustar ingredientes fijos
    for i in fixed_indices:
        ingredient = all_ingredients[i]
        if ingredient == 'cauliflower' and masa_name == 'G12':
            individual[i] = 0.0
        elif ingredient == 'chickpea_flour' and masa_name == 'C12':
            individual[i] = 0.0
        else:
            if ingredient == 'chickpea_flour' and masa_name == 'G12':
                individual[i] = min(0.4, max(0.1, individual[i]))
            elif ingredient == 'water':
                individual[i] = max(0.4, individual[i])
            else:
                individual[i] = max(0.1, individual[i])

    # Ajustar ingredientes ajustables
    for i in adjustable_indices:
        individual[i] = max(0.02, individual[i])

    # Normalizar a sum=1
    total = sum(individual)
    if total > 0:
        individual[:] = [prop / total for prop in individual]
    else:
        n = len(individual)
        individual[:] = [1.0 / n] * n
    return individual

def crear_receta_inicial(masa_name, all_ingredients):
    """Genera una receta inicial aleatoria normalizada."""
    proporciones = []
    for ingredient in all_ingredients:
        if ingredient == 'cauliflower':
            prop = random.uniform(0.2, 0.4) if masa_name == 'C12' else 0.0
        elif ingredient == 'chickpea_flour':
            prop = random.uniform(0.2, 0.4) if masa_name == 'G12' else 0.0
        elif ingredient == 'water':
            prop = random.uniform(0.4, 0.6)
        else:
            prop = random.uniform(0.05, 0.15)
        proporciones.append(prop)
    total = sum(proporciones)
    if total > 0:
        return [p / total for p in proporciones]
    return [1.0 / len(proporciones)] * len(proporciones)

def suggest_substitutes(ingredient):
    """Sugerencia de sustitutos."""
    if ingredient in SUBSTITUTES:
        return SUBSTITUTES[ingredient][0]
    return ingredient

# ----------------------------------------------------------------------
# 4. Función principal de optimización
# ----------------------------------------------------------------------
def optimize_genetic(masa_name, pop_size=50, ngen=30):
    """Realiza la optimización genética."""
    print(f"\n[INFO] Optimizando masa '{masa_name}' con pop_size={pop_size}, ngen={ngen}...")
    all_ingredients = get_ingredients_for_masa(masa_name)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual,
                     partial(crear_receta_inicial, masa_name, all_ingredients))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", partial(calcular_densidad, masa_name=masa_name, all_ingredients=all_ingredients))
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.05, indpb=0.3)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("repair", partial(repair_individual, masa_name=masa_name, all_ingredients=all_ingredients))

    pop = toolbox.population(n=pop_size)

    for _ in range(ngen):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.7, mutpb=0.3)
        for ind in offspring:
            ind = toolbox.repair(ind)
            ind.fitness.values = toolbox.evaluate(ind)
        pop = toolbox.select(offspring, k=len(pop))

    best_ind = tools.selBest(pop, 1)[0]
    best_recipe = dict(zip(all_ingredients, best_ind))
    print("[INFO] Mejor receta:", best_recipe)

    for ing in best_recipe.keys():
        maybe_sub = suggest_substitutes(ing)
        if maybe_sub != ing:
            print(f"   - Sugerencia: sustituir '{ing}' por '{maybe_sub}'")

    return best_recipe

# ----------------------------------------------------------------------
# 5. Ejemplo de uso
# ----------------------------------------------------------------------
if __name__ == "__main__":
    best_c12 = optimize_genetic('C12', pop_size=20, ngen=15)
    best_g12 = optimize_genetic('G12', pop_size=20, ngen=15)
    print("\nResultados finales:")
    print("Masa C12 ->", best_c12)
    print("Masa G12 ->", best_g12)