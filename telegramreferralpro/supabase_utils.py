import logging
import aiohttp
from typing import Optional, Dict, Any

from .config import BotConfig

logger = logging.getLogger(__name__)

async def send_task_update_to_supabase(
    config: BotConfig,
    telegram_id: int,
    task_key: str,
    status: str,
    meta: Optional[Dict[str, Any]] = None
) -> None:
    """
    Sends a task update to the configured Supabase Edge Function.

    Args:
        config: The bot's configuration object.
        telegram_id: The user's Telegram ID.
        task_key: A unique key for the task (e.g., "tg_referral_5").
        status: The status of the task (e.g., "completed").
        meta: Optional dictionary with additional metadata.
    """
    if not config.supabase_webhook_url or not config.supabase_webhook_secret:
        logger.info("Supabase webhook URL or secret not configured. Skipping update.")
        return

    headers = {
        "Content-Type": "application/json",
        "x-bot-secret": config.supabase_webhook_secret,
    }
    body = {"telegramId": telegram_id, "taskKey": task_key, "status": status, "meta": meta or {}}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(config.supabase_webhook_url, json=body, headers=headers) as response:
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                logger.info(f"Successfully sent task update to Supabase for user {telegram_id}. Status: {response.status}")
    except aiohttp.ClientError as e:
        logger.error(f"Error sending task update to Supabase for user {telegram_id}: {e}")