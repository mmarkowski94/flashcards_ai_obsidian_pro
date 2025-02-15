from pathlib import Path


def open_file(file_path: Path):
    """
    Opens a file and returns its content as a string.

    Args:
        file_path (Path): The path to the file to be opened.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file at the specified path does not exist.
        IOError: If an error occurs while opening or reading the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()