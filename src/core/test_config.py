from src.core.config import settings


def test_settings():
    """Prueba básica de la configuración"""
    assert settings.APP_NAME == "PizzaAI"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DATABASE_URL == "sqlite:///./pizzaai.db"
    assert settings.API_PORT == 8000
    assert settings.CACHE_TTL == 3600
    assert settings.MAX_UPLOAD_SIZE == 5 * 1024 * 1024  # 5MB
