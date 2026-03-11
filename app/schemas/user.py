from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    strava_athlete_id: int | None = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str