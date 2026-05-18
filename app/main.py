from fastapi import FastAPI
from app.database import init_db
from app.logger import logger
from app.routers.tasks import router

app = FastAPI(
    title="Task Management API"
)

@app.on_event("startup")
async def on_startup():
    await init_db()
    logger.info("Task Management API started")

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Task Management API Running"
    }
