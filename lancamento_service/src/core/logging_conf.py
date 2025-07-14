import logging
import logging.config
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import json
import sys

class LogConfig(BaseModel):
    """Configuração de logging centralizada"""
    LOGGER_NAME: str = "app"
    LOG_FORMAT: str = "%(asctime)s.%(msecs)03d | %(levelname)-8s | %(name)s.%(funcName)s | %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_FILE: Optional[Path] = None
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_prefix = "LOG_"

def setup_logging(config: LogConfig) -> logging.Logger:
    """Configura o sistema de logging global"""
    
    handlers = {
        "default": {
            "level": config.LOG_LEVEL,
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        }
    }

    if config.LOG_FILE:
        handlers["file"] = {
            "level": config.LOG_LEVEL,
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": config.LOG_FILE,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        }

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": config.LOG_FORMAT,
                "datefmt": config.LOG_DATE_FORMAT,
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s"
            }
        },
        "handlers": handlers,
        "loggers": {
            config.LOGGER_NAME: {
                "handlers": list(handlers.keys()),
                "level": config.LOG_LEVEL,
                "propagate": False
            },
        }
    })

    return logging.getLogger(config.LOGGER_NAME)

# Configuração padrão (pode ser sobrescrita via .env)
logger = setup_logging(LogConfig())