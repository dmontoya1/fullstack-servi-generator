# generator/logger.py

import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Configuración básica: nivel DEBUG y salida en consola
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s:%(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
