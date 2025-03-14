import pandas as pd

# Definir la ruta al archivo CSV (en la misma carpeta)
csv_path = "../data/ingredients_data_gluten_free.csv"
# Cargar el CSV en un DataFrame
df = pd.read_csv(csv_path)

# Convertir la columna 'ingredient' a minúsculas
df['ingredient'] = df['ingredient'].str.lower()

# Guardar el DataFrame actualizado en el CSV
df.to_csv(csv_path, index=False)
print("Nombres de ingredientes convertidos a minúsculas y guardados en", csv_path)