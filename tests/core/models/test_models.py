import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.models import Base, Ingredient, Recipe, RecipeIngredient

class TestModels(unittest.TestCase):
    def setUp(self):
        # Crear motor de base de datos en memoria
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def tearDown(self):
        self.session.close()
    
    def test_create_ingredient(self):
        """Prueba la creación de un ingrediente."""
        ingredient = Ingredient(
            name="Tomato",
            description="Fresh tomato",
            usda_fdc_id=12345,
            category="Vegetable",
            unit="g",
            calories_per_unit=0.18,
            protein_per_unit=0.009,
            carbs_per_unit=0.039,
            fat_per_unit=0.002
        )
        self.session.add(ingredient)
        self.session.commit()
        
        saved_ingredient = self.session.query(Ingredient).first()
        self.assertEqual(saved_ingredient.name, "Tomato")
        self.assertEqual(saved_ingredient.category, "Vegetable")
    
    def test_create_recipe(self):
        """Prueba la creación de una receta."""
        recipe = Recipe(
            name="Margherita Pizza",
            description="Classic Italian pizza",
            instructions="Mix ingredients and bake",
            prep_time=20,
            cook_time=15,
            servings=4,
            difficulty="medium",
            category="Italian",
            tags=["pizza", "italian", "vegetarian"]
        )
        self.session.add(recipe)
        self.session.commit()
        
        saved_recipe = self.session.query(Recipe).first()
        self.assertEqual(saved_recipe.name, "Margherita Pizza")
        self.assertEqual(saved_recipe.difficulty, "medium")
    
    def test_recipe_ingredient_relationship(self):
        """Prueba la relación entre recetas e ingredientes."""
        # Crear ingrediente
        ingredient = Ingredient(
            name="Tomato",
            description="Fresh tomato",
            category="Vegetable",
            unit="g"
        )
        self.session.add(ingredient)
        
        # Crear receta
        recipe = Recipe(
            name="Margherita Pizza",
            description="Classic Italian pizza",
            instructions="Mix ingredients and bake"
        )
        self.session.add(recipe)
        self.session.commit()
        
        # Crear relación
        recipe_ingredient = RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            quantity=200,
            unit="g"
        )
        self.session.add(recipe_ingredient)
        self.session.commit()
        
        # Verificar relación
        saved_recipe = self.session.query(Recipe).first()
        self.assertEqual(len(saved_recipe.recipe_ingredients), 1)
        self.assertEqual(saved_recipe.recipe_ingredients[0].quantity, 200)
        self.assertEqual(saved_recipe.recipe_ingredients[0].ingredient.name, "Tomato")

if __name__ == "__main__":
    unittest.main()
