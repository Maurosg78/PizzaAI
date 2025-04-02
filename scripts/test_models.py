from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.models import Base, Ingredient, Recipe, RecipeIngredient


def test_models():
    # Crear motor de base de datos en memoria
    engine = create_engine("sqlite:///:memory:")

    # Crear tablas
    Base.metadata.create_all(engine)

    # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Probar modelo de ingrediente
    ingredient = Ingredient(
        name="Tomato",
        description="Fresh tomato",
        usda_fdc_id=12345,
        category="Vegetable",
        unit="g",
        calories_per_unit=0.18,
        protein_per_unit=0.009,
        carbs_per_unit=0.039,
        fat_per_unit=0.002,
    )

    session.add(ingredient)
    session.commit()

    # Probar modelo de receta
    recipe = Recipe(
        name="Margherita Pizza",
        description="Classic Italian pizza",
        instructions="Mix ingredients and bake",
        prep_time=20,
        cook_time=15,
        servings=4,
        difficulty="medium",
        category="Italian",
        tags=["pizza", "italian", "vegetarian"],
    )

    # Crear la relación entre receta e ingrediente
    recipe_ingredient = RecipeIngredient(
        recipe=recipe, ingredient=ingredient, quantity=200, unit="g"
    )

    session.add(recipe)
    session.add(recipe_ingredient)
    session.commit()

    # Verificar que los datos se guardaron correctamente
    saved_ingredient = session.query(Ingredient).first()
    saved_recipe = session.query(Recipe).first()
    saved_recipe_ingredient = session.query(RecipeIngredient).first()

    print(f"Ingrediente guardado: {saved_ingredient.name}")
    print(f"Receta guardada: {saved_recipe.name}")
    print(
        f"Relación guardada: {saved_recipe_ingredient.quantity} {saved_recipe_ingredient.unit} de {saved_recipe_ingredient.ingredient.name}"
    )


if __name__ == "__main__":
    test_models()
