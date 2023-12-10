#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def main():
    # Use a cross-platform method to get the home directory
    home_dir = Path.home()

    # Define the directory for notes
    note_dir = home_dir / "notes" / "seeds"

    # Check if the directory exists, if not, create it
    note_dir.mkdir(parents=True, exist_ok=True)

    # Find the highest numbered file
    highest_num = 0
    for file in note_dir.glob('*.md'):
        file_num = file.stem
        if file_num.isdigit():
            highest_num = max(highest_num, int(file_num))

    # Determine the next file name
    next_num = highest_num + 1
    new_file = note_dir / f"{next_num}.md"

    # Open the new file in the editor
    editor = os.getenv('EDITOR', 'notepad' if sys.platform == 'win32' else 'vim')
    subprocess.run([editor, str(new_file)])

if __name__ == "__main__":
    main()

