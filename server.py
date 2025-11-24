from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field
import httpx

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


@mcp.tool()
async def get_articles() -> list[Article]:
    """
    Retrieve a list of blog articles from the API.

    Returns:
        A list of articles with metadata including title, author, URL, and engagement metrics.
    """
    api_url = "https://alayman.io/api/articles"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, timeout=10.0)
            response.raise_for_status()
            articles_data = response.json()

            # Parse and validate articles using Pydantic
            articles = [Article(**article) for article in articles_data]
            return articles

        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"Request error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to retrieve articles: {str(e)}")


if __name__ == "__main__":
    # Run server with streamable-http transport for easy testing
    mcp.run(transport="streamable-http")
