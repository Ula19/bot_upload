"""Сервис скачивания Instagram Stories — через private API + sessionid"""
import logging
import os
import re
import tempfile

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


async def get_user_id(session: aiohttp.ClientSession, username: str) -> str:
    """Получает user_id по username через private API"""
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    cookies = {"sessionid": settings.instagram_session_id}

    async with session.get(
        url, headers=INSTAGRAM_HEADERS, cookies=cookies,
        timeout=aiohttp.ClientTimeout(total=10),
    ) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Не удалось получить профиль @{username}: HTTP {resp.status}")
        data = await resp.json()

    user = data.get("data", {}).get("user", {})
    user_id = user.get("id")
    if not user_id:
        raise RuntimeError(f"Пользователь @{username} не найден")

    logger.info(f"@{username} → user_id={user_id}")
    return user_id


async def get_story_media(
    session: aiohttp.ClientSession, user_id: str, story_id: str
) -> dict:
    """Получает медиа конкретной истории"""
    url = f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={user_id}"
    cookies = {"sessionid": settings.instagram_session_id}

    async with session.get(
        url, headers=INSTAGRAM_HEADERS, cookies=cookies,
        timeout=aiohttp.ClientTimeout(total=10),
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

    # если конкретный ID не нашли — возвращаем по индексу (фоллбэк)
    logger.warning(f"Story {story_id} не найден, отправляем последнюю")
    return items[-1]


async def download_story(url: str, download_dir: str) -> dict:
    """Скачивает историю и возвращает {file_path, media_type}"""
    if not settings.instagram_session_id:
        raise RuntimeError(
            "Для скачивания Stories нужна авторизация.\n"
            "Администратор должен добавить INSTAGRAM_SESSION_ID в .env"
        )

    username, story_id = parse_story_url(url)

    async with aiohttp.ClientSession() as session:
        # получаем user_id
        user_id = await get_user_id(session, username)

        # получаем медиа истории
        item = await get_story_media(session, user_id, story_id)

        # определяем тип и URL медиа
        media_type = "video" if item.get("video_versions") else "photo"

        if media_type == "video":
            # берём лучшее качество (первый элемент)
            versions = item["video_versions"]
            media_url = versions[0]["url"]
            ext = ".mp4"
        else:
            # фото — берём лучшее качество
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
