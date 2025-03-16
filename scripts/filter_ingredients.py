import pandas as pd

# Cargar la base de datos
df = pd.read_csv('ingredients_data_doughs.csv')

# Función para filtrar ingredientes
def filter_ingredients(gluten_free=False, allergen_free=False):
    filtered_df = df
    if gluten_free:
        filtered_df = filtered_df[filtered_df['contains_gluten'] == 'No']
    if allergen_free:
        filtered_df = filtered_df[filtered_df['contains_allergens'] == 'No']
    return filtered_df

# Ejemplo: Filtrar para una receta sin gluten ni alérgenos
filtered = filter_ingredients(gluten_free=True, allergen_free=True)
print("Ingredientes sin gluten ni alérgenos:")
print(filtered['ingredient'].tolist())