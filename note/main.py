from .note import Note, Repository


def main():
    note_repo = Repository()
    note = Note(repo=note_repo)
    note.open()


if __name__ == "__main__":
    main()
