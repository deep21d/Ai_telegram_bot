from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def web_search(query: str):
    """Search the internet for current news, sports results, and recent information."""
    
    search = DuckDuckGoSearchRun()
    search_res = search.invoke(query)
    # print(search_res)
    return search_res


# web_search("who won t20 worldcup 2026")
