# from pydantic_settings import BaseSettings
# from pydantic import AnyHttpUrl, validator
# from typing import List, Optional, Union
# import secrets


# class Settings(BaseSettings):
#     # App
#     APP_NAME: str = "E-Commerce API"
#     APP_VERSION: str = "1.0.0"
#     DEBUG: bool = False
#     ENVIRONMENT: str = "production"

#     # Security
#     SECRET_KEY: str = secrets.token_urlsafe(32)
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#     REFRESH_TOKEN_EXPIRE_DAYS: int = 7

#     # Database
#     DATABASE_URL: str
#     DATABASE_URL_SYNC: str

#     # Redis
#     REDIS_URL: str = "redis://localhost:6379/0"
#     CELERY_BROKER_URL: str = "redis://localhost:6379/1"
#     CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

#     # Email
#     SMTP_HOST: str = "smtp.gmail.com"
#     SMTP_PORT: int = 587
#     SMTP_USER: str = ""
#     SMTP_PASSWORD: str = ""
#     EMAILS_FROM_EMAIL: str = "noreply@yourstore.com"
#     EMAILS_FROM_NAME: str = "Your Store"

#     # AWS S3
#     AWS_ACCESS_KEY_ID: Optional[str] = None
#     AWS_SECRET_ACCESS_KEY: Optional[str] = None
#     AWS_S3_BUCKET: Optional[str] = None
#     AWS_REGION: str = "ap-south-1"

#     # Payment
#     RAZORPAY_KEY_ID: Optional[str] = None
#     RAZORPAY_KEY_SECRET: Optional[str] = None
#     STRIPE_SECRET_KEY: Optional[str] = None
#     STRIPE_WEBHOOK_SECRET: Optional[str] = None

#     # CORS
#     ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

#     # Rate Limiting
#     RATE_LIMIT_PER_MINUTE: int = 60

#     # Frontend
#     FRONTEND_URL: str = "http://localhost:3000"

#     @validator("ALLOWED_ORIGINS", pre=True)
#     def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
#         if isinstance(v, str):
#             import json
#             return json.loads(v)
#         return v

#     class Config:
#         env_file = ".env"
#         case_sensitive = True


# settings = Settings()




from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Production Settings
    Loaded from .env
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    # ==========================================================
    # PROJECT
    # ==========================================================

    PROJECT_NAME: str = "Ecommerce API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"

    ENVIRONMENT: str = "development"

    DEBUG: bool = False
    # ==========================================================
    # ADMIN USER SEED
    # ==========================================================

    ADMIN_EMAIL: str = "admin@example.com"
    ADMIN_PASSWORD: str = "admin123"
    ADMIN_NAME: str = "Admin"
    
    # ==========================================================
    # SECURITY
    # ==========================================================

    SECRET_KEY: str

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    PASSWORD_RESET_EXPIRE_MINUTES: int = 15

    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24

    PRIVATE_KEY_PATH: str = "keys/private.pem"

    PUBLIC_KEY_PATH: str = "keys/public.pem"

    # ==========================================================
    # DATABASE
    # ==========================================================

    DATABASE_URL: str

    DATABASE_POOL_SIZE: int = 20

    DATABASE_MAX_OVERFLOW: int = 30

    DATABASE_POOL_TIMEOUT: int = 30

    DATABASE_POOL_RECYCLE: int = 1800

    DATABASE_ECHO: bool = False

    # ==========================================================
    # READ REPLICA DATABASE
    # ==========================================================

    READ_DATABASE_URL: Optional[str] = None

    # ==========================================================
    # REDIS
    # ==========================================================

    REDIS_URL: str

    REDIS_CACHE_TTL: int = 3600

    # ==========================================================
    # CORS
    # ==========================================================

    BACKEND_CORS_ORIGINS: List[str] = Field(default_factory=list)

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, value):
        if isinstance(value, str):
            return [i.strip() for i in value.split(",")]
        return value

    # ==========================================================
    # RATE LIMIT
    # ==========================================================

    RATE_LIMIT_ENABLED: bool = True

    RATE_LIMIT_REQUESTS: int = 100

    RATE_LIMIT_PERIOD_SECONDS: int = 60

    # ==========================================================
    # EMAIL SMTP
    # ==========================================================

    SMTP_HOST: str

    SMTP_PORT: int

    SMTP_USERNAME: str

    SMTP_PASSWORD: str

    SMTP_FROM_EMAIL: str

    SMTP_FROM_NAME: str = "Ecommerce"

    SMTP_TLS: bool = True

    SMTP_SSL: bool = False

    # ==========================================================
    # FILE STORAGE
    # ==========================================================

    MEDIA_ROOT: str = "media"

    MAX_FILE_SIZE: int = 5242880

    ALLOWED_IMAGE_EXTENSIONS: List[str] = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    ]

    # ==========================================================
    # RAZORPAY
    # ==========================================================

    RAZORPAY_KEY_ID: Optional[str] = None

    RAZORPAY_KEY_SECRET: Optional[str] = None

    RAZORPAY_WEBHOOK_SECRET: Optional[str] = None

    # ==========================================================
    # STRIPE
    # ==========================================================

    STRIPE_SECRET_KEY: Optional[str] = None

    STRIPE_WEBHOOK_SECRET: Optional[str] = None

    STRIPE_PUBLISHABLE_KEY: Optional[str] = None

    # ==========================================================
    # AWS
    # ==========================================================

    AWS_ACCESS_KEY_ID: Optional[str] = None

    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    AWS_REGION: Optional[str] = None

    AWS_S3_BUCKET: Optional[str] = None

    # ==========================================================
    # CELERY
    # ==========================================================

    CELERY_BROKER_URL: Optional[str] = None

    CELERY_RESULT_BACKEND: Optional[str] = None

    # ==========================================================
    # OPEN TELEMETRY
    # ==========================================================

    OTEL_ENABLED: bool = False

    OTEL_SERVICE_NAME: str = "ecommerce-api"

    OTEL_EXPORTER_OTLP_ENDPOINT: Optional[str] = None

    # ==========================================================
    # LOGGING
    # ==========================================================

    LOG_LEVEL: str = "INFO"

    LOG_JSON_FORMAT: bool = True

    LOG_FILE: str = "logs/app.log"

    # ==========================================================
    # CACHE
    # ==========================================================

    PRODUCT_CACHE_TTL: int = 300

    CATEGORY_CACHE_TTL: int = 600

    USER_CACHE_TTL: int = 300

    # ==========================================================
    # OTP
    # ==========================================================

    OTP_LENGTH: int = 6

    OTP_EXPIRE_MINUTES: int = 10

    OTP_MAX_ATTEMPTS: int = 5

    # ==========================================================
    # PASSWORD POLICY
    # ==========================================================

    PASSWORD_MIN_LENGTH: int = 8

    PASSWORD_REQUIRE_UPPERCASE: bool = True

    PASSWORD_REQUIRE_LOWERCASE: bool = True

    PASSWORD_REQUIRE_DIGIT: bool = True

    PASSWORD_REQUIRE_SPECIAL: bool = True

    # ==========================================================
    # SWAGGER
    # ==========================================================

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    OPENAPI_URL: str = "/openapi.json"

    # ==========================================================
    # APP FLAGS
    # ==========================================================

    ENABLE_REGISTRATION: bool = True

    ENABLE_EMAIL_VERIFICATION: bool = True

    ENABLE_SOCIAL_LOGIN: bool = False

    ENABLE_AUDIT_LOGS: bool = True

    ENABLE_WEBSOCKETS: bool = True

    ENABLE_BACKGROUND_TASKS: bool = True

    # ==========================================================
    # VALIDATION
    # ==========================================================

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value):
        allowed = [
            "development",
            "staging",
            "production"
        ]

        if value not in allowed:
            raise ValueError(
                f"ENVIRONMENT must be one of {allowed}"
            )

        return value

    @property
    def is_production(self):
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self):
        return self.ENVIRONMENT == "development"

    @property
    def is_staging(self):
        return self.ENVIRONMENT == "staging"

    @property
    def ACCESS_TOKEN_EXPIRE_SECONDS(self) -> int:
        return self.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()