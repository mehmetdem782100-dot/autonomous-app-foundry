import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="DEBUG"
)
logger.add(
    "logs/cognita_{time:YYYY-MM-DD}.log",
    rotation="50 MB",
    retention="10 days",
    level="INFO",
    serialize=True
)

def get_logger(module_name: str):
    return logger.bind(module=module_name)
