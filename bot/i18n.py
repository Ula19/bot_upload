"""Мультиязычность — русский и узбекский
Использование: from bot.i18n import t
  t("start.welcome", lang="uz", name="Улугбек")
"""

TRANSLATIONS = {
    # === /start ===
    "start.welcome": {
        "ru": (
            "👋 <b>Привет, {name}!</b>\n\n"
            "🎬 Я помогу тебе скачать видео и фото из Instagram.\n\n"
            "📌 <b>Как пользоваться:</b>\n"
            "Просто отправь мне ссылку на пост, Reels или историю — "
            "и я пришлю тебе медиа! 🚀\n\n"
            "Выбери действие ниже:"
        ),
        "uz": (
            "👋 <b>Salom, {name}!</b>\n\n"
            "🎬 Instagram'dan video va rasm yuklab olishda yordam beraman.\n\n"
            "📌 <b>Qanday foydalanish:</b>\n"
            "Menga post, Reels yoki story havolasini yubor — "
            "men senga media faylni yuboraman! 🚀\n\n"
            "Quyidagi tugmalardan birini tanlang:"
        ),
    },

    # === Кнопки главного меню ===
    "btn.download": {
        "ru": "📥 Скачать видео",
        "uz": "📥 Video yuklab olish",
    },
    "btn.profile": {
        "ru": "📊 Мой профиль",
        "uz": "📊 Mening profilim",
    },
    "btn.help": {
        "ru": "❓ Помощь",
        "uz": "❓ Yordam",
    },
    "btn.back": {
        "ru": "◀️ Назад",
        "uz": "◀️ Orqaga",
    },
    "btn.language": {
        "ru": "🌐 Tilni o'zgartirish",
        "uz": "🌐 Tilni o'zgartirish",
    },

    # === Скачивание ===
    "download.prompt": {
        "ru": (
            "📥 <b>Скачивание видео из Instagram</b>\n\n"
            "Отправь мне ссылку на:\n"
            "• Пост (фото/видео)\n"
            "• Reels\n"
            "• Историю\n\n"
            "🔗 Пример: <code>https://www.instagram.com/reel/...</code>"
        ),
        "uz": (
            "📥 <b>Instagram'dan video yuklab olish</b>\n\n"
            "Menga quyidagi havolani yuboring:\n"
            "• Post (rasm/video)\n"
            "• Reels\n"
            "• Story\n\n"
            "🔗 Misol: <code>https://www.instagram.com/reel/...</code>"
        ),
    },
    "download.processing": {
        "ru": "⏳ Скачиваю... Подожди немного",
        "uz": "⏳ Yuklab olinmoqda... Biroz kuting",
    },
    "download.not_instagram": {
        "ru": (
            "🤔 Это не похоже на ссылку Instagram.\n\n"
            "Отправь ссылку вида:\n"
            "<code>https://www.instagram.com/...</code>"
        ),
        "uz": (
            "🤔 Bu Instagram havolasiga o'xshamaydi.\n\n"
            "Quyidagi ko'rinishdagi havolani yuboring:\n"
            "<code>https://www.instagram.com/...</code>"
        ),
    },
    "download.only_video": {
        "ru": "📸 Пока поддерживаются только видео, Reels и Stories.",
        "uz": "📸 Hozircha faqat video, Reels va Stories qo'llab-quvvatlanadi.",
    },

    # === Профиль ===
    "profile.title": {
        "ru": (
            "👤 <b>Твой профиль</b>\n\n"
            "📛 Имя: {full_name}\n"
            "🆔 ID: <code>{user_id}</code>\n"
            "📥 Скачиваний: {downloads}\n"
        ),
        "uz": (
            "👤 <b>Sizning profilingiz</b>\n\n"
            "📛 Ism: {full_name}\n"
            "🆔 ID: <code>{user_id}</code>\n"
            "📥 Yuklashlar: {downloads}\n"
        ),
    },

    # === Помощь ===
    "help.text": {
        "ru": (
            "❓ <b>Помощь</b>\n\n"
            "🔹 Отправь ссылку на пост Instagram — получишь видео или фото\n"
            "🔹 Поддерживаются: посты, Reels, истории\n"
            "🔹 Приватные аккаунты не поддерживаются\n\n"
            "📩 По вопросам: @admin"
        ),
        "uz": (
            "❓ <b>Yordam</b>\n\n"
            "🔹 Instagram post havolasini yuboring — video yoki rasm olasiz\n"
            "🔹 Qo'llab-quvvatlanadi: postlar, Reels, stories\n"
            "🔹 Yopiq akkauntlar qo'llab-quvvatlanmaydi\n\n"
            "📩 Savollar uchun: @admin"
        ),
    },

    # === Подписка ===
    "sub.welcome": {
        "ru": (
            "👋 <b>Привет!</b>\n\n"
            "🎬 Этот бот скачивает видео, фото и Stories "
            "из Instagram — быстро и бесплатно!\n\n"
            "🔒 <b>Для начала подпишись на каналы ниже:</b>\n\n"
            "После подписки нажми «✅ Проверить подписку»"
        ),
        "uz": (
            "👋 <b>Salom!</b>\n\n"
            "🎬 Bu bot Instagram'dan video, rasm va Stories "
            "yuklab oladi — tez va bepul!\n\n"
            "🔒 <b>Boshlash uchun quyidagi kanallarga obuna bo'ling:</b>\n\n"
            "Obuna bo'lgandan keyin «✅ Obunani tekshirish» tugmasini bosing"
        ),
    },
    "sub.not_subscribed": {
        "ru": (
            "❌ <b>Ты ещё не подписался на все каналы:</b>\n\n"
            "Подпишись и нажми «✅ Проверить подписку» ещё раз."
        ),
        "uz": (
            "❌ <b>Siz hali barcha kanallarga obuna bo'lmadingiz:</b>\n\n"
            "Obuna bo'ling va «✅ Obunani tekshirish» tugmasini qayta bosing."
        ),
    },
    "sub.success": {
        "ru": (
            "✅ <b>Отлично, {name}!</b>\n\n"
            "Теперь ты можешь пользоваться ботом! 🚀\n\n"
            "Отправь ссылку на пост, Reels или историю Instagram."
        ),
        "uz": (
            "✅ <b>Ajoyib, {name}!</b>\n\n"
            "Endi siz botdan foydalanishingiz mumkin! 🚀\n\n"
            "Instagram post, Reels yoki story havolasini yuboring."
        ),
    },
    "btn.check_sub": {
        "ru": "✅ Проверить подписку",
        "uz": "✅ Obunani tekshirish",
    },
    "sub.check_alert_fail": {
        "ru": "❌ Подпишись на все каналы!",
        "uz": "❌ Barcha kanallarga obuna bo'ling!",
    },
    "sub.check_alert_ok": {
        "ru": "✅ Подписка подтверждена!",
        "uz": "✅ Obuna tasdiqlandi!",
    },
    "sub.not_required": {
        "ru": "✅ Подписка не требуется!",
        "uz": "✅ Obuna talab qilinmaydi!",
    },

    # === Ошибки ===
    "error.session": {
        "ru": "🔑 <b>Нужна авторизация</b>\n\nДля скачивания Stories нужен INSTAGRAM_SESSION_ID.",
        "uz": "🔑 <b>Avtorizatsiya kerak</b>\n\nStories yuklab olish uchun INSTAGRAM_SESSION_ID kerak.",
    },
    "error.story_expired": {
        "ru": "⏰ <b>История не найдена</b>\n\nВозможно, она уже истекла (24 часа) или аккаунт приватный.",
        "uz": "⏰ <b>Story topilmadi</b>\n\nEhtimol, u allaqachon o'chirilgan (24 soat) yoki akkaunt yopiq.",
    },
    "error.private": {
        "ru": "🔒 <b>Аккаунт приватный</b>\n\nК сожалению, скачивание из приватных аккаунтов невозможно.",
        "uz": "🔒 <b>Akkaunt yopiq</b>\n\nAfsuski, yopiq akkauntlardan yuklab olish mumkin emas.",
    },
    "error.not_found": {
        "ru": "❌ <b>Пост не найден</b>\n\nВозможно, он удалён или ссылка неправильная.",
        "uz": "❌ <b>Post topilmadi</b>\n\nEhtimol, u o'chirilgan yoki havola noto'g'ri.",
    },
    "error.unsupported": {
        "ru": "🚫 <b>Ссылка не поддерживается</b>\n\nПоддерживаются: посты, Reels и Stories.",
        "uz": "🚫 <b>Havola qo'llab-quvvatlanmaydi</b>\n\nQo'llab-quvvatlanadi: postlar, Reels va Stories.",
    },
    "error.too_large": {
        "ru": "📦 <b>Файл слишком большой</b>\n\nTelegram ограничивает размер файла до 50 МБ.",
        "uz": "📦 <b>Fayl juda katta</b>\n\nTelegram fayl hajmini 50 MB bilan cheklaydi.",
    },
    "error.timeout": {
        "ru": "⏱ <b>Превышено время ожидания</b>\n\nПопробуй ещё раз через пару минут.",
        "uz": "⏱ <b>Kutish vaqti tugadi</b>\n\nBir necha daqiqadan keyin qayta urinib ko'ring.",
    },
    "error.generic": {
        "ru": "❌ <b>Не удалось скачать</b>\n\nПопробуй позже или проверь ссылку.",
        "uz": "❌ <b>Yuklab olib bo'lmadi</b>\n\nKeyinroq urinib ko'ring yoki havolani tekshiring.",
    },

    # === Выбор языка ===
    "lang.choose": {
        "ru": "🌐 <b>Выберите язык / Tilni tanlang:</b>",
        "uz": "🌐 <b>Tilni tanlang / Выберите язык:</b>",
    },
    "lang.changed": {
        "ru": "✅ Язык изменён на русский",
        "uz": "✅ Til o'zbek tiliga o'zgartirildi",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить перевод по ключу и языку"""
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang, translations.get("ru", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text
