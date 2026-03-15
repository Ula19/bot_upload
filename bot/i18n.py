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
            "Menga post, Reels yoki story havolasini yuboring — "
            "men sizga media faylni yuboraman! 🚀\n\n"
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
        "ru": "🌐 Сменить язык",
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
    "error.rate_limit": {
        "ru": "⏳ <b>Слишком много запросов!</b>\n\nПодожди {seconds} секунд и попробуй снова.",
        "uz": "⏳ <b>Juda ko'p so'rovlar!</b>\n\n{seconds} soniya kuting va qayta urinib ko'ring.",
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

    # === Админ-панель ===
    "admin.title": {
        "ru": "🔧 <b>Админ-панель</b>\n\nВыбери действие:",
        "uz": "🔧 <b>Admin panel</b>\n\nAmalni tanlang:",
    },
    "admin.no_access": {
        "ru": "🚫 У тебя нет доступа к админке.",
        "uz": "🚫 Sizda admin panelga kirish huquqi yo'q.",
    },
    "admin.stats": {
        "ru": (
            "📊 <b>Статистика бота</b>\n\n"
            "👥 Всего юзеров: <b>{total_users}</b>\n"
            "🆕 За сегодня: <b>{today_users}</b>\n"
            "📥 Всего скачиваний: <b>{total_downloads}</b>\n"
            "📢 Каналов: <b>{total_channels}</b>"
        ),
        "uz": (
            "📊 <b>Bot statistikasi</b>\n\n"
            "👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
            "🆕 Bugun: <b>{today_users}</b>\n"
            "📥 Jami yuklashlar: <b>{total_downloads}</b>\n"
            "📢 Kanallar: <b>{total_channels}</b>"
        ),
    },
    "admin.channels_empty": {
        "ru": "📢 <b>Каналы</b>\n\nСписок пуст. Добавь канал кнопкой ниже.",
        "uz": "📢 <b>Kanallar</b>\n\nRo'yxat bo'sh. Quyidagi tugma orqali kanal qo'shing.",
    },
    "admin.channels_title": {
        "ru": "📢 <b>Каналы для подписки:</b>\n",
        "uz": "📢 <b>Obuna kanallari:</b>\n",
    },
    "admin.add_channel_id": {
        "ru": (
            "📢 <b>Добавление канала</b>\n\n"
            "Отправь <b>ID канала</b> (числовой, например <code>-1001234567890</code>)\n\n"
            "💡 Узнать ID: добавь бота @getmyid_bot в канал"
        ),
        "uz": (
            "📢 <b>Kanal qo'shish</b>\n\n"
            "<b>Kanal ID</b> raqamini yuboring (masalan <code>-1001234567890</code>)\n\n"
            "💡 ID bilish: @getmyid_bot ni kanalga qo'shing"
        ),
    },
    "admin.add_channel_title": {
        "ru": "✏️ Теперь отправь <b>название канала</b> (для отображения юзеру):",
        "uz": "✏️ Endi <b>kanal nomini</b> yuboring (foydalanuvchiga ko'rsatiladi):",
    },
    "admin.add_channel_link": {
        "ru": (
            "🔗 Теперь отправь <b>ссылку или юзернейм канала</b>\n\n"
            "Принимаю любой формат:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "uz": (
            "🔗 Endi <b>kanal havolasi yoki username</b> yuboring\n\n"
            "Istalgan formatda:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
    },
    "admin.channel_added": {
        "ru": "✅ <b>Канал добавлен!</b>",
        "uz": "✅ <b>Kanal qo'shildi!</b>",
    },
    "admin.confirm_delete": {
        "ru": "⚠️ <b>Удалить канал?</b>\n\nID: <code>{channel_id}</code>\n\nЭто действие нельзя отменить.",
        "uz": "⚠️ <b>Kanalni o'chirishni xohlaysizmi?</b>\n\nID: <code>{channel_id}</code>\n\nBu amalni qaytarib bo'lmaydi.",
    },
    "admin.id_not_number": {
        "ru": "❌ ID должен быть числом. Попробуй ещё раз:",
        "uz": "❌ ID raqam bo'lishi kerak. Qayta urinib ko'ring:",
    },
    "admin.title_too_long": {
        "ru": "❌ Название слишком длинное (макс 200 символов)",
        "uz": "❌ Nom juda uzun (maks 200 belgi)",
    },
    "admin.link_invalid": {
        "ru": "❌ Не удалось распознать ссылку.\nПопробуй ещё:",
        "uz": "❌ Havolani aniqlab bo'lmadi.\nQayta urinib ko'ring:",
    },
    "btn.admin_stats": {
        "ru": "📊 Статистика",
        "uz": "📊 Statistika",
    },
    "btn.admin_channels": {
        "ru": "📢 Каналы",
        "uz": "📢 Kanallar",
    },
    "btn.admin_home": {
        "ru": "🏠 Главное меню",
        "uz": "🏠 Bosh menyu",
    },
    "btn.admin_add": {
        "ru": "➕ Добавить канал",
        "uz": "➕ Kanal qo'shish",
    },
    "btn.admin_back": {
        "ru": "◀️ Назад",
        "uz": "◀️ Orqaga",
    },
    "btn.admin_cancel": {
        "ru": "❌ Отмена",
        "uz": "❌ Bekor qilish",
    },
    "btn.admin_confirm_del": {
        "ru": "✅ Да, удалить",
        "uz": "✅ Ha, o'chirish",
    },
    "btn.admin_cancel_del": {
        "ru": "❌ Отмена",
        "uz": "❌ Bekor qilish",
    },
    "btn.admin_panel": {
        "ru": "🔧 Админ-панель",
        "uz": "🔧 Admin panel",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить перевод по ключу и языку"""
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang, translations.get("ru", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text


def detect_language(language_code: str | None) -> str:
    """Определяет язык по коду из Telegram: ru → русский, остальные → узбекский"""
    if language_code and language_code.startswith("ru"):
        return "ru"
    return "uz"

