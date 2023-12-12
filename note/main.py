import os
import subprocess
import sys
from pathlib import Path
from pydantic import BaseModel

import magic
from model import FilePath

MODE = "TEACH"

def grow(seed: str, target: str) -> str:
    ## does magic and grows the seed into another representation
    return magic.simple(seed, target)

def create_new_note(branch_name):
    """
    in note mode:
        just creates the note file and exits
    in teaching mode:
        lets the ai attempt to improve the note
        lets the user improve the mutated string
        improve or approve it
    in auto mode:
        uses the optimize.pt system message
        this is a file you should definitely edit
        goal is to improve it periodically

    if success then returns true
    else false
    """
    seed_file = FilePath.from_home_dir(branch_name)
    seed_file.open_in_editor()

    seed = seed_file.read_content()

    if MODE == "NOTE":
        return True

    return False

def main():
    create_new_note("seeds")

if __name__ == "__main__":
    main()
