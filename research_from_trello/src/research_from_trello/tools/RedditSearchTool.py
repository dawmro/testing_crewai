import os
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from tavily import TavilyClient


class TavilySearchToolInput(BaseModel):
    query: str = Field(..., description="The query to search the web for.")
    max_results: int = Field(3, description="The maximum number of results to return.")


class RedditTavilySearchTool(BaseTool):
    name: str = "Reddit Search Tool with Tavily"
    description: str = "Search Reddit using Tavily"
    args_schema: Type[BaseModel] = TavilySearchToolInput

    _tavily_client: TavilyClient = PrivateAttr()

    def __init__(self):
        super().__init__()
        self._tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def _run(self, query: str, max_results: int) -> str:
        return self._tavily_client.search(f"Reddit: {query}", max_results=max_results)