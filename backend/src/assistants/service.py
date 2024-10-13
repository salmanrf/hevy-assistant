from bson import ObjectId
from langchain.schema import AIMessage, HumanMessage

from . import assistant_agent
from src.users.models.user import UserModel


async def generate_chat_response(
    sid: str, user: UserModel, run_messages: list[AIMessage | HumanMessage]
):
    try:
        thread_id = str(ObjectId())

        run_config = {
            "configurable": {
                "thread_id": thread_id,
                "user_data": user.model_dump(by_alias=True),
                "socket_id": sid,
            }
        }

        async for event in assistant_agent.graph.astream(
            input={"messages": run_messages}, config=run_config, stream_mode="values"
        ):
            if isinstance(event, Exception):
                print(
                    "Error at assistant_Service.generate_chat_response.astream", event
                )

            if isinstance(event, dict) and event.get("messages", None):
                print("MESSAGE", event["messages"][-1])

        await assistant_agent.clear_thread(thread_id)

        event = event if isinstance(event, dict) else {}
        last_message = event.get("messages", [])[-1]

        print("LAST MESSAGE", last_message)

        return last_message

    except Exception as e:
        print("Error at assistant_service.generate_chat_response", e)
