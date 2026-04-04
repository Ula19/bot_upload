"""Уведомление администраторов бота"""
import logging

from aiogram import Bot

from bot.config import settings

logger = logging.getLogger(__name__)


async def notify_admins(bot: Bot, text: str) -> None:
    """Отправляет сообщение всем админам из ADMIN_IDS"""
    if not settings.admin_id_list:
        logger.warning("Список ADMIN_IDS пуст — некому отправить уведомление")
        return

    for admin_id in settings.admin_id_list:
        try:
            await bot.send_message(admin_id, text)
            logger.info(f"Уведомление отправлено админу {admin_id}")
        except Exception as e:
            logger.error(f"Не удалось уведомить админа {admin_id}: {e}")
