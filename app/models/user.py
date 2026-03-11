from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    strava_athelete_id = Column(Integer, unique=True, nullable=True)
    strava_access_token = Column(String, nullable=True)
    strava_refresh_token = Column(String, nullable=True)

    # derived fields
    avg_distance_km = Column(Float, nullable=True)
    avg_elevation_m = Column(Float, nullable=True)
    preffered_pace_min_km = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    

