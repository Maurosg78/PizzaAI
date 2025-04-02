from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, BaseModelMixin


class Recipe(Base, BaseModelMixin):
    """Modelo para recetas."""

    __tablename__ = "recipes"

    name = Column(String(100), nullable=False)
    description = Column(String(500))
    instructions = Column(String(2000))
    prep_time = Column(Integer)  # en minutos
    cook_time = Column(Integer)  # en minutos
    servings = Column(Integer)
    difficulty = Column(String(20))  # fácil, medio, difícil
    category = Column(String(50))
    tags = Column(JSON)  # lista de etiquetas
    image_url = Column(String(200))

    # Relación con ingredientes
    recipe_ingredients = relationship("RecipeIngredient", back_populates="recipe")
