from langchain.tools import tool
from duckduckgo_search import DDGS

@tool
def web_search(query: str) -> str:
    """Search the internet for current news, sports results, and recent information."""
    
    with DDGS() as ddgs:
        results = ddgs.text(query + " latest", max_results=5)

        formatted_results = []

        for r in results:
            formatted_results.append(
                f"Title: {r['title']}\n"
                f"Snippet: {r['body']}\n"
                f"Source: {r['href']}\n"
            )

        return "\n\n".join(formatted_results)