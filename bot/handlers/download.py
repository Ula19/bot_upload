"""Хэндлер скачивания — обрабатывает ссылки Instagram"""
import logging
import os

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.database import async_session
from bot.database.crud import get_cached_download, get_or_create_user, save_download
from bot.keyboards.inline import get_back_keyboard
from bot.services.instagram import DownloadResult, downloader
from bot.services.stories import download_story, is_story_url
from bot.utils.helpers import clean_instagram_url, is_instagram_url

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text)
async def handle_instagram_link(message: Message) -> None:
    """Обработка текстовых сообщений — ищем ссылки Instagram"""
    text = message.text.strip()

    # проверяем что это ссылка на инсту
    if not is_instagram_url(text):
        await message.answer(
            "🤔 Это не похоже на ссылку Instagram.\n\n"
            "Отправь ссылку в формате:\n"
            "<code>https://www.instagram.com/reel/...</code>\n"
            "<code>https://www.instagram.com/p/...</code>\n"
            "<code>https://www.instagram.com/stories/...</code>",
            parse_mode="HTML",
        )
        return

    # очищаем URL
    clean_url = clean_instagram_url(text)

    # обновляем юзера в БД
    async with async_session() as session:
        user = await get_or_create_user(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )

        # проверяем кэш — может уже скачивали
        cached = await get_cached_download(session, clean_url)

    if cached:
        # отправляем из кэша — мгновенно!
        logger.info(f"Кэш найден для {clean_url}, отправляем file_id")
        await _send_cached(message, cached.file_id, cached.media_type)
        return

    # кэша нет — скачиваем
    status_msg = await message.answer("⏳ Скачиваю... Подожди немного")

    result = None
    story_data = None
    try:
        # выбираем метод: Stories или Cobalt
        if is_story_url(clean_url):
            story_data = await download_story(clean_url, downloader.download_dir)
            # оборачиваем в DownloadResult для единообразия
            result = DownloadResult(
                file_path=story_data["file_path"],
                media_type=story_data["media_type"],
                title=story_data["title"],
            )
        else:
            result = await downloader.download(clean_url)

        # проверяем размер файла (Telegram лимит 50 МБ)
        file_size = os.path.getsize(result.file_path)
        if file_size > 50 * 1024 * 1024:
            await status_msg.edit_text(
                "❌ Файл слишком большой (более 50 МБ).\n"
                "Telegram не позволяет отправлять такие файлы."
            )
            return

        # отправляем и получаем file_id
        file_id = await _send_media(message, result)

        # сохраняем в кэш
        if file_id:
            async with async_session() as session:
                await save_download(
                    session=session,
                    instagram_url=clean_url,
                    file_id=file_id,
                    media_type=result.media_type,
                )
                # обновляем счётчик скачиваний юзера
                user_obj = await get_or_create_user(
                    session=session,
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    full_name=message.from_user.full_name,
                )
                user_obj.download_count += 1
                await session.commit()

        # удаляем сообщение "Скачиваю..."
        await status_msg.delete()

    except Exception as e:
        logger.error(f"Ошибка скачивания {clean_url}: {e}")
        error_text = _get_error_text(str(e))
        await status_msg.edit_text(error_text)

    finally:
        # чистим временные файлы
        if result:
            downloader.cleanup(result)


async def _send_media(message: Message, result: DownloadResult) -> str | None:
    """Отправляет медиа юзеру и возвращает file_id"""
    file = FSInputFile(result.file_path)

    if result.media_type == "video":
        sent = await message.answer_video(
            video=file,
            caption=f"🎬 {result.title}" if result.title else None,
            duration=int(result.duration) if result.duration else None,
        )
        return sent.video.file_id

    elif result.media_type == "photo":
        sent = await message.answer_photo(
            photo=file,
            caption=f"📸 {result.title}" if result.title else None,
        )
        # у фото file_id в последнем элементе массива (макс. размер)
        return sent.photo[-1].file_id

    return None


async def _send_cached(
    message: Message, file_id: str, media_type: str
) -> None:
    """Отправляет из кэша по file_id — мгновенно"""
    try:
        if media_type == "video":
            await message.answer_video(video=file_id, caption="🎬 Из кэша ⚡")
        elif media_type == "photo":
            await message.answer_photo(photo=file_id, caption="📸 Из кэша ⚡")
    except Exception as e:
        logger.error(f"Ошибка отправки из кэша: {e}")
        # кэш протух — удалим и скажем юзеру переотправить
        await message.answer("⚠️ Кэш устарел. Отправь ссылку ещё раз.")


def _get_error_text(error: str) -> str:
    """Человеко-понятное сообщение об ошибке"""
    error_lower = error.lower()

    if "session" in error_lower and "авторизация" in error_lower:
        return (
            "🔑 <b>Нужна авторизация</b>\n\n"
            "Для скачивания Stories нужен INSTAGRAM_SESSION_ID."
        )
    elif "истории не найдены" in error_lower or "истекли" in error_lower:
        return (
            "⏰ <b>История не найдена</b>\n\n"
            "Возможно, она уже истекла (24 часа) или аккаунт приватный."
        )
    elif "private" in error_lower or "login" in error_lower:
        return (
            "🔒 <b>Аккаунт приватный</b>\n\n"
            "К сожалению, скачивание из приватных аккаунтов невозможно."
        )
    elif "not found" in error_lower or "404" in error_lower:
        return (
            "❌ <b>Пост не найден</b>\n\n"
            "Возможно, он удалён или ссылка неправильная."
        )
    elif "unsupported" in error_lower:
        return (
            "🚫 <b>Ссылка не поддерживается</b>\n\n"
            "Поддерживаются: посты, Reels и Stories."
        )
    elif "too large" in error_lower or "50 мб" in error_lower:
        return (
            "📦 <b>Файл слишком большой</b>\n\n"
            "Telegram ограничивает размер файла до 50 МБ."
        )
    elif "timeout" in error_lower:
        return (
            "⏱ <b>Превышено время ожидания</b>\n\n"
            "Попробуй ещё раз через пару минут."
        )
    else:
        return (
            "❌ <b>Не удалось скачать</b>\n\n"
            "Попробуй позже или проверь ссылку."
        )
