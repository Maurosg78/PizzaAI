import pandas as pd

# Simulación de datos: proporciones y elasticidad
data = {
    "cauliflower_ratio": [0.8, 0.6, 0.4, 0.2],
    "chickpea_ratio": [0.2, 0.4, 0.6, 0.8],
    "elasticity": [0.5, 0.6, 0.7, 0.8],  # Valores ficticios
}
df = pd.DataFrame(data)
df.to_csv("../data/experimental_data.csv", index=False)
