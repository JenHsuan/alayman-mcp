from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create FastMCP server
mcp = FastMCP("shellserver")


class Article(BaseModel):
    """Model representing a blog article"""
    model_config = ConfigDict(populate_by_name=True)

    id: int
    title: str
    subtitle: str
    image: str = Field(description="URL to article image")
    url: str = Field(description="URL to article page")
    author: str = Field(alias="name", description="Article author name")
    time: str = Field(description="Publication timestamp (ISO 8601)")
    readtime: str = Field(description="Estimated reading time")
    category: int
    description: str
    shareCount: int = Field(description="Number of shares")
    checkCount: int = Field(description="Number of views/checks")


class ArticlesResponse(BaseModel):
    """Response model for paginated articles"""
    articles: list[Article]
    total: int
    offset: int
    limit: int
    has_more: bool


@mcp.prompt()
def list_articles(
    number: Annotated[int, Field(description="Number of articles to list")] = 10,
    condition: Annotated[str, Field(description="Condition or filter for articles")] = ""
) -> str:
    """
    Generate a prompt to list alayman's articles with optional conditions.

    Args:
        number: Number of articles to list (default: 10)
        condition: Optional condition or filter criteria (user-defined)

    Returns:
        A prompt string instructing the LLM to fetch and display articles.
    """
    prompt_text = f"List {number} alayman's articles"
    if condition:
        prompt_text += f" {condition}"

    prompt_text += f"\n\nPlease use the get_articles tool to fetch the articles. Set the limit parameter to {number}."

    if condition:
        prompt_text += f"\n\nApply the following condition when presenting the results: {condition}"

    prompt_text += "\n\nDisplay the results in a clear, readable format including the article title, author, publication time, and URL."

    return prompt_text


@mcp.tool()
async def get_articles(
    limit: Annotated[int, Field(description="Number of articles to return", ge=1, le=100)] = 20,
    offset: Annotated[int, Field(description="Number of articles to skip", ge=0)] = 0
) -> ArticlesResponse:
    """
    Retrieve a paginated list of blog articles from the API.

    Args:
        limit: Number of articles to return (default: 20, max: 100)
        offset: Number of articles to skip (default: 0)

    Returns:
        A paginated response containing articles, total count, pagination info, and has_more flag.
    """
    api_url = os.getenv("ALAYMAN_API_URL")
    if not api_url:
        raise Exception("ALAYMAN_API_URL environment variable is not set")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, timeout=10.0)
            response.raise_for_status()
            articles_data = response.json()

            # Parse and validate all articles using Pydantic
            all_articles = [Article(**article) for article in articles_data]
            total = len(all_articles)

            # Apply pagination
            paginated_articles = all_articles[offset:offset + limit]
            has_more = (offset + limit) < total

            return ArticlesResponse(
                articles=paginated_articles,
                total=total,
                offset=offset,
                limit=limit,
                has_more=has_more
            )

        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Request error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to retrieve articles: {str(e)}")


if __name__ == "__main__":
    # Run server with stdio transport
    mcp.run(transport="stdio")
