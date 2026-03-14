"""Мидлварь проверки подписки на каналы
Если есть обязательные каналы — юзер должен быть подписан на ВСЕ.
Если каналов нет — пропускаем (бот работает без ограничений).
"""
import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.config import settings
from bot.database import async_session
from bot.database.crud import get_active_channels, get_user_language
from bot.i18n import t
from bot.keyboards.inline import get_subscription_keyboard

logger = logging.getLogger(__name__)

# эти callback_data пропускаем без проверки
SKIP_CALLBACKS = {"check_subscription", "set_lang_ru", "set_lang_uz", "change_language"}


class SubscriptionMiddleware(BaseMiddleware):
    """Проверяет подписку юзера на обязательные каналы"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        # пропускаем кнопку "Проверить подписку" и админские callback
        if isinstance(event, CallbackQuery) and (
            event.data in SKIP_CALLBACKS or event.data.startswith("admin")
        ):
            return await handler(event, data)

        # определяем юзера
        user = None
        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user

        # админы проходят без проверки
        if user and user.id in settings.admin_id_list:
            return await handler(event, data)

        # получаем список каналов
        async with async_session() as session:
            channels = await get_active_channels(session)

        # если каналов нет — пропускаем проверку
        if not channels:
            return await handler(event, data)

        # проверяем подписку на все каналы
        bot: Bot = data["bot"]
        not_subscribed = []

        for channel in channels:
            if not await is_subscribed(bot, channel.channel_id, user.id):
                not_subscribed.append({
                    "title": channel.title,
                    "invite_link": channel.invite_link,
                })

        # если подписан на всё — пропускаем
        if not not_subscribed:
            return await handler(event, data)

        # не подписан — получаем язык и показываем приветствие
        async with async_session() as session:
            lang = await get_user_language(session, user.id) if user else "ru"

        text = t("sub.welcome", lang)
        keyboard = get_subscription_keyboard(not_subscribed, lang)

        if isinstance(event, Message):
            await event.answer(text, reply_markup=keyboard, parse_mode="HTML")
        elif isinstance(event, CallbackQuery):
            await event.message.edit_text(
                text, reply_markup=keyboard, parse_mode="HTML"
            )
            await event.answer()

        # НЕ вызываем handler — блокируем действие
        return None


async def is_subscribed(bot: Bot, channel_id: int, user_id: int) -> bool:
    """Проверяет, подписан ли юзер на канал"""
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        # эти статусы = подписан
        return member.status in ("member", "administrator", "creator")
    except Exception as e:
        logger.warning(f"Не удалось проверить подписку {user_id} на {channel_id}: {e}")
        # если ошибка — пропускаем (чтобы бот не ломался)
        return True
