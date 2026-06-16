import random
import requests
import config

BASE_URL = 'https://proxy.royaleapi.dev/v1'

def _make_request(endpoint: str, params=None) -> dict | None:
    headers = {
        'Authorization': f'Bearer {config.CR_API_TOKEN}',
        'Accept': 'application/json',
    }
    try:
        response = requests.get(
            f'{BASE_URL}{endpoint}',
            headers=headers,
            params=params,
            timeout=10,
        )
    except requests.RequestException:
        return None

    if response.status_code == 200:
        return response.json()
    return None

def get_player_info(tag):
    pass

def get_random_card():
    data = _make_request("/cards")
    if data is None or 'items' not in data:
        return None
    card = random.choice(data["items"])
    name = card.get("name", "???")
    elixir = card.get("elixirCost", "???")
    rarity = card.get("rarity", "???")
    icon_url = card.get("iconUrls", "???")
    text = (
        f'Карта: {name}\n'
        f'Эликсир: {elixir}\n'
        f'Редкость: {rarity}'
    )
    return text, icon_url