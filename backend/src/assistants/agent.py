from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class AssistantState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class Assistant:
    prompt: ChatPromptTemplate
    chat_model: ChatOpenAI
    runnable: Runnable
    tools: list

    def __init__(
        self, prompt: ChatPromptTemplate, chat_model: ChatOpenAI, tools: list
    ) -> None:
        self.prompt = prompt
        self.chat_model = chat_model
        self.tools = tools
        self.runnable = self.prompt | self.chat_model.bind_tools(self.tools)

    async def __call__(self, state: AssistantState, config: RunnableConfig):
        filtered_messages = self.filter_messages(state["messages"])

        # formatted_prompt = await self.prompt.aformat(messages=filtered_messages)

        result = await self.runnable.ainvoke({"messages": filtered_messages})

        return {"messages": result}

    def filter_messages(self, messages: list[AnyMessage]):

        messages_size = len(messages)

        last_message_is_tool_result = False

        if messages_size > 0 and hasattr(messages[-1], "tool_call_id"):
            last_message_is_tool_result = True

        if messages_size > 5:
            # ? Include the last tool_call message if the last message is a tool call result
            start_index = messages_size - 5 - (1 if last_message_is_tool_result else 0)

            return messages[start_index:]

        return messages


class AssistantAgent:

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
