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
    if MODE == "TEACH":
        # perhaps randomly select from a list of aims
        # buf for now just do the story one
        # next will be the research one
        text_target = grow(seed, "story")
        improved_file= FilePath.from_home_dir('seeds')
        improved_file.write_content(text_target + f"\n---\n[seed]({seed_file.path.name})\n---\n")
        improved_file.open_in_editor()
        return True
    if MODE == "AUTO":
        seed_new = grow(seed, "story")
        text_target = grow(seed_new, "optimize")
        return True
    return False

def main():
    create_new_note("seeds")

if __name__ == "__main__":
    main()
