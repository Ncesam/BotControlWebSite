import asyncio
import json
import logging
import re
import requests

from src.BotsLogics.Schemas.Price import Price
from src.BotsLogics.ShopDataBase import price_database
from src.BotsLogics.Utils import get_random_headers

logger = logging.getLogger(__name__)


async def fetch_price_for_item(item: dict):
    try:
        logger.debug(f"Запрос цены для item_id={item['id']}")
        headers = get_random_headers(item_id=item["id"])
        url = f"https://vip3.activeusers.ru/app.php?act=item&id={item['id']}&sign=WAltA8GrnTaOlhGsNoivHasChPIWlfUuWsonSgob_X8&vk_access_token_settings=&vk_app_id=6987489&vk_are_notifications_enabled=0&vk_is_app_user=1&vk_is_favorite=0&vk_language=ru&vk_platform=mobile_web&vk_ref=other&vk_ts=1744485280&vk_user_id=623309596&back=act:user"

        response = requests.request("GET", url, headers=headers)
        html = response.text
        prices = []
        pattern = r"window\.graph_data\s*=\s*(\[\[.*?\]\]);"
        title_pattern = r'<div class="shop_res-title">(.+?)</div>'

        title_match = re.search(title_pattern, html, re.DOTALL)
        match = re.search(pattern, html, re.DOTALL)
        if not match:
            # print("Данные window.graph_data не найдены на странице")
            return None
        if not title_match:
            return None

        title = title_match.group(1)
        title = title.strip()
        data_str = match.group(1)

        try:
            graph_data = json.loads(data_str)
        except json.JSONDecodeError as e:
            print("Ошибка при разборе JSON:", e)
            return None
        for pair in graph_data:
            if isinstance(pair, list) and len(pair) >= 2:
                timestamp, price = pair[:2]
                prices.append(price)

        await price_database.update_item(
            item["id"],
            Price(
                low_price=min(prices),
                high_price=max(prices),
                average_price=sum(prices) / len(prices),
            ),
            title=title,
        )

        logger.info(
            f"[item_id={item['id']}] Обновлены цены: min={min(prices)}, avg={sum(prices) / len(prices):.2f}, max={max(prices)}"
        )

    except Exception as e:
        logger.exception(f"[item_id={item['id']}] Ошибка: {e}")


async def fetch_price():
    items_list = await price_database.get_all_price()
    logger.info(f"Начинаем обработку {len(items_list)} товаров")

    for item in items_list:
        await asyncio.sleep(2)
        await fetch_price_for_item(item)


def price_updater_start():
    loop = asyncio.new_event_loop()
    task = loop.create_task(price_updater_loop())
    loop.run_until_complete(task)


async def price_updater_loop():
    await asyncio.sleep(10)
    while True:
        try:
            await fetch_price()
        except Exception as e:
            logger.exception("Ошибка при обновлении цен: %s", e)
        await asyncio.sleep(30 * 60)  # 30 минут
