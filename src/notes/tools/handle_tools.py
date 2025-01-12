from typing import Dict, List, Optional
import mcp.types as types
from ..storage import NoteStorage

class NotesToolHandler:
    """Handles execution of note management tools."""
    
    def __init__(self, storage: NoteStorage):
        """Initialize with storage instance."""
        self.storage = storage

    async def handle_tool(self, name: str, arguments: Optional[Dict]) -> List[types.TextContent]:
        """Route tool requests to appropriate handlers."""
        if name == "add-note":
            return await self._handle_add_note(arguments)
        elif name == "update-note":
            return await self._handle_update_note(arguments)
        elif name == "delete-note":
            return await self._handle_delete_note(arguments)
        elif name == "list-all-notes":
            return await self._handle_list_notes()
        else:
            raise ValueError(f"Unknown tool: {name}")

    async def _handle_add_note(self, arguments: Optional[Dict]) -> List[types.TextContent]:
        """Process note creation requests."""
        if not arguments:
            raise ValueError("Missing arguments")

        note_name = arguments.get("name")
        content = arguments.get("content")

        if not note_name or not content:
            raise ValueError("Missing name or content")

        current_time, content = self.storage.add_note(note_name, content)
        return [
            types.TextContent(
                type="text",
                text=f"Created note '{note_name}' with content: {content}\nCreated at: {current_time}",
            )
        ]

    async def _handle_update_note(self, arguments: Optional[Dict]) -> List[types.TextContent]:
        """Process note update requests."""
        if not arguments:
            raise ValueError("Missing arguments")

        note_name = arguments.get("name")
        content = arguments.get("content")

        if not note_name or not content:
            raise ValueError("Missing name or content")

        current_time, content = self.storage.update_note(note_name, content)
        return [
            types.TextContent(
                type="text",
                text=f"Updated note '{note_name}' with content: {content}\nModified at: {current_time}",
            )
        ]

    async def _handle_delete_note(self, arguments: Optional[Dict]) -> List[types.TextContent]:
        """Process note deletion requests."""
        if not arguments:
            raise ValueError("Missing arguments")

        note_name = arguments.get("name")
        if not note_name:
            raise ValueError("Missing name")

        deleted_note = self.storage.delete_note(note_name)
        return [
            types.TextContent(
                type="text",
                text=f"Deleted note '{note_name}'\nLast modified: {deleted_note['modified_at']}",
            )
        ]

    async def _handle_list_notes(self) -> List[types.TextContent]:
        """Process note listing requests."""
        notes = self.storage.get_all_notes()
        if not notes:
            return [
                types.TextContent(
                    type="text",
                    text="No notes stored yet.",
                )
            ]
        
        notes_text = "\n".join(
            f"- {name}:\n"
            f"  Content: {note['content']}\n"
            f"  Created: {note['created_at']}\n"
            f"  Modified: {note['modified_at']}"
            for name, note in notes.items()
        )
        return [
            types.TextContent(
                type="text",
                text=f"All stored notes:\n{notes_text}",
            )
        ]