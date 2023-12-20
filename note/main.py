from .mycelium import mutate
from .model import FilePath


def grow(seed: str, target: str) -> str:
    # does magic and grows the seed into another representation
    return mutate(seed, target)


def create_new_note(
    branch_name: str = "seeds",
    seed: str = "note:",
    mode: str = "note",
    depth: int = 1
):
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
    seed_file.write_content(seed)
    seed_file.open_in_editor()

    seed = seed_file.read_content()

    if mode == "note":
        # just a plain note nothing else
        return seed
    else:
        # this is the magic stuff
        if (depth > 0):
            leaf = grow(seed, mode)
            return create_new_note(
                mode,
                seed=leaf,
                mode=mode,
                depth=depth-1
            )
        else:
            return seed


def main(mode, depth):
    print(f"running with mode={mode} and depth={depth}")
    seed = create_new_note("seeds", mode=mode, depth=depth)
    if seed == "":
        return

    # its a language server for natural language

    """ its literally a branching system. its like mycelium.
    it will connect everything, but i want it to be more like
    a superlight network maybe it will literally crystallize
    and we can take the pure essence of language and make something with it.
    you learn language the way you need it to learn.
    its literally a mapping between a model of language
    and your own interface of thoughts. i need to get copilot working again.
    as soon as possible.
    then i can write my notes in code and increase exponentially
    every diff in a commit will be a note
    so you can explain why you did things and can directly reflect
    """


if __name__ == "__main__":
    main("note", 1)
