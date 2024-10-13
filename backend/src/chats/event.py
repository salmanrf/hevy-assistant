from bson import ObjectId
from pydantic import ValidationError

import src.chats.service as chat_service
from socket_server import socket_server
from src.users.models.user import UserModel
from src.chats.schemas.chat import MessageSchema, MessageResponseSchema, FindNMessagesSchema, FindNMessagesResSchema


def register_handlers():
    sio = socket_server.get_server()

    @sio.on("chat:message")
    async def on_message(sid, message_dto: MessageSchema):
        user: UserModel = None

        try:
            message_dto = MessageSchema.model_validate(message_dto)
            session = await sio.get_session(sid)
            status = {"chat_status": session.get("chat_status", None)}

            # ? Stop if previous message is still being processed
            if  status["chat_status"] == "processing":
                return None
            # ? Start processing new message and update state
            status["chat_status"] = "processing"
            await sio.save_session(
                sid=sid,
                session=status
            )
            await sio.emit(
                event="chat:status",
                to=sid,
                data=status,
            )

            # ? Retrieve user from session
            user_data = session.get("user_data")
            user = UserModel(**user_data)

            # ? Get response
            chat = await chat_service.get_or_create_chat(user=user)
            response = await chat_service.create_chat_response(
                sid=sid, user=user, chat=chat, message_dto=message_dto
            )

            msg_payload = MessageResponseSchema(
                temp_id=message_dto.temp_id,
                message=response
            ).model_dump_json(by_alias=True) 

            # ? Finished processing message
            status["chat_status"] = "idle"
            await sio.save_session(
                sid=sid,
                session=status
            )
            await sio.emit(
                event="chat:status",
                to=sid,
                data=status,
            )

            await sio.emit(
                event="chat:message:created",
                room=str(user.id),
                data=msg_payload,
            )

        except ValidationError as e:
            print("Validaiton Error at chat_event.on_message", e)

            await sio.emit(
                event="chat:message:validation-error",
                to=sid,
                data=e.errors,
            )

        except Exception as e:
            print("Error at chat_event.on_message", e)

            await sio.emit(
                event="chat:message:error",
                to=sid,
                data=MessageResponseSchema(
                    temp_id=message_dto.temp_id,
                ).model_dump_json()
            )
    
    @sio.on("chat:get-status")
    async def on_message_status_check(sid, _):
        try:
            session = await sio.get_session(sid)

            return {"chat_status": session.get("chat_status")}
        except Exception as e:
            print("Error at chat_event.on_message_status_check", e)

    @sio.on("chat:get-last-n-messages")
    async def on_get_last_n_messages(sid, dto: FindNMessagesSchema):
        response = FindNMessagesResSchema(
            messages=[]
        )

        try:
            dto = FindNMessagesSchema.model_validate(dto)
            session = await sio.get_session(sid=sid)

            user_data = session.get("user_data", {})
            user_id = user_data.get("_id", None)


            if not user_id:
                return response.model_dump_json()

            messages_criteria = {
                "_id": {
                    "$lt": ObjectId(dto.last_n_id)
                }
            } if dto.last_n_id else None
            messages = await chat_service.find_chat_messages(
                chat_criteria={
                    "user_id": user_data["_id"]
                },
                message_criteria=messages_criteria,
                message_limit=dto.n_messages,
            )

            # ? Reverse the messages order because because  
            # ? find_chat_messages sort by created_at in reverse order
            messages = messages[::-1]

            response.messages = messages

            return response.model_dump_json(by_alias=True)
            
        except ValidationError as e:
            print("Validation Error at chat_event.get-last-n-messages", e)

            await sio.emit(
                event="chat:get-last-n-messages:error",
                to=sid,
                data=e.errors
            )

            return response.model_dump_json()
        except Exception as e:
            print("Error at chat_event.on_get_last_n_messages", e)

            return response.model_dump_json()
