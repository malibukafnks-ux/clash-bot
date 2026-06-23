import io
import random
import requests

import config

from PIL import Image


BASE_URL = 'https://proxy.royaleapi.dev/v1'
_cards_cache: list[dict] | None = None


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


def _get_all_cards() -> list[dict] | None:
    global _cards_cache
    if _cards_cache is not None:
        return _cards_cache

    data = _make_request('/cards')
    if data is None or 'items' not in data:
        return None

    _cards_cache = data['items']
    return _cards_cache


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
    cards = _get_all_cards()
    if not cards:
        return None
    deck = random.sample(cards, 8)
    total_elixir = sum(c.get('elixirCost', 0) for c in deck)
    avg_elixir = total_elixir / 8

    lines = [f'🎴 **Случайная колода** (средний эликсир: {avg_elixir:.1f})\n']
    for i, c in enumerate(deck, 1):
        lines.append(f'{i}. {c.get("name", "?")} (💧{c.get("elixirCost", "?")})')
    text = '\n'.join(lines)

    images = []
    for c in deck:
        url = c.get('iconUrls', {}).get('medium', '')
        if url:
            img_bytes = _download_image(url)
            if img_bytes:
                images.append(img_bytes)

    collage_bytes = None
    if len(images) == 8:
        collage_bytes = _make_collage(images)

    return text, collage_bytes


def _make_collage(images_bytes: list[bytes]) -> bytes | None:
    """Собирает коллаж 4x2 из 8 карт."""
    try:
        imgs = [Image.open(io.BytesIO(b)).convert('RGBA') for b in images_bytes]
        w, h = imgs[0].size
        collage = Image.new('RGBA', (w * 4, h * 2), (0, 0, 0, 0))
        for i, img in enumerate(imgs):
            img = img.resize((w, h))
            col, row = i % 4, i // 4
            collage.paste(img, (col * w, row * h))

        buf = io.BytesIO()
        collage.save(buf, format='PNG')
        return buf.getvalue()
    except Exception:
        return None


def get_guess_card() -> tuple[str, bytes, bytes] | None:
    """Карта для угадайки: (название, размытое фото, оригинал)."""
    cards = _get_all_cards()
    if not cards:
        return None

    card = random.choice(cards)
    name = card.get('name', '???')
    icon_url = card.get('iconUrls', {}).get('medium', '')
    if not icon_url:
        return None

    img_bytes = _download_image(icon_url)
    if not img_bytes:
        return None

    try:
        img = Image.open(io.BytesIO(img_bytes)).convert('RGBA')
        pixelated = img.resize((32, 32), Image.NEAREST)
        pixelated = pixelated.resize(img.size, Image.NEAREST)

        buf_blur = io.BytesIO()
        pixelated.save(buf_blur, format='PNG')

        buf_orig = io.BytesIO()
        img.save(buf_orig, format='PNG')

        return name, buf_blur.getvalue(), buf_orig.getvalue()
    except Exception:
        return None


def _download_image(url: str) -> bytes | None:
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.content
    except requests.RequestException:
        pass
    return None


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
    cards = _get_all_cards()
    if not cards:
        return None
    card = random.choice(cards)
    text = _card_text(card)
    icon_url = (card.get("iconUrls") or {}).get("medium")
    return text, icon_url
