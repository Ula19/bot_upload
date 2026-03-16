"""Клавиатуры бота — цветные кнопки с премиум-эмоджи (Bot API 9.4)
Стили: primary (синий), success (зелёный), danger (красный)
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import settings
from bot.emojis import E_ID
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
                icon_custom_emoji_id=E_ID["download"],
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.profile", lang),
                callback_data="my_profile",
                style="success",
                icon_custom_emoji_id=E_ID["profile"],
            ),
            InlineKeyboardButton(
                text=t("btn.help", lang),
                callback_data="help",
                style="success",
                icon_custom_emoji_id=E_ID["book"],
            ),
        ],
        [
            InlineKeyboardButton(
                text=t("btn.language", lang),
                callback_data="change_language",
                style="success",
                icon_custom_emoji_id=E_ID["globe"],
            ),
        ],
    ]

    # кнопка админки — только для админов
    if user_id and user_id in settings.admin_id_list:
        buttons.append([
            InlineKeyboardButton(
                text=t("btn.admin_panel", lang),
                callback_data="admin_panel",
                style="danger",
                icon_custom_emoji_id=E_ID["gear"],
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
                icon_custom_emoji_id=E_ID["back"],
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
                icon_custom_emoji_id=E_ID["megaphone"],
            ),
        ])
    buttons.append([
        InlineKeyboardButton(
            text=t("btn.check_sub", lang),
            callback_data="check_subscription",
            style="success",
            icon_custom_emoji_id=E_ID["check"],
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
                style="success",
            ),
            InlineKeyboardButton(
                text="🇺🇿 O'zbek",
                callback_data="set_lang_uz",
                style="success",
            ),
            InlineKeyboardButton(
                text="🇬🇧 English",
                callback_data="set_lang_en",
                style="success",
            ),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
