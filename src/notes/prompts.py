from typing import List, Dict, Optional
import mcp.types as types
from .storage import NoteStorage

class NotePrompts:
    """Handler for generating language model prompts from notes."""
    
    def __init__(self, storage: NoteStorage):
        """Initialize with storage instance."""
        self.storage = storage

    def list_prompts(self) -> List[types.Prompt]:
        """Return available prompt configurations."""
        return [
            types.Prompt(
                name="summarize-notes",
                description="Creates a summary of all notes",
                arguments=[
                    types.PromptArgument(
                        name="style",
                        description="Style of the summary (brief/detailed)",
                        required=False,
                    )
                ],
            )
        ]

    def get_prompt(self, name: str, arguments: Optional[Dict[str, str]]) -> types.GetPromptResult:
        """Generate a formatted prompt with current notes."""
        if name != "summarize-notes":
            raise ValueError(f"Unknown prompt: {name}")

        style = (arguments or {}).get("style", "brief")
        detail_prompt = " Give extensive details." if style == "detailed" else ""

        notes = self.storage.get_all_notes()
        return types.GetPromptResult(
            description="Summarize the current notes",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                        + "\n".join(
                            f"- {name}: {note['content']}"
                            for name, note in notes.items()
                        ),
                    ),
                )
            ],
        )