from app.core.config import settings
import httpx


async def get_email_by_token(token: str) -> str:

    query_params = {"token": token}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.USER_MANAGEMENT_URL}/profile", params=query_params
        )
        response.raise_for_status()

        data = response.json()

        email = data.get("email")
        if not email:
            error_msg = f"Failed to receive user email from: {data}"
            print(error_msg)
            raise KeyError(error_msg)

        return email
