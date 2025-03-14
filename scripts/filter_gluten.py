import pandas as pd

# Cargar el archivo de ingredientes
df = pd.read_csv('data/ingredients_data.csv')

# Lista de palabras clave que indican gluten
gluten_keywords = ['wheat', 'barley', 'rye']

# Filtrar ingredientes que no contienen gluten
df_filtered = df[~df['ingredient'].str.contains('|'.join(gluten_keywords), case=False)]

# Guardar el archivo filtrado
df_filtered.to_csv('data/ingredients_data_gluten_free.csv', index=False)
print("Archivo 'data/ingredients_data_gluten_free.csv' generado con éxito.")