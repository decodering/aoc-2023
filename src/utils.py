from pathlib import Path
import os
from contextlib import contextmanager
from importlib.util import module_from_spec, spec_from_file_location


def read_text_file(input_file_path: str) -> list:
    with open(input_file_path) as file:
        lines = file.read().splitlines()
    return lines


def get_current_file_path() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


def import_file(absolute_path: str):
    """
    implementation taken from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly

    https://stackoverflow.com/a/67692
    https://stackoverflow.com/a/41904558
    """

    @contextmanager
    def add_to_path(p):
        import sys

        old_path = sys.path
        sys.path = sys.path[:]
        sys.path.insert(0, p)
        try:
            yield
        finally:
            sys.path = old_path

    with add_to_path(os.path.dirname(absolute_path)):
        spec = spec_from_file_location(absolute_path, absolute_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
