from typing import Dict, List, Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "PizzaAI"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Configuración de seguridad
    SECRET_KEY: SecretStr = Field(default="tu_clave_secreta_aqui")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de la base de datos
    DATABASE_URL: str = Field(default="sqlite:///./pizzaai.db")
    
    # Configuración de CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(default=["*"])
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    
    # Configuración de la API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Configuración de caché
    CACHE_TTL: int = 3600  # 1 hora
    
    # Configuración de límites de API
    API_RATE_LIMIT: int = 100  # peticiones por minuto
    
    # Configuración de archivos
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # Configuración de email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[SecretStr] = None
    
    # Configuración de monitoreo
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Configuración de APIs externas
    USDA_API_KEY: SecretStr = Field(default="Rntzc9HDaefGgZL0w3Sid120qfk4kdJD4YZuicE4")
    USDA_API_BASE_URL: str = "https://api.nal.usda.gov/fdc/v1"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_default=True
    )

    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str) -> Optional[Union[str, int, bool, SecretStr]]:
        """Parsea variables de entorno personalizadas"""
        if raw_val.lower() in ('null', '', 'none'):
            return None
        return raw_val

# Crear una instancia global de la configuración
settings = Settings() 