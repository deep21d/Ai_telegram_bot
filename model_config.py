from langchain_openai import ChatOpenAI
from prompts import get_prompt
from langchain_classic.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

llm = ChatOpenAI(
    model_name="openai/gpt-oss-120b",
    openai_api_key=os.getenv("OPENAI_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-OpenRouter-Title": "My LangChain App",
    }
)

# store memory per user
memory_store = {}


def get_model_response(user_text, chat_id):

    # create memory for new user
    if chat_id not in memory_store:
        memory_store[chat_id] = ConversationBufferMemory(return_messages=True)

    memory = memory_store[chat_id]

    # load chat history
    history = memory.load_memory_variables({})["history"]

    ready_prompt = get_prompt(user_text)

    # combine history + new prompt
    messages = history + ready_prompt.messages

    response = llm.invoke(messages)

    # save conversation
    memory.save_context(
        {"input": user_text},
        {"output": response.content}
    )

    return response