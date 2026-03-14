"""Хэндлер /start — приветствие и главное меню"""
import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.database import async_session
from bot.database.crud import get_or_create_user
from bot.keyboards.inline import get_back_keyboard, get_start_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обработка команды /start"""
    async with async_session() as session:
        await get_or_create_user(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )

    # Приветственное сообщение
    welcome_text = (
        f"👋 <b>Привет, {message.from_user.first_name}!</b>\n\n"
        "🎬 Я помогу тебе скачать видео и фото из Instagram.\n\n"
        "📌 <b>Как пользоваться:</b>\n"
        "Просто отправь мне ссылку на пост, Reels или историю — "
        "и я пришлю тебе медиа! 🚀\n\n"
        "Выбери действие ниже:"
    )

    await message.answer(
        welcome_text,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery) -> None:
    """Возврат в главное меню"""
    welcome_text = (
        f"👋 <b>Привет, {callback.from_user.first_name}!</b>\n\n"
        "🎬 Я помогу тебе скачать видео и фото из Instagram.\n\n"
        "📌 <b>Как пользоваться:</b>\n"
        "Просто отправь мне ссылку на пост, Reels или историю — "
        "и я пришлю тебе медиа! 🚀\n\n"
        "Выбери действие ниже:"
    )

    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "download_video")
async def download_video_prompt(callback: CallbackQuery) -> None:
    """Нажатие на кнопку 'Скачать видео'"""
    text = (
        "📥 <b>Скачивание видео из Instagram</b>\n\n"
        "Отправь мне ссылку на:\n"
        "• Пост (фото/видео)\n"
        "• Reels\n"
        "• Историю\n\n"
        "🔗 Пример: <code>https://www.instagram.com/reel/...</code>"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "my_profile")
async def my_profile(callback: CallbackQuery) -> None:
    """Профиль пользователя"""
    async with async_session() as session:
        user = await get_or_create_user(
            session=session,
            telegram_id=callback.from_user.id,
            username=callback.from_user.username,
            full_name=callback.from_user.full_name,
        )

    text = (
        f"👤 <b>Твой профиль</b>\n\n"
        f"📛 Имя: {callback.from_user.full_name}\n"
        f"🆔 ID: <code>{callback.from_user.id}</code>\n"
        f"📥 Скачиваний: {user.download_count}\n"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery) -> None:
    """Помощь"""
    text = (
        "❓ <b>Помощь</b>\n\n"
        "🔹 Отправь ссылку на пост Instagram — получишь видео или фото\n"
        "🔹 Поддерживаются: посты, Reels, истории\n"
        "🔹 Приватные аккаунты не поддерживаются\n\n"
        "📩 По вопросам: @admin"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_back_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery) -> None:
    """Проверка подписки на каналы"""
    from bot.database.crud import get_active_channels
    from bot.middlewares.subscription import is_subscribed

    async with async_session() as session:
        channels = await get_active_channels(session)

    if not channels:
        await callback.answer("✅ Подписка не требуется!")
        return

    bot = callback.bot
    not_subscribed = []

    for channel in channels:
        if not await is_subscribed(bot, channel.channel_id, callback.from_user.id):
            not_subscribed.append({
                "title": channel.title,
                "invite_link": channel.invite_link,
            })

    if not_subscribed:
        # ещё не подписался
        from bot.keyboards.inline import get_subscription_keyboard
        text = (
            "❌ <b>Ты ещё не подписался на все каналы:</b>\n\n"
            "Подпишись и нажми «✅ Проверить подписку» ещё раз."
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_subscription_keyboard(not_subscribed),
            parse_mode="HTML",
        )
        await callback.answer("❌ Подпишись на все каналы!", show_alert=True)
    else:
        # подписан — показываем главное меню
        welcome_text = (
            f"✅ <b>Отлично, {callback.from_user.first_name}!</b>\n\n"
            "Теперь ты можешь пользоваться ботом! 🚀\n\n"
            "Отправь ссылку на пост, Reels или историю Instagram."
        )
        await callback.message.edit_text(
            welcome_text,
            reply_markup=get_start_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer("✅ Подписка подтверждена!")
