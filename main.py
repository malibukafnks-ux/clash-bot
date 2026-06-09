from pyrogram import Client, filters
from pyrogram.types import Message

import config
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
        '/card — случайная карта Clash Royale, добавим позже\n'
        '/player <тег> — игрок Clash Royale, добавим позже'
    )

@bot.on_message(filters.command('kaomoji'))
async def kaomoji_command(client: Client, message: Message):
    await message.reply(get_random_kaomoji())

if __name__ == "__main__":
    print('Bot started')
    bot.run()
