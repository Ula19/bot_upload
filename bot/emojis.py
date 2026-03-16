"""Премиум-эмоджи из пака tgmacicons
E_ID — чистые ID для кнопок (icon_custom_emoji_id)
E — HTML-теги для текстов сообщений
"""

# ID для InlineKeyboardButton(icon_custom_emoji_id=...)
E_ID = {
    "download":  "5258336354642697821",
    "profile":   "5258362837411045098",
    "book":      "5258328383183396223",
    "star":      "5258185631355378853",
    "folder":    "5258514780469075716",
    "cross":     "5258226313285607065",
    "check":     "5260726538302660868",
    "megaphone": "5260268501515377807",
    "camera":    "5258205968025525531",
    "link":      "5260730055880876557",
    "lock":      "5258476306152038031",
    "clock":     "5258258882022612173",
    "chart":     "5258391025281408576",
    "gear":      "5258096772776991776",
    "home":      "5257963315258204021",
    "plus":      "5258108352008823107",
    "plane":     "5258115571848846212",
    "pin":       "5258461531464539536",
    "video":     "5258077307985207053",
    "users":     "5258513401784573443",
    "info":      "5258503720928288433",
    "bulb":      "5258216851472654189",
    "warning":   "5258474669769497337",
    "back":      "5258236805890710909",
    "package":   "5258134813302332906",
    "edit":      "5258331647358540449",
    "bot":       "5258093637450866522",
    "refresh":   "5258420634785947640",
    "eye":       "5253959125838090076",
    "search":    "5429571366384842791",
    "trash":     "5258130763148172425",
    "globe":     "5258212268742549391",
    "flag_ru":   "5398017006165305287",
    "flag_uz":   "5445378486711623503",
    "flag_gb":   "5458416160586342331",
}


def _tag(name: str, fallback: str) -> str:
    """Собирает HTML-тег для текстов сообщений"""
    return f'<tg-emoji emoji-id="{E_ID[name]}">{fallback}</tg-emoji>'


# HTML-теги для текстов сообщений (parse_mode="HTML")
E = {
    "download":  _tag("download", "⬇️"),
    "profile":   _tag("profile", "👤"),
    "book":      _tag("book", "📖"),
    "star":      _tag("star", "⭐️"),
    "folder":    _tag("folder", "📂"),
    "cross":     _tag("cross", "❌"),
    "check":     _tag("check", "✅"),
    "megaphone": _tag("megaphone", "📣"),
    "camera":    _tag("camera", "📸"),
    "link":      _tag("link", "⛓"),
    "lock":      _tag("lock", "🔒"),
    "clock":     _tag("clock", "⏲"),
    "chart":     _tag("chart", "📈"),
    "gear":      _tag("gear", "⚙"),
    "home":      _tag("home", "🏘"),
    "plus":      _tag("plus", "➕"),
    "plane":     _tag("plane", "✈️"),
    "pin":       _tag("pin", "📌"),
    "video":     _tag("video", "📹"),
    "users":     _tag("users", "👥"),
    "info":      _tag("info", "ℹ️"),
    "bulb":      _tag("bulb", "💡"),
    "warning":   _tag("warning", "❗️"),
    "back":      _tag("back", "⬅️"),
    "package":   _tag("package", "📦"),
    "edit":      _tag("edit", "✍️"),
    "bot":       _tag("bot", "🤖"),
    "refresh":   _tag("refresh", "🔄"),
    "eye":       _tag("eye", "👁"),
    "search":    _tag("search", "🔎"),
    "trash":     _tag("trash", "🗑"),
    "globe":     _tag("globe", "🌠"),
}
