from typing import List
import mcp.types as types

class NotesToolList:
    """Handles tool registration and schema definitions."""
    
    @staticmethod
    def get_tool_list() -> List[types.Tool]:
        """Return list of available note management tools."""
        return [
            types.Tool(
                name="add-note",
                description="Create a new note",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["name", "content"],
                },
            ),
            types.Tool(
                name="list-all-notes",
                description="Read all stored notes",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="update-note",
                description="Update an existing note",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["name", "content"],
                },
            ),
            types.Tool(
                name="delete-note",
                description="Delete an existing note",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                    },
                    "required": ["name"],
                },
            )
        ]