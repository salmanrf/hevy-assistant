from bson import ObjectId
from typing import Annotated
from typing_extensions import TypedDict
from langchain_anthropic.chat_models import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.base import BaseCheckpointSaver, empty_checkpoint
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, AIMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.prompts.chat import ChatPromptTemplate


class AssistantState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class Assistant:
    prompt: ChatPromptTemplate
    chat_model: ChatAnthropic
    runnable: Runnable
    tools: list

    def __init__(
        self, prompt: ChatPromptTemplate, chat_model: ChatAnthropic, tools: list
    ) -> None:
        self.prompt = prompt
        self.chat_model = chat_model
        self.tools = tools
        self.runnable = self.prompt | self.chat_model.bind_tools(self.tools)

    async def __call__(self, state: AssistantState, config: RunnableConfig):
        filtered_messages = state["messages"]
        # formatted_prompt = await self.prompt.aformat(messages=filtered_messages)

        result = await self.runnable.ainvoke({"messages": filtered_messages})

        return {"messages": result}

    def filter_messages(self, messages: list[AnyMessage]):
        messages_size = len(messages)

        if messages_size > 3:
            return messages[messages_size - 3 :]

        return messages


class AssistantAgent:
    checkpointer: BaseCheckpointSaver

    def __init__(self, assistant: Assistant, checkpointer: BaseCheckpointSaver) -> None:
        graph_builder = StateGraph(AssistantState)

        assistant_node = assistant
        tool_node = ToolNode(tools=assistant.tools)

        graph_builder.add_node("assistant_llm", assistant_node)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "assistant_llm")
        graph_builder.add_conditional_edges("assistant_llm", tools_condition)
        graph_builder.add_edge("tools", "assistant_llm")

        graph = graph_builder.compile(checkpointer=checkpointer)

        self.graph = graph
        self.checkpointer = checkpointer

    async def clear_thread(self, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}
        checkpoint = empty_checkpoint()

        self.checkpointer.aput(
            config=config, checkpoint=checkpoint, metadata={}, new_versions={}
        )
