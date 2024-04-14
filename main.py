import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_uri: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

db_client = AsyncIOMotorClient(settings.mongo_uri)
db = db_client.todoDb

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
