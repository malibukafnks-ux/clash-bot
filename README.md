# 🤖 Clash Bot

Telegram-бот на Python и Pyrogram для фанатов Clash Royale. Показывает случайные карты, собирает колоды, ищет статистику игроков и запускает мини-игру «угадай карту» 🎴

## ✨ Возможности

- 🖼️ Случайная карта Clash Royale с изображением и характеристиками
- 🎴 Случайная колода из 8 карт со средним эликсиром и коллажем
- 🔍 Мини-игра: угадай карту по пиксельной картинке
- 😅 Команда `/giveup`, чтобы сдаться и увидеть правильный ответ
- 👤 Поиск информации об игроке по тегу Clash Royale
- 😜 Случайные kaomoji для настроения

## 💬 Команды

| Команда | Что делает |
|---------|------------|
| `/start` | Показывает список возможностей бота |
| `/randomcard` | Отправляет случайную карту с картинкой |
| `/randomdeck` | Собирает случайную колоду из 8 карт |
| `/guess` | Запускает игру «угадай карту» |
| `/giveup` | Завершает активную игру и показывает ответ |
| `/player <тег>` | Показывает статистику игрока Clash Royale |
| `/kaomoji` | Отправляет случайную ASCII-эмоцию |

## 🚀 Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/<ваш-аккаунт>/clash-bot.git
cd clash-bot

# Создать виртуальное окружение и установить зависимости
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt

# Создать .env и заполнить токены
cp .env.example .env

# Запустить бота
python main.py
```

## 🔐 Переменные окружения

| Переменная | Описание |
|------------|----------|
| `API_ID` | ID приложения Telegram из my.telegram.org |
| `API_HASH` | Hash приложения Telegram из my.telegram.org |
| `BOT_TOKEN` | Токен Telegram-бота от BotFather |
| `CR_API_TOKEN` | Токен Clash Royale API |

## 📁 Структура проекта

```text
clash-bot/
├── main.py           — команды Telegram-бота и логика угадайки
├── clash_royale.py   — запросы к Clash Royale API, карты, колоды, изображения
├── kaomoji.py        — список kaomoji и выбор случайной эмоции
├── config.py         — загрузка переменных окружения из .env
├── .env.example      — пример конфигурации без секретов
├── railway.toml      — команда запуска для Railway
└── requirements.txt  — зависимости проекта
```

## 🛠️ Технологии

- **Python 3.12+** 🐍
- **Pyrogram 2** 💬
- **Pillow** 🖼️
- **Requests** 🌐
- **python-dotenv** 🔐
- **Clash Royale API** ⚔️

## ☁️ Деплой

Проект готов к запуску на Railway: команда старта уже указана в `railway.toml`.

Перед деплоем добавь переменные `API_ID`, `API_HASH`, `BOT_TOKEN` и `CR_API_TOKEN` в настройках окружения сервиса.

## 👾 Автор

Учебный проект Skillbox — Telegram-бот с Clash Royale API и мини-игрой.
