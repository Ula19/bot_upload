"""CRUD операции с базой данных"""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Channel, Download, User


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
    full_name: str,
) -> User:
    """Получить юзера или создать нового"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def get_user_language(session: AsyncSession, telegram_id: int) -> str:
    """Получить язык юзера (по умолчанию ru)"""
    result = await session.execute(
        select(User.language).where(User.telegram_id == telegram_id)
    )
    lang = result.scalar_one_or_none()
    return lang or "ru"


async def update_user_language(
    session: AsyncSession, telegram_id: int, language: str
) -> None:
    """Обновить язык юзера"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    if user:
        user.language = language
        await session.commit()

async def get_active_channels(session: AsyncSession) -> list[Channel]:
    """Получить все каналы для обязательной подписки"""
    result = await session.execute(select(Channel))
    return list(result.scalars().all())


async def get_cached_download(
    session: AsyncSession, instagram_url: str
) -> Download | None:
    """Получить кэш по ссылке, если не протух"""
    result = await session.execute(
        select(Download).where(
            Download.instagram_url == instagram_url,
            Download.expires_at > datetime.now(),
        )
    )
    download = result.scalar_one_or_none()

    # обновляем счетчик если кэш найден
    if download:
        download.download_count += 1
        await session.commit()

    return download


async def save_download(
    session: AsyncSession,
    instagram_url: str,
    file_id: str,
    media_type: str,
) -> Download:
    """Сохранить скачанный файл в кэш"""
    # может уже быть запись с протухшим кэшем — обновим её
    result = await session.execute(
        select(Download).where(Download.instagram_url == instagram_url)
    )
    download = result.scalar_one_or_none()

    if download:
        download.file_id = file_id
        download.media_type = media_type
        download.created_at = datetime.now()
        download.download_count += 1
        from datetime import timedelta
        download.expires_at = datetime.now() + timedelta(days=30)
    else:
        download = Download(
            instagram_url=instagram_url,
            file_id=file_id,
            media_type=media_type,
        )
        session.add(download)

    await session.commit()
    return download


# === Админские функции ===

async def add_channel(
    session: AsyncSession,
    channel_id: int,
    title: str,
    invite_link: str,
) -> Channel:
    """Добавить канал для обязательной подписки"""
    # проверяем нет ли уже
    result = await session.execute(
        select(Channel).where(Channel.channel_id == channel_id)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError(f"Канал {channel_id} уже добавлен")

    channel = Channel(
        channel_id=channel_id,
        title=title,
        invite_link=invite_link,
    )
    session.add(channel)
    await session.commit()
    await session.refresh(channel)
    return channel


async def remove_channel(session: AsyncSession, channel_id: int) -> bool:
    """Удалить канал. Возвращает True если удалён"""
    result = await session.execute(
        select(Channel).where(Channel.channel_id == channel_id)
    )
    channel = result.scalar_one_or_none()
    if not channel:
        return False

    await session.delete(channel)
    await session.commit()
    return True


async def get_user_stats(session: AsyncSession) -> dict:
    """Статистика: всего юзеров, за сегодня, скачиваний"""
    from sqlalchemy import func as sa_func

    # всего юзеров
    total = await session.execute(select(sa_func.count(User.id)))
    total_users = total.scalar() or 0

    # за сегодня
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_result = await session.execute(
        select(sa_func.count(User.id)).where(User.created_at >= today)
    )
    today_users = today_result.scalar() or 0

    # всего скачиваний
    downloads = await session.execute(
        select(sa_func.sum(User.download_count))
    )
    total_downloads = downloads.scalar() or 0

    # каналов
    channels = await session.execute(select(sa_func.count(Channel.id)))
    total_channels = channels.scalar() or 0

    return {
        "total_users": total_users,
        "today_users": today_users,
        "total_downloads": total_downloads,
        "total_channels": total_channels,
    }
