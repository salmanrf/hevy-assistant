from langchain_anthropic.chat_models import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)

from config import config
from .agent import Assistant, AssistantAgent
from .prompt import ASSISTANT_MAIN_PROMPT

anthropic_chat_model = ChatAnthropic(
    api_key=config.ANTHROPIC_API_KEY,
    model_name=config.ANTHROPIC_MODEL,
    temperature=config.ANTHROPIC_TEMPERATURE,
    max_tokens=config.ANTHROPIC_MAX_OUTPUT_TOKEN,
)

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(ASSISTANT_MAIN_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

assistant = Assistant(
    prompt=primary_assistant_prompt,
    chat_model=anthropic_chat_model,
    tools=[],
)

memory = MemorySaver()
assistant_agent = AssistantAgent(assistant=assistant, checkpointer=memory)
