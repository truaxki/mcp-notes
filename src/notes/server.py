import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl

from .storage import NoteStorage
from .tools import NotesToolList, NotesToolHandler
from .resources import NoteResources
from .prompts import NotePrompts

# Initialize server components
server = Server("Notes")
storage = NoteStorage()
tool_list = NotesToolList()
tool_handler = NotesToolHandler(storage)
resources = NoteResources(storage)
prompts = NotePrompts(storage)

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """Return list of available note resources."""
    return resources.list_resources()

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read content of specified note resource."""
    return resources.read_resource(uri)

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """Return list of available prompt configurations."""
    return prompts.list_prompts()

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    """Generate specified prompt with current notes."""
    return prompts.get_prompt(name, arguments)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Return list of available note management tools."""
    return tool_list.get_tool_list()

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Execute requested note management tool."""
    result = await tool_handler.handle_tool(name, arguments)
    await server.request_context.session.send_resource_list_changed()
    return result

async def main():
    """Run the notes server using stdin/stdout streams."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="Notes",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())