# MCP Notes Server
[![smithery badge](https://smithery.ai/badge/notes)](https://smithery.ai/server/notes)

A Model Context Protocol (MCP) server implementation for managing notes with persistent storage.

<a href="https://glama.ai/mcp/servers/tg4ugmp8jr"><img width="380" height="200" src="https://glama.ai/mcp/servers/tg4ugmp8jr/badge" alt="Notes Server MCP server" /></a>

## Features

- Create, read, update, and delete notes
- Persistent storage using JSON
- Timestamp tracking for creation and modifications
- Note summarization via prompts
- Resource-based access using note:// URI scheme

## Installation

### Installing via Smithery

To install Notes Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/notes):

```bash
npx -y @smithery/cli install notes --client claude
```

### Manual Installation
1. Ensure you have Python 3.10 or later installed
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   
   # On Unix/MacOS:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install MCP
   ```

## Project Structure

```
notes/
├── __init__.py          # Package initialization
├── server.py           # Main server implementation
├── storage.py          # Note persistence layer
├── resources.py        # Resource handling (note:// URIs)
├── prompts.py         # LLM prompt generation
└── tools/             # Server tools
    ├── __init__.py    # Tools package initialization
    ├── list_tools.py  # Tool listing functionality
    └── handle_tools.py # Tool handling implementation
```

## Available Tools

- `add-note`: Create a new note
- `list-all-notes`: Display all stored notes
- `update-note`: Modify an existing note
- `delete-note`: Remove a note

## Usage

1. Start the server:
   ```bash
   mcp install src/notes
   mcp start Notes
   ```

2. Example operations:
   ```python
   # Create a note
   await client.call_tool("add-note", {
       "name": "example",
       "content": "This is a test note"
   })

   # List all notes
   await client.call_tool("list-all-notes")

   # Update a note
   await client.call_tool("update-note", {
       "name": "example",
       "content": "Updated content"
   })

   # Delete a note
   await client.call_tool("delete-note", {
       "name": "example"
   })
   ```

## Storage

Notes are stored in `notes_storage.json` with the following structure:
```json
{
    "note_name": {
        "content": "Note content",
        "created_at": "2025-01-12T11:28:16.721704",
        "modified_at": "2025-01-12T11:28:16.721704"
    }
}
```

## Resource Access

Notes can be accessed as resources using the `note://` URI scheme:
- List resources: Returns all available notes as resources
- Read resource: Access a specific note using `note://internal/note_name`

## Prompt Generation

The server includes a prompt generation feature for note summarization:
- Supports both brief and detailed summaries
- Formats notes for language model input
- Available via the "summarize-notes" prompt

## Development

To modify or extend the server:
1. Clone the repository
2. Install development dependencies
3. Make changes in the appropriate module
4. Test thoroughly before deploying

## Testing

Tests should cover:
- Basic CRUD operations
- Multiple note handling
- Error cases
- Resource access
- Prompt generation

## License

[Add your license here]
