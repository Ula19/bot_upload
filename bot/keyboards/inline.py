"""Клавиатуры бота — цветные кнопки (Bot API 9.4)
Стили: primary (синий), success (зелёный), danger (красный)
TODO: добавить icon_custom_emoji_id когда юзер пришлёт ID
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Главное меню после /start"""
    buttons = [
        [
            InlineKeyboardButton(
                text="📥 Скачать видео",
                callback_data="download_video",
                style="primary",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📊 Мой профиль",
                callback_data="my_profile",
                style="success",
            ),
            InlineKeyboardButton(
                text="❓ Помощь",
                callback_data="help",
                style="success",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Кнопка 'Назад' — красная"""
    buttons = [
        [
            InlineKeyboardButton(
                text="◀️ Назад",
                callback_data="back_to_menu",
                style="danger",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_subscription_keyboard(
    channels: list[dict],
) -> InlineKeyboardMarkup:
    """Кнопки подписки на каналы + проверка"""
    buttons = []
    for ch in channels:
        buttons.append([
            InlineKeyboardButton(
                text=f"🔔 {ch['title']}",
                url=ch["invite_link"],
                style="primary",
            ),
        ])
    buttons.append([
        InlineKeyboardButton(
            text="✅ Проверить подписку",
            callback_data="check_subscription",
            style="success",
        ),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
