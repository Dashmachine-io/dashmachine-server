import uvicorn

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

from app.api.v1 import api_router
from app.core import settings


def register_sockets():
    import app.sockets


app = FastAPI(title=settings.PROJECT_NAME)

socket = SocketManager(app=app, cors_allowed_origins=[])
register_sockets()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8123)
