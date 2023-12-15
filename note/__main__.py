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
        help='Set the mode of operation (default: "note")'
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the mode value
    main(mode=args.mode)


if __name__ == "__main__":
    entrypoint()
