import sys

from elemental_tools.cli import ArgumentParser
from elemental_tools.code.countlines import count_lines_in_directory


class CountLines(ArgumentParser):
    description = "Count lines "

    def __init__(self):
        super().__init__()
        self.add_argument("--extension", "-e", help="The extension of that files that you want to count lines")


if __name__ == "__main__":

    reproved = False

    if len(sys.argv) != 2:
        directory_path = None
        print("Usage: python countlines.py <directory_path>\nOr specify a directory path for me to iterate over\n")

    else:
        directory_path = sys.argv[1]

    while directory_path is None:
        display_message = ""
        if reproved:
            display_message += "Invalid directory.\n"
        display_message = "Enter the directory path or hit Ctrl+C to exit.\n"

        try:
            directory_path = input()
            total_lines = count_lines_in_directory(directory_path)
            print(f"\nTotal lines in all .py files: {total_lines}")

        except:
            reproved = True
            pass