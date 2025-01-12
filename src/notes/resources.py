from typing import List
from pydantic import AnyUrl
import mcp.types as types
from .storage import NoteStorage

class NoteResources:
    """Resource handler for exposing notes via URIs."""
    
    def __init__(self, storage: NoteStorage):
        """Initialize with storage instance."""
        self.storage = storage

    def list_resources(self) -> List[types.Resource]:
        """Return all notes as addressable resources."""
        return [
            types.Resource(
                uri=AnyUrl(f"note://internal/{name}"),
                name=f"Note: {name}",
                description=f"A simple note named {name}",
                mimeType="text/plain",
            )
            for name in self.storage.get_all_notes()
        ]

    def read_resource(self, uri: AnyUrl) -> str:
        """Read note content using note:// URI scheme."""
        if uri.scheme != "note":
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

        name = uri.path
        if name is not None:
            name = name.lstrip("/")
            notes = self.storage.get_all_notes()
            if name in notes:
                return notes[name]["content"]
        raise ValueError(f"Note not found: {name}")