"""
Módulo core de PizzaAI
"""

from .config import get_settings

settings = get_settings()

__all__ = ["settings"]
