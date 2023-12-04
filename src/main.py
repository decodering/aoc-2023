from os.path import join
from pathlib import Path
from textwrap import dedent

import typer
from typing_extensions import Annotated
from src.utils import import_file


def get_current_file_path() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


def run_file(
    day_num: Annotated[int, typer.Argument()],
    debug: Annotated[bool, typer.Option()] = False,
):
    tasks_file = join(get_current_file_path(), f"day-{day_num}", "tasks.py")
    tasks_file = import_file(tasks_file)

    if debug:
        tasks_file.main()
        return

    task1_answer, task2_answer = tasks_file.main()
    print(
        dedent(
            f"""
            Task 1 answer: {task1_answer}
            Task 2 answer: {task2_answer}
          """
        )
    )


if __name__ == "__main__":
    typer.run(run_file)
