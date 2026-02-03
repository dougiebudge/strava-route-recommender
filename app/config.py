from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://strava_user:localdev123@localhost:5433/strava_routes"
    secret_key: str = "dev-secret-change-in-production"
    strava_client_id: str = ""
    strava_client_secret: str = ""

    class Config:
        env_file = ".env"

settings = Settings()