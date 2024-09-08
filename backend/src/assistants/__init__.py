from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)

from config import config
from src.checkpointer import mongodb_checkpointer
from .agent import Assistant, AssistantAgent
from .tools.find_workouts import find_workout_routine
from .prompt import ASSISTANT_MAIN_PROMPT

openai_chat_model = ChatOpenAI(
    model=config.OPENAI_MODEL,
    temperature=config.OPENAI_TEMPERATURE,
    api_key=config.OPENAI_API_KEY,
)

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(ASSISTANT_MAIN_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

assistant = Assistant(
    prompt=primary_assistant_prompt,
    chat_model=openai_chat_model,
    tools=[find_workout_routine],
)

assistant_agent = AssistantAgent(assistant=assistant, checkpointer=mongodb_checkpointer)
