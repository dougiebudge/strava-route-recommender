from fastapi import FastAPI
from app.models.database import engine, Base
from app.routers import auth, strava

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Strava Route Recommender",
    description="Get personalized route recommendations based on your Strava history.",
    version="0.1.0"
)

app.include_router(auth.router)
app.include_router(strava.router)

@app.get("/health")
def health_check():
    return {"status":"healthy"}


