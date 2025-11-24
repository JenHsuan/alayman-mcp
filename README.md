# Shellserver - MCP Article Retrieval Server

A simple Model Context Protocol (MCP) server that exposes a tool to retrieve blog articles from an external API.

## Overview

This MCP server provides a single tool called `get_articles` that fetches and returns a list of blog articles with metadata including titles, authors, URLs, and engagement metrics.

## Features

- **Article Retrieval Tool**: Fetches articles
- **Structured Output**: Returns validated data using Pydantic models
- **Async HTTP**: Uses httpx for efficient async API calls
- **Error Handling**: Proper exception handling for network and HTTP errors

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

## Available Tools

### get_articles

Retrieves a list of blog articles from the API.

**Parameters**: None

**Returns**: A list of Article objects with the following fields:

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
Can you retrieve the latest articles using the get_articles tool?
```

## Project Structure

```
shellserver/
   server.py           # Main MCP server implementation
   pyproject.toml      # Project dependencies
   README.md           # This file
   CLAUDE.md           # Claude Code project instructions
   .python-version     # Python version specification
```

## Dependencies

- `mcp[cli]>=1.22.0` - Model Context Protocol SDK with CLI support
- `httpx>=0.28.0` - Modern async HTTP client
- `python-dotenv` - Environment variable management from .env files

## Development

### Architecture

The server uses the FastMCP framework from the MCP Python SDK, which provides:

- Simple decorator-based tool registration
- Automatic JSON schema generation from type hints
- Built-in validation using Pydantic models
- Support for async operations

### Code Structure

1. **Pydantic Model**: Defines the `Article` schema for type-safe data validation
2. **Tool Function**: The `get_articles()` async function fetches and validates article data
3. **Server Instance**: FastMCP server configured with streamable-http transport

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
