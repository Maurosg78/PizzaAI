"""
pipeline.py

Ejemplo de pipeline simplificado que integra el uso del genetic_optimizer
y demuestra el flujo de varias fases de producción.
Ajusta nombres y rutas según tu proyecto real.
"""

import datetime
import os

# Importa tu optimizador genético (ajusta la ruta si es distinto)
from scripts.genetic_optimizer import optimize_genetic

def fase_mezclado(masa_name="C12", pop_size=30, ngen=20):
    print(f"\n[FASE MEZCLADO] - Optimizar {masa_name}")
    best_recipe = optimize_genetic(masa_name, pop_size=pop_size, ngen=ngen)
    return best_recipe

def run_pipeline():
    # Ejemplo: fase 1 (pretratamiento) con datos ficticios
    print("[FASE 1] - Pretratamiento: Revisando humedad del vegetal ...")
    # ... haz algo ficticio ...
    
    # Fase 2: Mezclado con GA
    best_c12 = fase_mezclado("C12", pop_size=30, ngen=15)
    best_g12 = fase_mezclado("G12", pop_size=30, ngen=15)
    
    # Fase 3: Cocción, etc. (solo impresión de ejemplo)
    print("\n[FASE 3] - Cocción: Ajustando tiempos y temperaturas ...")
    # ... lo que necesites ...
    
    # Al final, generamos un mini-reporte
    now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pipeline_resultado_{now_str}.txt"
    
    # Supongamos que queremos guardarlo en la raíz de resultados_main
    resultados_path = os.path.join("..", "resultados_main", filename)
    
    with open(resultados_path, "w") as f:
        f.write("[REPORTE PIPELINE]\n")
        f.write(f"Fecha/Hora: {now_str}\n")
        f.write(f"Mejor C12: {best_c12}\n")
        f.write(f"Mejor G12: {best_g12}\n")
    
    print(f"\nReporte final guardado en: {resultados_path}")

if __name__ == "__main__":
    run_pipeline()
