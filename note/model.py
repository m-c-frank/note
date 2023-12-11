import os
import subprocess
import sys
from pathlib import Path
from pydantic import BaseModel

FILE_EXTENSION="md"

PATH_NOTES = Path.home() / "notes"

class FilePath(BaseModel):
    path: Path

    @classmethod
    def from_home_dir(cls, subdir: str):
        home_dir = Path.home()
        dir_path = home_dir / "notes" / subdir
        dir_path.mkdir(parents=True, exist_ok=True)

        highest_num = max(
            (int(p.stem) for p in dir_path.glob(f'*.{FILE_EXTENSION}') if p.stem.isdigit()), 
            default=0
        )

        new_file = dir_path / f"{highest_num + 1}.{FILE_EXTENSION}"
        return cls(path=new_file)

    def open_in_editor(self):
        editor = os.getenv('EDITOR', 'notepad' if os.name == 'nt' else 'vim')
        subprocess.run([editor, str(self.path)])

    def read_content(self):
        with open(self.path, "r") as f:
            return f.read()

    def write_content(self, content: str):
        with open(self.path, "w") as f:
            f.write(content)

