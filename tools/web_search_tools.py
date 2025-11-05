from utils.decorators import tool
from ddgs import DDGS
import flyte
from typing import Optional


@tool(agent="web_search")
@flyte.trace
async def duck_duck_go(
    query: str,
    max_results: int = 10,
    region: str = "us-en",
    safesearch: str = "moderate",
    timelimit: Optional[str] = None
) -> list[dict]:
    """
    Search DuckDuckGo for web results.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to return (default: 10).
        region (str): Region code for search results (default: "us-en").
            Examples: "us-en", "uk-en", "de-de", "fr-fr"
        safesearch (str): Safe search level (default: "moderate").
            Options: "off", "moderate", "strict"
        timelimit (str, optional): Time limit for results (default: None for all time).
            Options: "d" (day), "w" (week), "m" (month), "y" (year)

    Returns:
        list[dict]: List of search results with 'title', 'href', and 'body' keys.
    """
    ddgs = DDGS()

    results = ddgs.text(
        query=query,
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results
    )

    # Convert generator to list and extract relevant fields
    search_results = []
    for result in results:
        search_results.append({
            "title": result.get("title", ""),
            "href": result.get("href", ""),
            "body": result.get("body", "")
        })

    print(f"[DuckDuckGo] Found {len(search_results)} results for: {query}")
    return search_results