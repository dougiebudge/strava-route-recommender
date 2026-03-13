from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import logging

from app.models.database import get_db
from app.models.user import User
from app.services.dependencies import get_current_user
from app.services import strava as strava_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/strava", tags=["strava"])

@router.get("/connect")
def connect_strava(current_user: User = Depends(get_current_user)):
    """
    Returns the Strava authorization URL.
    Frontend should redirect user to this URL.
    """
    auth_url = strava_service.get_authorization_url()
    return {"authorization_url": auth_url}

@router.get("/callback")
async def strava_callback(
    code: str = Query(...),
    scope: str = Query(default=""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Strava redirects here after user authorizes
    Exchanges code for tokens and saves to user record
    """
    try: 
        token_data = await strava_service.exchange_code_for_tokens(code)
    except Exception as e:
        logger.error(f"Failed to exchange Strava code: {e}")
        raise HTTPException(status_code=400, detail="Failed to connect to Strava")

    # Save tokens to user
    current_user.strava_athlete_id = token_data["athlete"]["id"]
    current_user.strava_access_token = token_data["access_token"]
    current_user.strava_refresh_token = token_data["refresh_token"]
    current_user.strava_token_expires_at = token_data["expires_at"]
    db.commit()

    return {
        "message": "Strava connected successfully",
        "athlete_id": token_data["athlete"]["id"],
        "athlete_name": token_data["athlete"].get("firstname", ""),
    }

@router.get("/activities")
async def get_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Fetch and return the user's recent activities from Strava
    """
    if not current_user.strava_access_token:
        raise HTTPException(
            status_code=400,
            detail="Strava account not connected. Visit /strava/connect first."
        )

    try:
        access_token = await strava_service.get_valid_access_token(current_user, db)
        activities = await strava_service.get_athlete_activities(access_token)
        return {"count": len(activities), "activities": activities}
    except Exception as e:
        logger.error(f"Failed to fetch Strava activities for user {current_user.id}: {e}")
        raise HTTPException(status_code=502, detail="Failed to fetch activities from Strava")
