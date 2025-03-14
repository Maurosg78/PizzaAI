import random
import pandas as pd
from deap import base, creator, tools, algorithms
from functools import partial

# Cargar datos de ingredientes sin gluten
df = pd.read_csv('data/ingredients_data_gluten_free.csv')
ingredients_data = df.set_index('ingredient').to_dict('index')

# Lista de ingredientes ajustables
adjustable_ingredients = ['rice flour', 'potato flour', 'corn starch', 'olive oil', 'xanthan gum', 'sugar', 'salt']

# Función para estimar la densidad si falta
def estimar_densidad_ingrediente(ingrediente):
    """Estima la densidad teórica de un ingrediente usando su contenido de fibra."""
    if 'fiber' in ingredients_data[ingrediente]:
        fiber = ingredients_data[ingrediente]['fiber']
        return 1 / (1 + fiber * 0.1)  # Fórmula teórica: densidad disminuye con más fibra
    else:
        return 0.5  # Valor por defecto si no hay datos

# Función para calcular la densidad total de una receta
def calcular_densidad(receta):
    """Calcula la densidad total como suma ponderada de densidades individuales."""
    densidad_total = 0
    for ingrediente, proporcion in receta.items():
        if ingrediente in ingredients_data:
            d_i = ingredients_data[ingrediente].get('density', estimar_densidad_ingrediente(ingrediente))
            densidad_total += d_i * proporcion
        else:
            print(f"Advertencia: {ingrediente} no está en ingredients_data. Usando densidad por defecto.")
            densidad_total += 0.5 * proporcion  # Valor por defecto
    return (densidad_total,)  # Tupla para compatibilidad con DEAP

# Función para crear una receta inicial
def crear_receta(masa_name):
    """Crea una receta inicial con proporciones aleatorias dentro de rangos definidos."""
    receta = {}
    if masa_name == 'C12':
        receta['cauliflower'] = random.uniform(0.2, 0.4)  # Ingrediente fijo para C12
    elif masa_name == 'G12':
        receta['chickpea'] = random.uniform(0.2, 0.4)  # Ingrediente fijo para G12
    
    for ing in adjustable_ingredients:
        receta[ing] = random.uniform(0.05, 0.15)
    
    # Normalizar para que la suma sea 1.0
    total = sum(receta.values())
    for ing in receta:
        receta[ing] /= total
    return receta

# Función para ejecutar la optimización genética
def optimize_genetic(masa_name):
    """Ejecuta el algoritmo genético para optimizar la densidad de la masa."""
    print(f"Optimizando {masa_name} con algoritmo genético...")
    
    # Configurar el algoritmo genético
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar la densidad
    creator.create("Individual", dict, fitness=creator.FitnessMin)
    
    toolbox = base.Toolbox()
    # Registrar la función crear_receta con el parámetro masa_name
    toolbox.register("individual", tools.initIterate, creator.Individual, partial(crear_receta, masa_name))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", calcular_densidad)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    # Ejecutar el algoritmo genético
    pop = toolbox.population(n=50)  # Población inicial de 50 individuos
    for _ in range(20):  # 20 generaciones
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        pop = toolbox.select(offspring, k=len(pop))
    
    # Seleccionar y mostrar la mejor receta
    best_genetic = tools.selBest(pop, 1)[0]
    print(f"Mejor receta genética para {masa_name}:", best_genetic)
    return best_genetic