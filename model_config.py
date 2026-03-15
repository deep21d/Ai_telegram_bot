import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from tools.weather import get_weather
from tools.search import web_search


load_dotenv()
print(os.getenv("OPENAI_KEY"))

# 1. Setup the LLM (OpenRouter)
llm = ChatOpenAI(
    model_name="openai/gpt-oss-120b:free", # Standard model name
    openai_api_key=os.getenv("OPENAI_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-OpenRouter-Title": "My LangChain App",
    },
    # max_tokens=500,
    temperature=0.3
)

# 2. Tools and Prompt
# Make sure get_weather has a @tool decorator!
tools = [get_weather,web_search]

# 3. Construct the Agent
agent = create_agent(llm, tools)

# 4. Simple Memory Store (Dictionary)
memory_store = {}

def get_model_response(user_text, chat_id):
    # Initialize history for this user if it doesn't exist
    if chat_id not in memory_store:
        memory_store[chat_id] = []

    # Get the history for this specific chat
    history = memory_store[chat_id]

    input = {
    "messages": history + [HumanMessage(content=user_text)]
    }
    result = agent.invoke(input)

    for chunk in agent.stream(input, stream_mode="updates"):
        print(chunk)
    
    
    final_answer = result["messages"][-1].content

    # 6. Manually Update History
    # We store the interaction so the NEXT turn knows what happened.
    memory_store[chat_id].append(HumanMessage(content=user_text))
    memory_store[chat_id].append(AIMessage(content=final_answer))

    return final_answer

# # Example Usage:
# print(get_model_response("who won t20 woldcup, jut tell me the name", "user_123"))
