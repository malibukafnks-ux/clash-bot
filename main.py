import io

from pyrogram import Client, filters
from pyrogram.types import Message
import requests

import config
from clash_royale import get_random_card, get_player_info, get_random_deck, get_guess_card
from kaomoji import get_random_kaomoji


guess_games: dict[int, tuple[str, bytes]] = {}


bot = Client(
    "clash_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,

)


def _png_file(data: bytes, name: str) -> io.BytesIO:
    file = io.BytesIO(data)
    file.name = name
    return file


@bot.on_message(filters.command('start'))
async def start_command(client: Client, message: Message):
    await message.reply(
        '👋 Привет! Вот что я умею:\n\n'
        '🖼 /randomcard — случайная карта с картинкой\n'
        '🎴 /randomdeck — случайная колода из 8 карт\n'
        '🔍 /guess — угадай карту по пикселям!\n'
        '👤 /player <тег> — информация об игроке CR\n'
        '😜 /kaomoji — случайная ASCII-эмоция\n\n'
        'Попробуй любую команду!'
    )


@bot.on_message(filters.command('kaomoji'))
async def kaomoji_command(client: Client, message: Message):
    await message.reply(get_random_kaomoji())


@bot.on_message(filters.command('randomcard'))
async def randomcard_command(client: Client, message: Message):
    result = get_random_card()
    if result is None:
        await message.reply('Не удалось получить карту. Попробуй позже.')
        return

    text, icon_url = result
    if icon_url:
        await message.reply_photo(icon_url, caption=text)
    else:
        await message.reply(text)


@bot.on_message(filters.command('player'))
async def player_command(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply('Укажи тег игрока. Пример: /player #C0G20PR2')
        return
    player = get_player_info(message.command [1])
    if player is None:
        await message.reply('Игрок не найден. Проверь тег.')
        return
    await message.reply(player)


@bot.on_message(filters.command('randomdeck'))
async def randomdeck_command(client: Client, message: Message):
    result = get_random_deck()
    if result is None:
        await message.reply('Не удалось собрать колоду. Попробуй позже.')
        return
    text, collage_bytes = result
    if collage_bytes:
        await message.reply_photo(_png_file(collage_bytes, 'deck.png'), caption=text)
    else:
        await message.reply(text)


@bot.on_message(filters.command('guess'))
async def guess_command(client: Client, message: Message):
    result = get_guess_card()
    if result is None:
        await message.reply('Не удалось загрузить карту. Попробуй позже.')
        return

    name, blurred, original = result
    guess_games[message.chat.id] = (name, original)

    await message.reply_photo(
        _png_file(blurred, 'guess.png'),
        caption=(
            '🔍 **Угадай карту!**\n'
            'Напиши название карты (на английском).\n'
            'Подсказка: /giveup — сдаться и увидеть ответ.'
        ),
    )


@bot.on_message(filters.command('giveup'))
async def giveup_command(client: Client, message: Message):
    game = guess_games.pop(message.chat.id, None)
    if game is None:
        await message.reply('Нет активной игры. Начни новую: /guess')
        return

    name, original = game
    await message.reply_photo(
        _png_file(original, 'card.png'),
        caption=f'😅 Это была карта: **{name}**',
    )


@bot.on_message(filters.text)
async def guess_answer_handler(client: Client, message: Message):
    if not message.text or message.text.startswith('/'):
        return

    game = guess_games.get(message.chat.id)
    if game is None:
        return

    name, original = game
    user_answer = message.text.strip().lower()

    if user_answer == name.lower():
        guess_games.pop(message.chat.id, None)
        await message.reply_photo(
            _png_file(original, 'card.png'),
            caption=f'🎉 Правильно! Это **{name}**!',
        )
    else:
        await message.reply('❌ Неправильно, попробуй ещё! Или /giveup чтобы сдаться.')


if __name__ == "__main__":
    print('Bot started')
    try:
        outbound_ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f'Outbound ip: {outbound_ip}')
    except requests.RequestException as error:
        print(f'Outbound ip: failed ({error})')
    bot.run()
