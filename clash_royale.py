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
    tag = tag.replace('#', '%23')
    data = _make_request(f"/players/{tag}")
    if data is None:
        return None

    name = data.get("name", "???")
    trophies = data.get("trophies", 0)
    best_trophies = data.get("bestTrophies", 0)
    wins = data.get("wins", 0)
    losses = data.get("losses", 0)
    clan_name = data.get("clan" , {}).get("name" , "без клана")
    return (
        f'👤 **{name}**\n'
        f'🏆 Трофеи: {trophies} (рекорд: {best_trophies})\n'
        f'⚔️ Победы: {wins} | Поражения: {losses}\n'
        f'🛡️ Клан: {clan_name}'
    )

def get_random_deck():
    data = _make_request("/cards")
    if data is None or 'items' not in data:
        return None
    deck = random.sample(data['items'], 8)
    avg_elixir = sum(card.get('elixirCost', 0) for card in deck) / 8

    lines = [f'Случайная колода. Средний эликсир: {avg_elixir:.1f}']
    for index, card in enumerate(deck, 1):
        name = card.get('name', '?')
        elixir = card.get('elixirCost', '?')
        lines.append(f'{index}. {name} — {elixir}')

    return '\n'.join(lines)





def _card_text(card):
    name = card.get("name", "???")
    elixir = card.get("elixirCost", "???")
    rarity = card.get("rarity", "???")
    max_level = card.get('maxLevel', "???")

    return (
        f'🃏 **{name}**\n'
        f'💧 Эликсир: {elixir}\n'
        f'⭐ Редкость: {rarity}\n'
        f'⬆️ Макс. уровень: {max_level}'
    )

def get_random_card():
    data = _make_request("/cards")
    if data is None or 'items' not in data:
        return None
    card = random.choice(data["items"])
    text = _card_text(card)
    icon_url = (card.get("iconUrls") or {}).get("medium")
    return text, icon_url
