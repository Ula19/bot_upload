"""Сервис скачивания Instagram Stories — через private API + sessionid
Поддерживает прокси (INSTAGRAM_PROXY) для обхода блокировки IP.
"""
import asyncio
import logging
import os
import re

import aiohttp

from bot.config import settings

logger = logging.getLogger(__name__)

# Instagram private API — мобильные заголовки
INSTAGRAM_HEADERS = {
    "User-Agent": "Instagram 275.0.0.27.98 Android (33/13; 420dpi; 1080x2400; samsung; SM-G991B; o1s; exynos2100)",
    "X-IG-App-ID": "936619743392459",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
}


def parse_story_url(url: str) -> tuple[str, str]:
    """Извлекает username и story_id из URL истории
    URL формат: https://www.instagram.com/stories/username/story_id/
    """
    match = re.search(r"stories/([^/]+)/(\d+)", url)
    if not match:
        raise ValueError(f"Не удалось распарсить URL истории: {url}")
    return match.group(1), match.group(2)


def is_story_url(url: str) -> bool:
    """Проверяет, является ли URL ссылкой на историю"""
    return bool(re.search(r"instagram\.com/stories/[^/]+/\d+", url))


# кэш user_id чтобы не запрашивать повторно
_user_id_cache: dict[str, str] = {}


def _get_proxy() -> str | None:
    """Возвращает прокси или None"""
    return settings.instagram_proxy or None


async def get_user_id(session: aiohttp.ClientSession, username: str) -> str:
    """Получает user_id по username через private API (с ретраем при 429)"""
    if username in _user_id_cache:
        logger.info(f"@{username} → user_id={_user_id_cache[username]} (кэш)")
        return _user_id_cache[username]

    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    cookies = {"sessionid": settings.instagram_session_id}
    proxy = _get_proxy()

    # ретрай при 429
    max_retries = 2
    delays = [5, 10]

    for attempt in range(max_retries + 1):
        async with session.get(
            url, headers=INSTAGRAM_HEADERS, cookies=cookies,
            timeout=aiohttp.ClientTimeout(total=10),
            proxy=proxy,
        ) as resp:
            if resp.status == 429:
                if attempt < max_retries:
                    delay = delays[attempt]
                    logger.warning(f"429 от Instagram, ждём {delay}с (попытка {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)
                    continue
                raise RuntimeError(
                    "Instagram блокирует запросы (429).\n"
                    "Нужен резидентный прокси — добавь INSTAGRAM_PROXY в .env"
                )
            if resp.status != 200:
                raise RuntimeError(f"Не удалось получить профиль @{username}: HTTP {resp.status}")
            data = await resp.json()
            break

    user = data.get("data", {}).get("user", {})
    user_id = user.get("id")
    if not user_id:
        raise RuntimeError(f"Пользователь @{username} не найден")

    _user_id_cache[username] = user_id
    logger.info(f"@{username} → user_id={user_id}")
    return user_id


async def get_story_media(
    session: aiohttp.ClientSession, user_id: str, story_id: str
) -> dict:
    """Получает медиа конкретной истории"""
    url = f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={user_id}"
    cookies = {"sessionid": settings.instagram_session_id}
    proxy = _get_proxy()

    async with session.get(
        url, headers=INSTAGRAM_HEADERS, cookies=cookies,
        timeout=aiohttp.ClientTimeout(total=10),
        proxy=proxy,
    ) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Не удалось получить истории: HTTP {resp.status}")
        data = await resp.json()

    reels = data.get("reels", {})
    reel = reels.get(user_id, {})
    items = reel.get("items", [])

    if not items:
        raise RuntimeError("Истории не найдены или уже истекли (24 часа)")

    # ищем конкретную историю по story_id
    for item in items:
        if str(item.get("pk")) == story_id or str(item.get("id", "")).startswith(story_id):
            return item

    # фоллбэк — последняя история
    logger.warning(f"Story {story_id} не найден, отправляем последнюю")
    return items[-1]


async def download_story(url: str, download_dir: str) -> dict:
    """Скачивает историю и возвращает {file_path, media_type}"""
    if not settings.instagram_session_id:
        raise RuntimeError(
            "Для скачивания Stories нужна авторизация.\n"
            "Добавь INSTAGRAM_SESSION_ID в .env"
        )

    username, story_id = parse_story_url(url)
    proxy = _get_proxy()
    logger.info(f"Stories: user=@{username}, proxy={'да' if proxy else 'нет'}")

    async with aiohttp.ClientSession() as session:
        # получаем user_id
        user_id = await get_user_id(session, username)

        # получаем медиа истории
        item = await get_story_media(session, user_id, story_id)

        # определяем тип и URL медиа
        media_type = "video" if item.get("video_versions") else "photo"

        if media_type == "video":
            versions = item["video_versions"]
            media_url = versions[0]["url"]
            ext = ".mp4"
        else:
            candidates = item.get("image_versions2", {}).get("candidates", [])
            if not candidates:
                raise RuntimeError("Не удалось найти фото в истории")
            media_url = candidates[0]["url"]
            ext = ".jpg"

        # скачиваем файл
        file_path = os.path.join(download_dir, f"story_{username}_{story_id}{ext}")

        async with session.get(
            media_url, timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Не удалось скачать медиа: HTTP {resp.status}")
            content = await resp.read()

            if len(content) > 50 * 1024 * 1024:
                raise RuntimeError("Файл больше 50 МБ — лимит Telegram")

            with open(file_path, "wb") as f:
                f.write(content)

        size_mb = len(content) / (1024 * 1024)
        logger.info(f"Story скачана: {file_path} ({size_mb:.1f} МБ, {media_type})")

        return {
            "file_path": file_path,
            "media_type": media_type,
            "title": f"Story @{username}",
        }
