import os
import importlib
import logging
import random

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


def get_random_headers(item_id):
    return {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": random.choice(["en-US,en;q=0.9", "ru-RU,ru;q=0.9"]),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://vip3.activeusers.ru",
        "Referer": build_referer(item_id),
        "User-Agent": random.choice(USER_AGENTS),
    }


def build_referer(item_id):
    return f"https://vip3.activeusers.ru/app.php?act=item&id={item_id}&sign=WAltA8GrnTaOlhGsNoivHasChPIWlfUuWsonSgob_X8&vk_access_token_settings=&vk_app_id=6987489&vk_are_notifications_enabled=0&vk_is_app_user=1&vk_is_favorite=0&vk_language=ru&vk_platform=mobile_web&vk_ref=other&vk_ts=1744485280&vk_user_id=623309596&back=act:user"


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
]
