# 🎬 Instagram Downloader Bot

Telegram-бот для скачивания видео, фото и Stories из Instagram.

---

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| 📥 Скачивание | Видео, Reels, фото и Stories по ссылке |
| ⚡ Кэширование | Повторные запросы — мгновенно (file_id) |
| 🌐 Мультиязычность | Русский / Узбекский + автоопределение |
| 🔔 Подписка на каналы | Обязательная подписка для использования |
| 🔄 Pending URL | Автоскачивание ссылки после подписки |
| 🔧 Админ-панель | Статистика, управление каналами |
| 🎨 UI | Цветные кнопки с эмодзи (Bot API 9.4) |

## 🛠 Стек технологий

- **Python 3.12** + **aiogram 3** — асинхронный Telegram Bot API
- **PostgreSQL** + **SQLAlchemy 2.0** — база данных
- **Cobalt API** (Docker) — скачивание видео/фото
- **Instagram Private API** — скачивание Stories
- **aiohttp** — HTTP-клиент
- **pydantic-settings** — конфигурация

## 📁 Структура проекта

```
bot_4_insta/
├── bot/
│   ├── config.py              # Настройки из .env
│   ├── i18n.py                # Переводы (ru/uz)
│   ├── main.py                # Точка входа
│   ├── database/
│   │   ├── __init__.py        # Подключение к БД
│   │   ├── models.py          # User, Channel, Download
│   │   └── crud.py            # CRUD операции
│   ├── handlers/
│   │   ├── start.py           # /start, меню, язык, подписка
│   │   ├── download.py        # Скачивание по ссылке
│   │   └── admin.py           # Админ-панель
│   ├── keyboards/
│   │   ├── inline.py          # Основные кнопки
│   │   └── admin.py           # Кнопки админки
│   ├── middlewares/
│   │   └── subscription.py    # Проверка подписки
│   ├── services/
│   │   ├── instagram.py       # Cobalt API клиент
│   │   └── stories.py         # Instagram Stories API
│   └── utils/
│       └── helpers.py         # URL валидация
├── .env.example               # Шаблон переменных
├── requirements.txt           # Зависимости
├── DEPLOY.md                  # Гайд по деплою
└── README.md
```

## ⚡ Быстрый старт

```bash
# 1. Клонирование
git clone <repo-url> && cd bot_4_insta

# 2. Виртуальное окружение
python3 -m venv venv && source venv/bin/activate

# 3. Зависимости
pip install -r requirements.txt

# 4. Настройки
cp .env.example .env
# заполнить .env (токен, БД, sessionid)

# 5. Cobalt API (Docker)
docker run -d -p 9000:9000 -e API_URL=http://localhost:9000 \
  ghcr.io/imputnet/cobalt:10

# 6. Запуск
python -m bot.main
```

## ⚙️ Переменные окружения

| Переменная | Описание |
|-----------|----------|
| `BOT_TOKEN` | Токен от @BotFather |
| `INSTAGRAM_SESSION_ID` | Cookie sessionid (запасной аккаунт!) |
| `DB_HOST` | Хост PostgreSQL |
| `DB_PORT` | Порт PostgreSQL (5432) |
| `DB_NAME` | Имя базы данных |
| `DB_USER` | Пользователь БД |
| `DB_PASSWORD` | Пароль БД |
| `ADMIN_IDS` | Telegram ID администраторов (через запятую) |
| `COBALT_API_URL` | URL Cobalt API (http://localhost:9000) |


## 👨‍💻 Админ-панель

Доступ: кнопка «🔧 Админ-панель» в меню (только для `ADMIN_IDS`)

- 📊 **Статистика** — юзеры, скачивания, каналы
- 📢 **Каналы** — добавить/удалить каналы подписки
- 🏠 **Главное меню** — вернуться в бота

## 📄 Лицензия

MIT
