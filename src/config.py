"""
ConsumeSafe Application Configuration
"""

import os
from typing import Optional


class Settings:
    """Application settings"""
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Data paths
    BOYCOTT_DATA_PATH: str = os.getenv(
        "BOYCOTT_DATA_PATH",
        "data/boycott_list.json"
    )
    PRODUCTS_DATA_PATH: str = os.getenv(
        "PRODUCTS_DATA_PATH",
        "data/tunisian_products.json"
    )
    
    # API
    API_TITLE: str = "ConsumeSafe API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Boycott checker and Tunisian product alternatives"
    
    # Security
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_CALLS: int = int(os.getenv("RATE_LIMIT_CALLS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Timeouts
    REQUEST_TIMEOUT: int = 30
    DATABASE_TIMEOUT: int = 10


settings = Settings()
