import uvicorn
import socketio
import argparse

from typing import AsyncGenerator
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from socket_server import socket_server


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # * Startup
    from src.databases.mongo import mongo_connection

    try:
        await mongo_connection.connect()

        await mongo_connection.get_server_info()

    except Exception as e:
        raise Exception() from e

    yield

    await mongo_connection.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    sio = socket_server.create_server()

    socket_app = socketio.ASGIApp(socketio_server=sio)

    app.mount("/", socket_app)

    from event import register_handlers
    from src.chats.event import register_handlers as register_chat_handlers

    register_handlers()
    register_chat_handlers()

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Hevy Assistant server.")
    parser.add_argument(
        "--env",
        type=str,
        required=True,
        help="Environment name to load .env file. e.g. dev, prod, test",
    )
    args = parser.parse_args()

    if args.env == "prod":
        dotenv_path = ".env.prod"
        reload = False
    elif args.env == "dev":
        dotenv_path = ".env.dev"
        reload = True
    elif args.env == "test":
        dotenv_path = ".env.test"
        reload = False

    load_dotenv(dotenv_path=dotenv_path)

    from config import config

    uvicorn.run(
        "main:create_app",
        port=config.SERVER_PORT,
        factory=True,
        reload=reload,
    )
