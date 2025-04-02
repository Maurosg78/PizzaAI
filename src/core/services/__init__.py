"""
Servicios de PizzaAI
"""

from .simple_recommender import SimpleRecommender
from .usda_service import USDAService
from ..config import get_settings

settings = get_settings()
usda_service = USDAService(api_key=settings.USDA_API_KEY)

__all__ = ["usda_service", "USDAService", "SimpleRecommender"]
