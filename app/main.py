from fastapi import FastAPI
from app.models.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Strava Route Recommender",
    description="Get personalized route recommendations based on your Strava history.",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status":"healthy"}


