from sqlalchemy import Column, String, Integer, Float, JSON
from sqlalchemy.orm import relationship
from .base import Base, BaseModelMixin

class Ingredient(Base, BaseModelMixin):
    """Modelo para ingredientes."""
    __tablename__ = "ingredients"

    name = Column(String(100), nullable=False)
    description = Column(String(500))
    usda_fdc_id = Column(Integer, unique=True)
    nutrients = Column(JSON)  # Almacena los datos nutricionales de USDA
    category = Column(String(50))
    unit = Column(String(20))
    calories_per_unit = Column(Float)
    protein_per_unit = Column(Float)
    carbs_per_unit = Column(Float)
    fat_per_unit = Column(Float)
    
    # Relación con recetas
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredient")
