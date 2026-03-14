"""Сервис скачивания Instagram — через yt-dlp"""
import asyncio
import logging
import os
import tempfile
from dataclasses import dataclass

import yt_dlp

logger = logging.getLogger(__name__)


@dataclass
class DownloadResult:
    """Результат скачивания"""
    file_path: str       # путь к файлу
    media_type: str      # video, photo
    title: str           # название поста
    duration: int | None # длительность в секундах (для видео)
    thumbnail: str | None  # путь к превью


class InstagramDownloader:
    """Скачивает контент из Instagram через yt-dlp"""

    def __init__(self):
        # папка для временных файлов
        self.download_dir = tempfile.mkdtemp(prefix="insta_bot_")

    def _get_yt_dlp_options(self, output_path: str) -> dict:
        """Настройки yt-dlp для скачивания"""
        return {
            "outtmpl": output_path,
            "format": "best[ext=mp4]/best",  # лучшее качество в mp4
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            # ограничение размера файла (50 МБ — лимит Telegram)
            "max_filesize": 50 * 1024 * 1024,
            # не скачивать плейлисты целиком
            "noplaylist": True,
            # пишем превью
            "writethumbnail": True,
            # таймаут
            "socket_timeout": 30,
        }

    async def download(self, url: str) -> DownloadResult:
        """Скачивает медиа по ссылке Instagram (асинхронно)"""
        # генерим уникальное имя файла
        output_path = os.path.join(self.download_dir, "%(id)s.%(ext)s")
        opts = self._get_yt_dlp_options(output_path)

        # yt-dlp синхронный — запускаем в отдельном потоке
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, self._download_sync, url, opts)

        # определяем путь и тип
        file_path = info.get("requested_downloads", [{}])[0].get("filepath", "")
        duration = info.get("duration")

        # ищем превью
        thumbnail_path = None
        thumb_candidates = [
            file_path.rsplit(".", 1)[0] + ".jpg",
            file_path.rsplit(".", 1)[0] + ".webp",
            file_path.rsplit(".", 1)[0] + ".png",
        ]
        for thumb in thumb_candidates:
            if os.path.exists(thumb):
                thumbnail_path = thumb
                break

        # определяем тип медиа
        ext = os.path.splitext(file_path)[1].lower()
        if ext in (".mp4", ".webm", ".mkv", ".mov"):
            media_type = "video"
        elif ext in (".jpg", ".jpeg", ".png", ".webp"):
            media_type = "photo"
        else:
            media_type = "video"  # по умолчанию

        return DownloadResult(
            file_path=file_path,
            media_type=media_type,
            title=info.get("title", "Instagram"),
            duration=duration,
            thumbnail=thumbnail_path,
        )

    def _download_sync(self, url: str, opts: dict) -> dict:
        """Синхронная обёртка yt-dlp (для run_in_executor)"""
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info

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
