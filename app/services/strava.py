import httpx
import time
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_API_BASE = "https://www.strava.com/api/v3"

def get_authorization_url() -> str:
    """Generate tge Strava Oauth Authorization URL"""
    params = {
        "client_id": settings.strava_client_id,
        "redirect_uri": settings.strava_redirect_uri,
        "response_type": "code",
        "scope": "activity:read_all",
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{STRAVA_AUTH_URL}?{query_string}"

async def exchange_code_for_tokens(code: str) -> dict:
    """Exchange the Strava Oauth code for a token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            STRAVA_TOKEN_URL,
            data={
                "client_id": settings.strava_client_id,
                "client_secret": settings.strava_client_secret,
                "code": code,
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        return response.json()

async def refresh_access_token(refresh_token: str) -> dict:
    """Refresh the Strava access token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            STRAVA_TOKEN_URL,
            data={
                "client_id": settings.strava_client_id,
                "client_secret": settings.strava_client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )
        response.raise_for_status()
        return response.json()

async def get_valid_access_token(user: User, db: Session) -> str:
    """Return a valid access token for the user"""
    # Check if token expired with 60s buffer
    if user.strava_token_expires_at and user.strava_token_expires_at < (time.time() + 60):
        token_data = await refresh_access_token(user.strava_refresh_token)

        user.strava_access_token = token_data["access_token"]
        user.strava_refresh_token = token_data["refresh_token"]
        user.strava_token_expires_at = token_data["expires_at"]
        db.commit()

    return user.strava_access_token

async def get_athlete_activities(access_token: str, per_page: int = 30) -> list:
    """ Fetch recent activities from Strava"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{STRAVA_API_BASE}/athlete/activities",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "per_page": per_page,
            },
        )
        response.raise_for_status()
        return response.json()
