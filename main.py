from pyrogram import Client, filters
from pyrogram.types import Message
import requests

import config
from clash_royale import get_random_card
from kaomoji import get_random_kaomoji


bot = Client(
    "clash_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,

)


@bot.on_message(filters.command('start'))
async def start_command(client: Client, message: Message):
    await message.reply(
        'Привет! Я Clash Royale + Kaomoji бот.\n\n'
        '/kaomoji — случайная текстовая эмоция\n'
        '/randomcard — случайная карта Clash Royale, добавим позже\n'
        '/player <тег> — игрок Clash Royale, добавим позже'
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


if __name__ == "__main__":
    print('Bot started')
    try:
        outbound_ip = requests.get('https://api.ipify.org', timeout=5).text
        print(f'Outbound ip: {outbound_ip}')
    except requests.RequestException as error:
        print(f'Outbound ip: failed ({error})')
    bot.run()
