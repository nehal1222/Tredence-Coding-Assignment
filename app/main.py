from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.api.routes import router  # your workflow API routes
from app.api.websocket import ws_router   # websocket routes
from app.database import db
from app.workflows.code_review import register_code_review_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Workflow Engine...")
    await db.connect()
    register_code_review_tools()
    logger.info("Workflow Engine started successfully")
    yield
    logger.info("Shutting down Workflow Engine...")
    await db.disconnect()

app = FastAPI(
    title="Workflow Engine",
    description="A powerful async workflow engine for building agent workflows",
    version="1.0.0",
    lifespan=lifespan
)

# Register REST API routes
app.include_router(router, prefix="/api/v1", tags=["workflows"])

# Register WebSocket routes
app.include_router(ws_router, prefix="/api/v1", tags=["websocket"])

@app.get("/")
async def root():
    return {
        "message": "Workflow Engine API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
