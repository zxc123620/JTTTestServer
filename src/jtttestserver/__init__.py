import os.path

import logging.config

import dotenv

def init_logger_config():
    """
    初始化日志配置
    """
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    log_config_data = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s|%(name)s|%(levelname)s|%(filename)s|%(lineno)d: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "info_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "interval": 1,
                "backupCount": 30,
                "filename": "./logs/info.log",
                "when": "midnight",

                "encoding": "utf8"
            },
            "error_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "./logs/errors.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf8"
            },
            "debug_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "./logs/debug.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf8"
            },
            "api_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "./logs/api.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 30,
                "encoding": "utf8",

            }
        },
        "loggers": {},
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "info_file_handler", "error_file_handler", "debug_file_handler"]
        }
    }
    logging.config.dictConfig(log_config_data)


def init_environment():
    """
    初始化环境变量
    :return:
    """
    dotenv.load_dotenv(verbose=True)

