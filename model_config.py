import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
# If the above still fails in your specific environment version, use:
# from langchain.agents.agent import AgentExecutor
from langchain import hub
from langchain_core.messages import HumanMessage, AIMessage
from tools.weather import get_weather

# Assuming these are your custom imports
# from prompts import get_prompt
# from tools import get_weather

load_dotenv()

# 1. Setup the LLM (OpenRouter)
llm = ChatOpenAI(
    model_name="openai/gpt-oss-120b", # Standard model name
    openai_api_key=os.getenv("OPENAI_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-OpenRouter-Title": "My LangChain App",
    },
    max_tokens=500,
    temperature=0.3
)

# 2. Tools and Prompt
# Make sure get_weather has a @tool decorator!
tools = [get_weather]

# IMPORTANT: The 'hwchase17/react' prompt expects exactly these variables:
# 'input', 'agent_scratchpad', and 'tools'. 
# It does NOT natively support 'chat_history'. 
# Let's use a version that supports memory:
# In model_config.py
base_prompt = hub.pull("hwchase17/react-chat")
# Add your custom Telegram instructions to the beginning
prompt = base_prompt.partial(
    instructions="Give short, crisp answers (2–5 bullet points). Format for Telegram using Markdown."
)

# 3. Construct the Agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True # Good for small LLMs that might trip up
)

# 4. Simple Memory Store (Dictionary)
memory_store = {}

def get_model_response(user_text, chat_id):
    # Initialize history for this user if it doesn't exist
    if chat_id not in memory_store:
        memory_store[chat_id] = []

    # Get the history for this specific chat
    history = memory_store[chat_id]

    # 5. RUN THE AGENT
    # The agent_executor handles the 'get_prompt' logic internally.
    # We pass 'input' and 'chat_history' as required by the 'react-chat' prompt.
    result = agent_executor.invoke({
        "input": user_text,
        "chat_history": history
    })

    final_answer = result["output"]

    # 6. Manually Update History
    # We store the interaction so the NEXT turn knows what happened.
    memory_store[chat_id].append(HumanMessage(content=user_text))
    memory_store[chat_id].append(AIMessage(content=final_answer))

    return final_answer

# Example Usage:
# print(get_model_response("What is the weather in London?", "user_123"))
