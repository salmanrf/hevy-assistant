import socketio


class SocketServer:
    def __init__(self):
        self.server = None

    def create_server(self):
        self.server = socketio.AsyncServer(
            cors_allowed_origins="*", async_mode="asgi", async_handlers=True
        )

        return self.server

    def get_server(self):
        return self.server


socket_server = SocketServer()
