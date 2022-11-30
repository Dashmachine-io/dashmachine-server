from app.main import socket


@socket.on("check-connection")
async def check_connection():
    await socket.emit("confirm-connection", "confirmed")
