import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.models import Base, Ingredient, Recipe, RecipeIngredient
from src.core.services.simple_recommender import SimpleRecommender

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def check_usda_api():
    """Verifica la conexión con la API de USDA."""
    try:
        logger.info("Verificando conexión con USDA API...")
        api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
        recommender = SimpleRecommender(api_key)

        # Probar búsqueda básica
        foods = recommender.search_foods("tomato")
        if not foods:
            logger.error("❌ Error crítico: No se pueden obtener datos de USDA API")
            return False

        logger.info("✅ Conexión con USDA API funcionando correctamente")
        return True

    except Exception as e:
        logger.error(f"❌ Error crítico en USDA API: {str(e)}")
        return False


def check_database():
    """Verifica la conexión y estructura de la base de datos."""
    try:
        logger.info("Verificando base de datos...")
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)

        # Probar operaciones básicas
        Session = sessionmaker(bind=engine)
        session = Session()

        # Probar modelo de ingrediente
        ingredient = Ingredient(
            name="Test Ingredient", description="Test", category="Test", unit="g"
        )
        session.add(ingredient)
        session.commit()

        # Probar modelo de receta
        recipe = Recipe(name="Test Recipe", description="Test", instructions="Test")
        session.add(recipe)
        session.commit()

        # Probar relación
        recipe_ingredient = RecipeIngredient(
            recipe=recipe, ingredient=ingredient, quantity=100, unit="g"
        )
        session.add(recipe_ingredient)
        session.commit()

        logger.info("✅ Base de datos funcionando correctamente")
        return True

    except Exception as e:
        logger.error(f"❌ Error crítico en base de datos: {str(e)}")
        return False


def check_recommendations():
    """Verifica el sistema de recomendaciones."""
    try:
        logger.info("Verificando sistema de recomendaciones...")
        api_key = "Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4"
        recommender = SimpleRecommender(api_key)

        # Probar recomendaciones
        recommendations = recommender.get_recommendations("tomato")
        if not recommendations:
            logger.error("❌ Error crítico: No se pueden generar recomendaciones")
            return False

        logger.info("✅ Sistema de recomendaciones funcionando correctamente")
        return True

    except Exception as e:
        logger.error(f"❌ Error crítico en sistema de recomendaciones: {str(e)}")
        return False


def main():
    """Función principal de verificación."""
    logger.info("Iniciando verificación de errores críticos...")

    # Lista de verificaciones
    checks = [
        ("USDA API", check_usda_api),
        ("Base de datos", check_database),
        ("Sistema de recomendaciones", check_recommendations),
    ]

    # Ejecutar verificaciones
    all_checks_passed = True
    for name, check_func in checks:
        logger.info(f"\nVerificando {name}...")
        if not check_func():
            all_checks_passed = False
            logger.error(f"❌ {name} falló la verificación")

    # Resumen final
    if all_checks_passed:
        logger.info("\n✅ Todas las verificaciones pasaron correctamente")
        sys.exit(0)
    else:
        logger.error("\n❌ Se encontraron errores críticos")
        sys.exit(1)


if __name__ == "__main__":
    main()
