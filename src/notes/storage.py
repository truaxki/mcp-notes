import json
from pathlib import Path
from datetime import datetime

# Storage file location
NOTES_FILE = Path("notes_storage.json")

class NoteStorage:
    """Storage system for managing persistent notes."""
    
    def __init__(self):
        """Initialize storage and load existing notes."""
        self.notes = self.load_notes()

    def load_notes(self) -> dict:
        """Load notes from storage file."""
        if NOTES_FILE.exists():
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_notes(self) -> None:
        """Save current notes to storage file."""
        with open(NOTES_FILE, "w") as f:
            json.dump(self.notes, f, indent=2)

    def get_all_notes(self) -> dict:
        """Return all stored notes."""
        return self.notes

    def add_note(self, name: str, content: str) -> tuple[str, str]:
        """Add a new note with content and timestamps."""
        if name in self.notes:
            raise ValueError(f"Note '{name}' already exists")
        
        current_time = datetime.now().isoformat()
        self.notes[name] = {
            "content": content,
            "created_at": current_time,
            "modified_at": current_time
        }
        self.save_notes()
        return current_time, content

    def update_note(self, name: str, content: str) -> tuple[str, str]:
        """Update existing note's content and modified time."""
        if name not in self.notes:
            raise ValueError(f"Note '{name}' not found")
        
        current_time = datetime.now().isoformat()
        self.notes[name]["content"] = content
        self.notes[name]["modified_at"] = current_time
        self.save_notes()
        return current_time, content

    def delete_note(self, name: str) -> dict:
        """Remove a note and return its data."""
        if name not in self.notes:
            raise ValueError(f"Note '{name}' not found")
        
        deleted_note = self.notes.pop(name)
        self.save_notes()
        return deleted_note