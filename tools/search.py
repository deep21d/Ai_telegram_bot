from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools import tool

search = DuckDuckGoSearchAPIWrapper(max_results=3)

@tool
def web_search(query: str) -> str:
    """Search the web for current information."""
    return search.run(query)