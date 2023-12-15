import argparse
from .main import main


def entrypoint():
    # Create the parser
    parser = argparse.ArgumentParser(description="take notes")

    # Add the --mode option
    parser.add_argument(
        '--mode',
        type=str,
        default='note',
        help='set the mode of operation (default: "note")'
    )

    # Add the --depth option
    parser.add_argument(
        '--depth',
        type=int,
        default=2,
        help='set the depth of operation (default: 2)'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the mode value
    main(mode=args.mode, depth=args.depth)


if __name__ == "__main__":
    entrypoint()
