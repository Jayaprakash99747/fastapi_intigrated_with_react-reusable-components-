# import sys
# from loguru import logger
# from app.core.settings import settings

# # Remove default handler
# logger.remove()

# # Console
# logger.add(
#     sys.stdout,
#     format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
#     level="DEBUG" if settings.DEBUG else "INFO",
#     colorize=True,
# )

# # File - all logs
# logger.add(
#     "logs/app.log",
#     rotation="10 MB",
#     retention="30 days",
#     compression="zip",
#     level="INFO",
#     format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
# )

# # File - errors only
# logger.add(
#     "logs/error.log",
#     rotation="10 MB",
#     retention="30 days",
#     compression="zip",
#     level="ERROR",
#     format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
# )

# __all__ = ["logger"]








import logging
import json
import sys


class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
        }

        return json.dumps(log_record)


def get_logger(name: str = "app"):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = get_logger("app_logger")