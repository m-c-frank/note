import os
import sys
from pathlib import Path
from .model import Note, Repository
import fire
import uvicorn

# default location
PATH_NOTES = os.getenv("PATH_NOTES", Path.home() / "notes" / "notes")
EDITOR = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
FILE_EXTENSION = "md"


def get_repo_notes() -> Repository:
    """Get the notes repository."""
    return Repository(node_type=Note)


def create_new_note() -> None:
    """Create and open a new note, default action."""
    repo = get_repo_notes()
    new_note = repo.new_node()
    new_note.edit()


def write_new_note(content: str, silent: str=True) -> None:
    """Create a new note with the given content and open it."""
    repo = get_repo_notes()
    new_note = repo.new_node()
    new_note.write(content)
    if not silent:
        new_note.edit()


def list_notes() -> list:
    """List all notes."""
    repo = get_repo_notes()
    return repo.nodes


def print_note(index: int = -1) -> str:
    """Read a specific note by index."""
    repo = get_repo_notes()
    note = Note.from_repository(repo=repo, index=index)
    return note.meta


def edit_note(index: int = -1):
    """Edit a specific note by index."""
    repo = get_repo_notes()
    note = Note.from_repository(repo=repo, index=index)
    note.edit()


def search_notes(term: str):
    """Search for a term in all notes."""
    repo = get_repo_notes()
    result = ""
    for index in repo.index_nodes:
        note = Note(repo=repo, index=index)
        content = note.meta
        if term.lower() in content:
            result += content
    return result


def serve():
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    app = FastAPI()

    class Note(BaseModel):
        text: str

    def process_text(text: str) -> str:
        write_new_note(text)
        return f"Processed text: {text}"

    @app.post("/")
    async def process(note: Note):
        try:
            result = process_text(note.text)
            return {"result": result}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    uvicorn.run(app, host="localhost", port=8200)


def cli():
    """CLI entry point."""
    if len(sys.argv) == 1:
        create_new_note()
        exit()

    fire.Fire({
        'new': create_new_note,
        'write': write_new_note,
        'list': list_notes,
        'print': print_note,
        'edit': edit_note,
        'search': search_notes,
        'serve': serve,
        'repository': Repository,
    })
