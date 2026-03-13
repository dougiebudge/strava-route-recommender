from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = ""
    secret_key: str = ""
    strava_client_id: str = ""
    strava_client_secret: str = ""
    strava_redirect_uri: str = "http://localhost:8000/strava/callback"

    class Config:
        env_file = ".env"

settings = Settings()