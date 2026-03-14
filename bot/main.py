"""Точка входа — запуск бота"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy import text

from bot.config import settings
from bot.database import engine
from bot.database.models import Base
from bot.handlers import admin, download, start
from bot.middlewares.subscription import SubscriptionMiddleware

# настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    """Действия при запуске бота"""
    # создаём таблицы если их нет
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # миграция: добавляем колонку language если её нет
        try:
            await conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS language VARCHAR(5) DEFAULT 'ru'"
            ))
        except Exception:
            pass  # колонка уже есть или ошибка — не критично

    logger.info("Таблицы БД созданы/проверены")

    # получаем информацию о боте
    bot_info = await bot.get_me()
    logger.info(f"Бот запущен: @{bot_info.username}")


async def on_shutdown(bot: Bot) -> None:
    """Действия при остановке бота"""
    await engine.dispose()
    logger.info("Бот остановлен, соединение с БД закрыто")


async def main() -> None:
    """Главная функция запуска"""
    # создаём бота с HTML-парсингом по умолчанию
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # диспетчер для обработки событий
    dp = Dispatcher()

    # регистрируем хэндлеры (порядок важен!)
    dp.include_router(start.router)      # /start и меню — первый
    dp.include_router(admin.router)      # /admin — второй
    dp.include_router(download.router)   # ссылки Instagram — последний

    # мидлварь проверки подписки на каналы
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())

    # хуки запуска/остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("Запускаем бота...")

    # запуск polling (получение обновлений)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
