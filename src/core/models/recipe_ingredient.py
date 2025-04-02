from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class RecipeIngredient(Base):
    """Modelo para la relación entre recetas e ingredientes."""
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    created_at = Column(String, default="2025-04-02 18:10:17.102775")
    updated_at = Column(String, default="2025-04-02 18:10:17.102776")

    # Relaciones
    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", back_populates="recipe_ingredients")
