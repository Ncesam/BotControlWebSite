from typing import List, Union


def prepare_nickname_string(nicknames: Union[str, List[str]]) -> List[str]:
    """Корректно обрабатывает никнеймы, независимо от типа входных данных."""
    if isinstance(nicknames, str):
        return [nick.strip() for nick in nicknames.split(",") if nick.strip()]
    elif isinstance(nicknames, list):
        return [nick.strip() for nick in nicknames if isinstance(nick, str)]
    return []
