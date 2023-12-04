from pathlib import Path


def read_text_file(input_file_path: str) -> list:
    with open(input_file_path) as file:
        lines = file.read().splitlines()
    return lines


def get_current_file_path() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"
