"""Сервис скачивания Instagram — yt-dlp для видео, aiohttp для фото"""
import asyncio
import logging
import os
import re
import tempfile
from dataclasses import dataclass

import aiohttp
import yt_dlp

logger = logging.getLogger(__name__)


@dataclass
class DownloadResult:
    """Результат скачивания"""
    file_path: str       # путь к файлу
    media_type: str      # video, photo
    title: str           # название поста
    duration: int | None  # длительность в секундах (для видео)
    thumbnail: str | None  # путь к превью


class InstagramDownloader:
    """Скачивает контент из Instagram — видео через yt-dlp, фото через aiohttp"""

    def __init__(self):
        # папка для временных файлов
        self.download_dir = tempfile.mkdtemp(prefix="insta_bot_")

    def _get_yt_dlp_options(self, output_path: str) -> dict:
        """Настройки yt-dlp для скачивания видео"""
        return {
            "outtmpl": output_path,
            "format": "best[ext=mp4]/best",
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            "max_filesize": 50 * 1024 * 1024,
            "noplaylist": True,
            "writethumbnail": True,
            "socket_timeout": 30,
        }

    async def download(self, url: str) -> DownloadResult:
        """Скачивает медиа по ссылке Instagram (сначала yt-dlp, потом фото)"""
        # сначала пробуем через yt-dlp (для видео/reels)
        try:
            result = await self._download_video(url)
            if result:
                return result
        except Exception as e:
            logger.info(f"yt-dlp не смог скачать {url}: {e}")

        # если yt-dlp не справился — пробуем скачать как фото
        try:
            result = await self._download_photo(url)
            if result:
                return result
        except Exception as e:
            logger.error(f"Фото тоже не удалось: {e}")

        raise FileNotFoundError("Не удалось скачать медиа. Проверь ссылку.")

    async def _download_video(self, url: str) -> DownloadResult | None:
        """Скачивает видео через yt-dlp"""
        output_path = os.path.join(self.download_dir, "%(id)s.%(ext)s")
        opts = self._get_yt_dlp_options(output_path)

        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, self._yt_dlp_sync, url, opts)

        # если это фото-пост — yt-dlp вернёт пустой playlist
        if info.get("_type") == "playlist" and not info.get("entries"):
            return None

        file_path = self._find_downloaded_file(info)
        if not file_path or not os.path.exists(file_path):
            return None

        # определяем тип медиа
        ext = os.path.splitext(file_path)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".webp"):
            media_type = "photo"
        else:
            media_type = "video"

        return DownloadResult(
            file_path=file_path,
            media_type=media_type,
            title=info.get("title", "Instagram"),
            duration=info.get("duration"),
            thumbnail=None,
        )

    async def _download_photo(self, url: str) -> DownloadResult | None:
        """Скачивает фото через Instagram embed API"""
        # получаем URL фото через oEmbed API
        oembed_url = f"https://api.instagram.com/oembed/?url={url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(oembed_url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    logger.warning(f"oEmbed вернул {resp.status}")
                    return None
                data = await resp.json()

        thumbnail_url = data.get("thumbnail_url")
        title = data.get("title", "Instagram")

        if not thumbnail_url:
            logger.warning("oEmbed не вернул thumbnail_url")
            return None

        # скачиваем фото
        post_id = url.rstrip("/").split("/")[-1]
        file_path = os.path.join(self.download_dir, f"{post_id}.jpg")

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail_url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return None
                content = await resp.read()
                with open(file_path, "wb") as f:
                    f.write(content)

        logger.info(f"Фото скачано: {file_path} ({len(content)} байт)")

        return DownloadResult(
            file_path=file_path,
            media_type="photo",
            title=title,
            duration=None,
            thumbnail=None,
        )

    def _find_downloaded_file(self, info: dict) -> str:
        """Ищет скачанный файл разными способами"""
        # способ 1: из requested_downloads
        downloads = info.get("requested_downloads", [])
        if downloads and downloads[0].get("filepath"):
            return downloads[0]["filepath"]

        # способ 2: собираем путь из id и ext
        video_id = info.get("id", "")
        ext = info.get("ext", "mp4")
        if video_id:
            candidate = os.path.join(self.download_dir, f"{video_id}.{ext}")
            if os.path.exists(candidate):
                return candidate

        # способ 3: ищем самый свежий файл в папке
        files = []
        for f in os.listdir(self.download_dir):
            full = os.path.join(self.download_dir, f)
            if os.path.isfile(full) and not f.endswith((".json", ".txt")):
                files.append((os.path.getmtime(full), full))

        if files:
            files.sort(reverse=True)
            return files[0][1]

        return ""

    def _yt_dlp_sync(self, url: str, opts: dict) -> dict:
        """Синхронная обёртка yt-dlp"""
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=True)

    def cleanup(self, result: DownloadResult) -> None:
        """Удаляет временные файлы после отправки"""
        try:
            if os.path.exists(result.file_path):
                os.remove(result.file_path)
                logger.info(f"Удалён: {result.file_path}")
            if result.thumbnail and os.path.exists(result.thumbnail):
                os.remove(result.thumbnail)
        except OSError as e:
            logger.warning(f"Не удалось удалить файл: {e}")


# глобальный экземпляр
downloader = InstagramDownloader()
