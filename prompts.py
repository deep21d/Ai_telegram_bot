from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a knowledgeable AI assistant.

Format responses for Telegram chat.

Rules:
- Use **bold headings**
- Use bullet points (•)
- Avoid tables
- Keep responses concise but informative
- Use clear sections when explaining topics
"""
    ),
    ("human", "{input}")
])


def get_prompt(user_text):
    return prompt.invoke({"input": user_text})