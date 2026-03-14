"""Клавиатуры бота — цветные кнопки (Bot API 9.4)
Стили: primary (синий), success (зелёный), danger (красный)
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import settings
from bot.i18n import t


def get_start_keyboard(
    user_id: int | None = None, lang: str = "ru"
) -> InlineKeyboardMarkup:
    """Главное меню (админам — кнопка админки)"""
    buttons = [
        [
            InlineKeyboardButton(
                text=t("btn.download", lang),
                callback_data="download_video",
                style="primary",
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.profile", lang),
                callback_data="my_profile",
                style="success",
            ),
            InlineKeyboardButton(
                text=t("btn.help", lang),
                callback_data="help",
                style="success",
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.language", lang),
                callback_data="change_language",
            ),
        ],
    ]

    # кнопка админки — только для админов
    if user_id and user_id in settings.admin_id_list:
        buttons.append([
            InlineKeyboardButton(
                text="🔧 Админ-панель",
                callback_data="admin_panel",
                style="danger",
            ),
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    """Кнопка 'Назад'"""
    buttons = [
        [
            InlineKeyboardButton(
                text=t("btn.back", lang),
                callback_data="back_to_menu",
                style="danger",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_subscription_keyboard(
    channels: list[dict], lang: str = "ru"
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
            text=t("btn.check_sub", lang),
            callback_data="check_subscription",
            style="success",
        ),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Кнопки выбора языка"""
    buttons = [
        [
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data="set_lang_ru",
            ),
            InlineKeyboardButton(
                text="🇺🇿 O'zbek",
                callback_data="set_lang_uz",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
