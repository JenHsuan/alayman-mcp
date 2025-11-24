# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server project named "shellserver". MCP servers expose tools, resources, and prompts that can be used by MCP clients like Claude Desktop.

## Development Setup

**Python Version**: 3.11 (specified in `.python-version`)

**Package Manager**: This project uses `uv` for dependency management.

Install dependencies:
```bash
uv sync
```

## Running the Server

MCP servers are typically not run standalone but are configured in an MCP client (like Claude Desktop). To test the server during development:

```bash
uv run server.py
```

For MCP servers, you typically want to use the MCP inspector for testing:
```bash
npx @modelcontextprotocol/inspector uv run server.py
```

## Architecture

**MCP Server Implementation**: The main server logic should be implemented in `server.py` using the `mcp` package (version >=1.22.0).

MCP servers typically define:
- **Tools**: Functions that the LLM can call to perform actions
- **Resources**: Data sources that can be read (like files or API endpoints)
- **Prompts**: Reusable prompt templates

## Key Dependencies

- `mcp[cli]>=1.22.0`: The Model Context Protocol SDK with CLI support

## Project Structure

This is a minimal single-file MCP server project. The main implementation goes in `server.py`.


## Rules
Always follows rules from the following files.
* rules/python.md
