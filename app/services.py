# app/services.py
import httpx
from app.config import settings

async def send_telegram_message(chat_id: int, text: str) -> bool:
    """Sends a message to a user via the Telegram Bot API."""
    url = f"{settings.telegram_api_url}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        return response.status_code == 200