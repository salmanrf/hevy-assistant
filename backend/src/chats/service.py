from bson import ObjectId
from langchain.schema.messages import AIMessage, HumanMessage

import src.assistants.service as assistant_service
from src.databases.mongo import mongo_connection
from src.users.models.user import UserModel
from .models.chat import ChatModel, ChatMessageModel, MessageAuthor
from .schemas.chat import MessageSchema


async def find_one_chat(criteria: dict):
    try:
        db = await mongo_connection.get_db()

        result = await db["chats"].find_one(criteria)

        if not result:
            return None

        return ChatModel(**result)

    except Exception as e:
        print("Error at chat_service.find_one_chat", e)

        raise e


async def create_chat(chat_dto: ChatModel):
    try:
        db = await mongo_connection.get_db()

        inserted = await db["chats"].insert_one(chat_dto.model_dump(by_alias=True))
        saved = await find_one_chat({"_id": inserted.inserted_id})

        return saved
    except Exception as e:
        print("Error at chat_service.create_chat", e)

        raise e


async def get_or_create_chat(user: UserModel, additional_data: dict = {}):
    try:
        chat = await find_one_chat({"user_id": user.id})

        if chat:
            return chat

        chat_dto = ChatModel(user_id=user.id, **additional_data)

        chat = await create_chat(chat_dto)

        return chat

    except Exception as e:
        print("Error at chat_service.get_or_create_chat", e)

        raise e


async def find_chat_messages(
    chat_criteria: dict,
    message_criteria: dict = None,
    message_sort: dict = None,
    message_limit: int = None,
):
    try:
        db = await mongo_connection.get_db()

        pipeline = [
            {"$match": chat_criteria},
            {"$unwind": {"path": "$messages", "preserveNullAndEmptyArrays": False}},
            {"$replaceRoot": {"newRoot": "$messages"}},
        ]

        if message_criteria:
            pipeline.append({"$match": message_criteria})

        if message_sort:
            pipeline.append({"$sort": message_criteria})
        else:
            pipeline.append({"$sort": {"created_at": -1}})

        if message_limit:
            pipeline.append({"$limit": message_limit})

        results = (
            await db["chats"]
            .aggregate(pipeline)
            .to_list(length=message_limit if message_limit else None)
        )

        if not isinstance(results, list) or len(results) == 0:
            return []

        return [ChatMessageModel(**m) for m in results]

    except Exception as e:
        print("Error at chat_service.find_chat_messages", e)

        raise e


async def find_last_n_chat_messages(chat_criteria: dict, n: int):
    try:
        results = await find_chat_messages(chat_criteria=chat_criteria, message_limit=n)

        return results

    except Exception as e:
        print("Error at chat_service.get_last_n_chat_messages", e)

        raise e


async def save_chat_messages(chat_criteria: dict, messages: list[ChatMessageModel]):
    try:
        db = await mongo_connection.get_db()

        messages_dict = [m.model_dump(by_alias=True) for m in messages]

        _ = await db["chats"].update_one(
            filter=chat_criteria,
            update={"$push": {"messages": {"$each": messages_dict}}},
        )

        return None
    except Exception as e:
        print("Error at chat_service.save_chat_messages", e)

        raise e


async def create_chat_response(
    sid: str, user: UserModel, chat: ChatModel, message_dto: MessageSchema
):
    try:
        chat_history: list[ChatMessageModel] = await find_chat_messages(
            chat_criteria={"_id": chat.id}, message_limit=10
        )

        run_messages = format_chat_history_anthropic(chat_history)
        run_messages.append(HumanMessage(message_dto.content))

        human_message_model = ChatMessageModel(
            author=MessageAuthor(author_id=user.id, author_type="user"),
            content=message_dto.content,
        )

        response_message = await assistant_service.generate_chat_response(
            sid=sid, user=user, run_messages=run_messages
        )

        response_msg_model = ChatMessageModel(
            author=MessageAuthor(author_id=None, author_type="assistant"),
            content=response_message.content,
        )

        await save_chat_messages(
            chat_criteria={"_id": chat.id},
            messages=[
                human_message_model,
                response_msg_model,
            ],
        )

        return response_msg_model

    except Exception as e:
        print("Error at chat_service.create_chat_response", e)

        raise e


def format_chat_history_anthropic(
    chat_history: list[ChatMessageModel],
) -> list[AIMessage | HumanMessage]:
    try:
        chat_history = chat_history[::-1]
        messages = []
        start_index = 0

        for i, x in enumerate(chat_history):
            if x.author.author_type == "user":
                start_index = i
                break

        for ch in chat_history[start_index:]:
            if ch.author.author_type == "user":
                messages.append(HumanMessage(ch.content))
            else:
                messages.append(AIMessage(ch.content))

        return messages
    except Exception as e:
        print("Error at chat_service.format_chat_history_anthropic", e)

        raise e
