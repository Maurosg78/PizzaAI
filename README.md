# PizzaAI

Sistema de recomendación y optimización de recetas de pizza basado en IA.

## Estructura del Proyecto

```
pizzaai/
├── src/                    # Código fuente principal
│   ├── api/               # API REST
│   ├── core/              # Componentes centrales
│   │   ├── models/        # Modelos de datos
│   │   ├── services/      # Servicios principales
│   │   └── cache/         # Sistema de caché
│   └── features/          # Características específicas
│       ├── nutrition/     # Análisis nutricional
│       ├── production/    # Gestión de producción
│       └── recommendations/ # Motor de recomendaciones
├── tests/                 # Pruebas unitarias y de integración
├── scripts/               # Scripts de utilidad
├── docs/                  # Documentación
├── app/                   # Aplicación web
└── config/                # Configuraciones
```

## Scripts Principales

- `genetic_optimizer.py`: Optimización de recetas usando algoritmos genéticos
- `create_issues.py`: Gestión automatizada de issues en GitHub
- `build_database.py`: Construcción de la base de datos
- `data_collection.py`: Recolección de datos de ingredientes
- `generate_ingredients.py`: Generación de ingredientes
- `add_physical_properties.py`: Adición de propiedades físicas

## Configuración

La configuración del proyecto se centraliza en `pyproject.toml`, que incluye:
- Configuración de formateo (black)
- Configuración de importaciones (isort)
- Configuración de pruebas (pytest)
- Configuración de linting (flake8)
- Configuración de tipado (mypy)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`

## Uso

1. Configurar variables de entorno en `.env`
2. Ejecutar el servidor: `python src/api/main.py`
3. Acceder a la API en `http://localhost:8000`

## Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas con cobertura
pytest --cov=src tests/
```

## Contribución

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías de contribución.

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles. 