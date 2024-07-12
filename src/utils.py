import logging
import importlib

class Logger:
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Create and configure a logger.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

def dynamic_import(module_name: str, class_name: str):
    """
    Dynamically import a class from a module.
    """
    module = importlib.import_module(module_name)
    return getattr(module, class_name)