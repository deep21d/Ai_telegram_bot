from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

# create search instance once (faster)
search = DuckDuckGoSearchResults(num_results=5)

@tool
def web_search(query: str) -> str:
    """Search the internet for current news, sports results, and recent information."""
    
    results = search.invoke(query)

    if not results:
        return "No good search results found."

    return results

# res = web_search("who won t20 woldcup2026")
# print(type(res))