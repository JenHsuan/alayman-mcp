# Alayman MCP Server - Article Retrieval and Search

A Model Context Protocol (MCP) server that provides tools and prompts to retrieve and search blog articles from the **Alayman blog** ([A Layman on Medium](https://medium.com/a-layman)) by Jen-Hsuan Hsieh (Sean).

## Overview

This MCP server provides tools and prompts to interact with Alayman blog articles, allowing you to:
- Fetch paginated article lists (currently 285+ articles available)
- Search and filter articles by topic, title, or content
- Generate contextual prompts for article discovery
- Access article metadata including author, publication time, read time, and engagement metrics

## Features

- **Article Retrieval Tool**: Fetches paginated articles with customizable limit and offset
- **Article List Prompt**: Generates intelligent prompts for article discovery with optional filters
- **Structured Output**: Returns validated data using Pydantic models
- **Pagination Support**: Efficient handling of large article collections
- **Async HTTP**: Uses httpx for efficient async API calls
- **Error Handling**: Comprehensive exception handling for network and HTTP errors

## Topics Covered in the Blog

The Alayman blog covers a wide range of software engineering topics, including:

- **Frontend Development**: React, Angular, Next.js, Vue.js, TypeScript, JavaScript
- **Backend Development**: Django, Node.js, NestJS, Python, GraphQL, RESTful APIs
- **Data Visualization**: D3.js, Cytoscape.js, Highcharts, ECharts
- **Cloud & DevOps**: AWS, Docker, Kubernetes, CI/CD, GitLab, GitHub Actions
- **Architecture & Patterns**: Micro Frontends, Design Patterns, System Design
- **Testing**: Unit Testing, Integration Testing, Karma, Jasmine
- **AI & Tools**: Claude CLI, GitHub Copilot, RAG, LangChain.js
- **Web Performance**: SEO, Optimization, Caching, SSR/SSG
- **Career & Soft Skills**: Team Management, Digital Nomad Life, Conference Insights

## Requirements

- Python 3.11 or higher
- uv (package manager)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
uv sync
```

3. Create a `.env` file in the project root with the required API URL:

```bash
ALAYMAN_API_URL=your_api_url_here
```

## Usage

### Running the Server

Start the MCP server:

```bash
uv run server.py
```

The server uses stdio transport for communication with MCP clients.

### Testing with MCP Inspector

The MCP Inspector is a web-based tool for testing MCP servers:

```bash
npx @modelcontextprotocol/inspector uv run server.py
```

This will start the inspector and connect it to your server automatically.

### Integration with Claude Desktop

To use this server with Claude Desktop, add it to your Claude Desktop configuration:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "shellserver": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/server.py"],
      "cwd": "/absolute/path/to/shellserver"
    }
  }
}
```

Restart Claude Desktop after updating the configuration.

### Integration with Claude Code

You can add this server to Claude Code using the `claude mcp add` command. From the project directory, run:

```bash
claude mcp add --scope user alayman uv run $(pwd)/server.py
```

This will add the server with the name "alayman" to your user-level MCP configuration, making it available across all your Claude Code sessions.

Alternatively, you can manually add it to your Claude Code MCP configuration:

- **macOS/Linux**: `~/.claude/mcp.json`
- **Windows**: `%USERPROFILE%\.claude\mcp.json`

```json
{
  "mcpServers": {
    "shellserver": {
      "command": "uv",
      "args": ["run", "/absolute/path/to/server.py"],
      "cwd": "/absolute/path/to/shellserver"
    }
  }
}
```

After updating the configuration, restart Claude Code or reload the MCP servers for the changes to take effect.

### Integration with Docker and Claude Code

* Build the Docker image
```
docker build -t alayman .
```

* Add the Docker container as the MCP server
```
claude mcp add-json --scope user alayman '{"type":"stdio","command":"docker","args":["run","-i","--rm","--init","-e","DOCKER_CONTAINER=true","alayman"]}'
```

## Quick Start Examples

Once integrated with Claude Desktop or Claude Code, you can use the server in various ways:

**Direct tool usage:**
```
Show me the first 10 articles from the Alayman blog
Get articles 20-30 from the blog
Retrieve 5 articles starting from position 10
```

**Using the prompt command (Claude Code):**
```bash
/alayman:list_articles 10 "the title contains 'React'"
/alayman:list_articles 5 "articles about Django"
/alayman:list_articles 15 "published in the last year"
```

**Natural language queries:**
```
Find all articles about Angular
Show me articles related to AWS
List articles about data visualization with D3.js
```

## Available Tools and Prompts

### Tool: get_articles

Retrieves a paginated list of blog articles from the API.

**Parameters**:
- `limit` (int, optional): Number of articles to return (default: 20, min: 1, max: 100)
- `offset` (int, optional): Number of articles to skip (default: 0, min: 0)

**Returns**: An ArticlesResponse object containing:
- `articles` (list[Article]): List of article objects
- `total` (int): Total number of articles available
- `offset` (int): Current offset value
- `limit` (int): Current limit value
- `has_more` (bool): Whether more articles are available

**Article Object Fields**:
- `id` (int): Unique article identifier
- `title` (str): Article title
- `subtitle` (str): Article subtitle
- `image` (str): URL to article image
- `url` (str): URL to article page
- `author` (str): Article author name
- `time` (str): Publication timestamp (ISO 8601)
- `readtime` (str): Estimated reading time
- `category` (int): Article category ID
- `description` (str): Article description
- `shareCount` (int): Number of shares
- `checkCount` (int): Number of views/checks

**Example usage in Claude**:

```
Can you retrieve the first 10 articles?
Can you get articles 20-40?
Fetch the latest 5 articles from the blog.
```

### Prompt: list_articles

Generates an intelligent prompt to list and filter Alayman's articles. This prompt will instruct the LLM to use the get_articles tool and apply specific filters.

**Parameters**:
- `number` (int, optional): Number of articles to list (default: 10)
- `condition` (str, optional): Condition or filter criteria for articles (default: "")

**Example usage in Claude Code**:

```
/alayman:list_articles 5 "the title contains 'React'"
/alayman:list_articles 10 "published in 2024"
/alayman:list_articles 15 "related to Python"
```

When you run this prompt, it generates instructions for Claude to fetch articles and apply your specified conditions when presenting the results.

## Project Structure

```
alayman-mcp/
├── server.py           # Main MCP server implementation
├── pyproject.toml      # Project dependencies and metadata
├── uv.lock             # Dependency lock file
├── README.md           # This file
├── CLAUDE.md           # Claude Code project instructions
├── reference.md        # Additional reference documentation
├── Dockerfile          # Docker container configuration
├── .dockerignore       # Docker build exclusions
├── .env.example        # Example environment variables
├── .env                # Environment variables (not in git)
├── .python-version     # Python version specification (3.11)
├── .gitignore          # Git exclusions
├── .venv/              # Virtual environment (created by uv)
└── rules/              # Development rules and guidelines
    └── python.md       # Python coding standards
```

## Dependencies

- `mcp[cli]>=1.22.0` - Model Context Protocol SDK with CLI support
- `httpx>=0.28.0` - Modern async HTTP client
- `python-dotenv` - Environment variable management from .env files

## Development

### Architecture

The server uses the FastMCP framework from the MCP Python SDK, which provides:

- Simple decorator-based tool and prompt registration
- Automatic JSON schema generation from type hints
- Built-in validation using Pydantic models
- Support for async operations

### Code Structure

1. **Pydantic Models**:
   - `Article`: Defines the article schema for type-safe data validation
   - `ArticlesResponse`: Defines the paginated response structure
2. **Tool Function**: The `get_articles()` async function fetches and validates article data with pagination support
3. **Prompt Function**: The `list_articles()` function generates contextual prompts for article discovery
4. **Server Instance**: FastMCP server configured with stdio transport

## Error Handling

The server includes comprehensive error handling for:

- HTTP errors (4xx, 5xx responses)
- Network connectivity issues
- JSON parsing errors
- Data validation failures

All errors are caught and returned as descriptive exception messages.

## License

This project is provided as-is for educational and development purposes.

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Guide](https://github.com/modelcontextprotocol/python-sdk/tree/main/src/mcp/server/fastmcp)
