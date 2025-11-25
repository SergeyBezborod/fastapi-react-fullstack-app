from contextlib import asynccontextmanager
from .database import init_db
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .ws_manager import manager
import time
from .routers.user_routers import router as user_routers
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Social.NET (FastAPI)",
    debug=True,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routers, prefix="/api")


@app.get("/")
async def test():
    return {"status": "OK", "message": "Server is running!"}


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(f"{username}-{message}-{time.strftime('%H:%M:%S', time.localtime())}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"-User {username} left the chat")
