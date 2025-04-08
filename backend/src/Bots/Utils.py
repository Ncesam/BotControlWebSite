import os
import importlib
import logging

logger = logging.getLogger(__name__)


def auto_register_controllers(package: str):
    """
    Автоматически импортирует все модули в указанном пакете (например, 'src.Bot.controllers'),
    чтобы активировать декораторы регистрации.
    """
    try:
        package_dir = importlib.import_module(package).__path__[0]

        for filename in os.listdir(package_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{package}.{filename[:-3]}"
                try:
                    importlib.import_module(module_name)
                    logger.debug(f"📦 Imported controller module: {module_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to import {module_name}: {e}")

    except Exception as e:
        logger.error(f"❌ Could not auto-register controllers from '{package}': {e}")
