def write_to_file(filepath: str, contents: str) -> None:
    """
    Writes the given string to the given filepath
    """
    with open(filepath, "w") as fp:
        fp.write(contents)
