"""Клавиатуры админ-панели"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


def get_admin_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Главное меню админки"""
    buttons = [
        [
            InlineKeyboardButton(
                text=t("btn.admin_stats", lang),
                callback_data="admin_stats",
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.admin_channels", lang),
                callback_data="admin_channels",
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.admin_home", lang),
                callback_data="back_to_menu",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_channels_keyboard(
    channels: list | None = None, lang: str = "ru"
) -> InlineKeyboardMarkup:
    """Клавиатура управления каналами"""
    buttons = []

    if channels:
        for ch in channels:
            buttons.append([
                InlineKeyboardButton(
                    text=f"🗑 {ch.title}",
                    callback_data=f"admin_del_{ch.channel_id}",
                ),
            ])

    buttons.append([
        InlineKeyboardButton(
            text=t("btn.admin_add", lang),
            callback_data="admin_add_channel",
        ),
    ])
    buttons.append([
        InlineKeyboardButton(
            text=t("btn.admin_back", lang),
            callback_data="admin_cancel",
        ),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_cancel_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка отмены"""
    buttons = [
        [
            InlineKeyboardButton(
                text=t("btn.admin_cancel", lang),
                callback_data="admin_cancel",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
