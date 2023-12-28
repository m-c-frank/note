import os
import subprocess
from pathlib import Path
from pydantic import BaseModel

# default location
PATH_NOTES = os.getenv("PATH_NOTES", Path.home() / "notes" / "notes")
EDITOR = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
FILE_EXTENSION = "md"


class Note(BaseModel):
    """note model"""
    repo: "Repository"
    index: int

    @property
    def path(self) -> Path:
        return self.repo / f"{self.index}.{FILE_EXTENSION}"

    def open(self, editor: str = EDITOR):
        subprocess.run([editor, str(self.path)])

    def read_content(self) -> str:
        with open(self.path, "r") as f:
            return f.read()

    def write_content(self, content: str) -> None:
        with open(self.path, "w") as f:
            f.write(content)


class Repository(BaseModel):
    """repository in which notes exist"""
    path: Path = PATH_NOTES

    def last_index(self) -> int:
        highest_num = max(
            (
                int(p.stem) for p in self.path.glob(
                    f'*.{FILE_EXTENSION}'
                )
                if p.stem.isdigit()
            ),
            default=0
        )
        return highest_num

    def get_last_note(self) -> Note:
        index_note = self.get_last_index()
        note = Note(repo=self, index=index_note)
        return note

    def take_note(self) -> Note:
        self.path.mkdir(parents=True, exist_ok=True)
        note = self.get_last_note()
        note.index += 1
        return note
