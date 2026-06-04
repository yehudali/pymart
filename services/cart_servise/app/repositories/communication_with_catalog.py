from app.core.config import settings
import httpx

CATALOG_SERVICE_URL = settings.CATALOG_SERVICE_URL


async def send_order_to_catalog(payload: list[dict]) -> bool:
    """מתקשרת מול סרוויס הקטלוג ומוודאת שהבקשה הצליחה"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CATALOG_SERVICE_URL}/create_order", json=payload
        )

        response.raise_for_status()
        return True
