from socket_server import socket_server
import src.users.service as user_service
from src.users.models.user import UserModel


def register_handlers():
    sio = socket_server.get_server()

    @sio.on("connect")
    async def on_connect(sid, _, auth):
        try:
            user_dto = UserModel.model_validate(auth, strict=False)

            user = await user_service.find_or_create_user(user_dto)

            user_room = str(user.id)

            await sio.save_session(
                sid=sid, session={
                    "chat_status": "idle", 
                    "user_data": user.model_dump(by_alias=True)
                }
            )
            await sio.enter_room(room=user_room, sid=sid)

        except Exception as e:
            print("Error at socket_server.on_connect", e)
