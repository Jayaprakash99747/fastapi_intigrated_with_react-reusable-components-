# # from pydantic_settings import BaseSettings
# # from functools import lru_cache

# # class Settings(BaseSettings):
# #     DATABASE_URL: str
# #     SECRET_KEY: str
# #     ALGORITHM: str = "HS256"
# #     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
# #     REFRESH_TOKEN_EXPIRE_DAYS: int = 7

# #     GOOGLE_CLIENT_ID: str
# #     GOOGLE_CLIENT_SECRET: str
# #     GOOGLE_REDIRECT_URI: str

# #     EMAIL_HOST: str
# #     EMAIL_PORT: int
# #     EMAIL_USER: str
# #     EMAIL_PASSWORD: str
# #     FRONTEND_URL: str

# #     class Config:
# #         env_file = ".env"
# #         extra = "ignore"

# # @lru_cache()
# # def get_settings():
# #     return Settings()


# # from pydantic_settings import BaseSettings,SettingsConfigDict
# # from functools import lru_cache
# # from typing import Literal

# # class Settings(BaseSettings):
# #     DATABASE_URL: str
# #     SECRET_KEY: str
# #     ALGORITHM: str = "HS256"
# #     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
# #     REFRESH_TOKEN_EXPIRE_DAYS: int = 7

# #     GOOGLE_CLIENT_ID: str
# #     GOOGLE_CLIENT_SECRET: str
# #     GOOGLE_REDIRECT_URI: str

# #     EMAIL_HOST: str
# #     EMAIL_PORT: int
# #     EMAIL_USER: str
# #     EMAIL_PASSWORD: str
# #     FRONTEND_URL: str

# #     RAZORPAY_KEY_ID: str
# #     RAZORPAY_KEY_SECRET: str

# #     class Config:
# #         env_file = ".env"
# #         extra = "ignore"


# #     ENVIRONMENT: Literal["development", "staging", "production"] = "development"

# #     model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
# # @lru_cache()
# # def get_settings():
# #     return Settings()




# from pydantic_settings import BaseSettings, SettingsConfigDict
# from typing import Literal

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#     REFRESH_TOKEN_EXPIRE_DAYS: int = 7

#     RAZORPAY_KEY_ID: str
#     RAZORPAY_KEY_SECRET: str

#     ENVIRONMENT: Literal["development", "staging", "production"] = "development"

#     model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# settings = Settings()







import json
import logging
import logging.config
import os
import sys
import uuid
from contextvars import ContextVar
from pathlib import Path

from app.core.settings import settings


# ==========================================================
# REQUEST CONTEXT
# ==========================================================

request_id_ctx_var: ContextVar[str] = ContextVar(
    "request_id",
    default="-"
)

user_id_ctx_var: ContextVar[str] = ContextVar(
    "user_id",
    default="-"
)


# ==========================================================
# REQUEST ID HELPERS
# ==========================================================

def set_request_id(request_id: str | None = None):
    request_id_ctx_var.set(
        request_id or str(uuid.uuid4())
    )


def get_request_id() -> str:
    return request_id_ctx_var.get()


def set_user_id(user_id: str):
    user_id_ctx_var.set(user_id)


def get_user_id() -> str:
    return user_id_ctx_var.get()


# ==========================================================
# JSON FORMATTER
# ==========================================================

class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "timestamp": self.formatTime(
                record,
                self.datefmt
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": get_request_id(),
            "user_id": get_user_id(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_record["exception"] = (
                self.formatException(
                    record.exc_info
                )
            )

        return json.dumps(
            log_record,
            default=str
        )


# ==========================================================
# LOG DIRECTORY
# ==========================================================

BASE_DIR = Path.cwd()

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    exist_ok=True,
    parents=True
)

LOG_FILE = LOG_DIR / "app.log"

ERROR_LOG_FILE = LOG_DIR / "error.log"


# ==========================================================
# LOGGING CONFIG
# ==========================================================

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {

        "json": {
            "()": JsonFormatter
        },

        "default": {
            "format":
                "%(asctime)s | "
                "%(levelname)s | "
                "%(name)s | "
                "%(message)s"
        },
    },

    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter":
                "json"
                if settings.LOG_JSON_FORMAT
                else "default",
        },

        "file": {
            "class":
                "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_FILE),
            "maxBytes": 10485760,
            "backupCount": 10,
            "formatter":
                "json"
                if settings.LOG_JSON_FORMAT
                else "default",
            "encoding": "utf-8",
        },

        "error_file": {
            "class":
                "logging.handlers.RotatingFileHandler",
            "filename": str(ERROR_LOG_FILE),
            "maxBytes": 10485760,
            "backupCount": 10,
            "formatter":
                "json"
                if settings.LOG_JSON_FORMAT
                else "default",
            "level": "ERROR",
            "encoding": "utf-8",
        },
    },

    "root": {
        "handlers": [
            "console",
            "file",
            "error_file",
        ],
        "level": settings.LOG_LEVEL,
    },
}


# ==========================================================
# SETUP LOGGING
# ==========================================================

def setup_logging():

    logging.config.dictConfig(
        LOGGING_CONFIG
    )

    logger = logging.getLogger(
        "application"
    )

    logger.info(
        "Logging initialized"
    )

    return logger


# ==========================================================
# APP LOGGER
# ==========================================================

logger = setup_logging()


# ==========================================================
# AUDIT LOGGER
# ==========================================================

audit_logger = logging.getLogger(
    "audit"
)


# ==========================================================
# SECURITY LOGGER
# ==========================================================

security_logger = logging.getLogger(
    "security"
)


# ==========================================================
# DATABASE LOGGER
# ==========================================================

db_logger = logging.getLogger(
    "database"
)


# ==========================================================
# EMAIL LOGGER
# ==========================================================

email_logger = logging.getLogger(
    "email"
)


# ==========================================================
# PAYMENT LOGGER
# ==========================================================

payment_logger = logging.getLogger(
    "payment"
)


# ==========================================================
# AUDIT EVENT
# ==========================================================

def audit_log(
    action: str,
    user_id: str | int,
    resource: str,
    resource_id: str | int | None = None,
):

    audit_logger.info(
        {
            "action": action,
            "user_id": user_id,
            "resource": resource,
            "resource_id": resource_id,
        }
    )


# ==========================================================
# SECURITY EVENT
# ==========================================================

def security_log(
    event: str,
    message: str,
):

    security_logger.warning(
        {
            "event": event,
            "message": message,
        }
    )


# ==========================================================
# PAYMENT EVENT
# ==========================================================

def payment_log(
    event: str,
    data: dict,
):

    payment_logger.info(
        {
            "event": event,
            "data": data,
        }
    )


# ==========================================================
# DATABASE EVENT
# ==========================================================

def database_log(
    event: str,
    message: str,
):

    db_logger.info(
        {
            "event": event,
            "message": message,
        }
    )


# ==========================================================
# EMAIL EVENT
# ==========================================================

def email_log(
    event: str,
    recipient: str,
):

    email_logger.info(
        {
            "event": event,
            "recipient": recipient,
        }
    )


# ==========================================================
# OPEN TELEMETRY PLACEHOLDER
# ==========================================================

def initialize_telemetry():

    if not settings.OTEL_ENABLED:
        return

    logger.info(
        "OpenTelemetry initialization started"
    )

    """
    Install later:

    opentelemetry-api
    opentelemetry-sdk
    opentelemetry-exporter-otlp

    Configure tracer provider here.
    """


# ==========================================================
# STARTUP CONFIG
# ==========================================================

def initialize_app_config():

    logger.info(
        f"Environment: {settings.ENVIRONMENT}"
    )

    logger.info(
        f"Project: {settings.PROJECT_NAME}"
    )

    initialize_telemetry()

    logger.info(
        "Application configuration loaded"
    )