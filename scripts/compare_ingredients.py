import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import euclidean

# Cargar datos sin gluten
df = pd.read_csv('data/ingredients_data_gluten_free.csv')

# Normalizar valores nutricionales
nutrients = ['calories', 'protein', 'carbs', 'fat', 'fiber']
scaler = MinMaxScaler()
df[nutrients] = scaler.fit_transform(df[nutrients])

# Función para encontrar ingredientes similares
def find_similar_ingredients(target_ingredient, df, top_n=3):
    target = df[df['ingredient'] == target_ingredient][nutrients].values[0]
    similarities = []
    for _, row in df.iterrows():
        if row['ingredient'] != target_ingredient:
            distance = euclidean(target, row[nutrients])
            similarities.append((row['ingredient'], distance))
    similarities.sort(key=lambda x: x[1])
    return similarities[:top_n]

# Ejemplo: Buscar reemplazos para 'rice flour'
similar_to_rice_flour = find_similar_ingredients('rice flour', df)
print(f"Reemplazos para 'rice flour': {similar_to_rice_flour}")