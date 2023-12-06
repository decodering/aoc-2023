import math
from os.path import join
from pathlib import Path
from typing import List

from src.utils import read_text_file


def get_current_file_dir() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


TEST1_TXT = join(get_current_file_dir(), "inputs", "test1.txt")
TEST2_TXT = join(get_current_file_dir(), "inputs", "test2.txt")
INPUT_TXT = join(get_current_file_dir(), "inputs", "input.txt")
SAMPLE_TXT = join(get_current_file_dir(), "inputs", "sample.txt")

BOAT_STARTING_SPEED = 0  # mm/ms
SPEED_INCREASE = 1  # mm/ms


def get_hold_button_times(parsed: List[List[int]]) -> dict:
    hold_button_times = {}
    for ind, (time, distance) in enumerate(zip(*parsed)):
        # (t*SPEED_INCREASE + BOAT_STARTING_SPEED)*(time-t)=d
        # -t^2 + 7*t = max(d) (t<7)
        res = []
        for t in range(1, time):
            d = t * (time - t)
            if d > distance:
                res.append((t, d))
        hold_button_times[f"race {ind}"] = res
    return hold_button_times


def get_parsed_input_1(lines: List[str]) -> List[List[int]]:
    parsed_lines = []
    for line in lines:
        parsed_lines.append([int(_) for _ in line.split(":")[-1].split(" ") if _])

    return parsed_lines


def get_parsed_input_2(lines: List[str]) -> List[List[int]]:
    parsed_lines = []
    for line in lines:
        parsed_lines.append(int(line.split(":")[-1].replace(" ", "")))

    return [[_] for _ in parsed_lines]


def main(
    input_file: str = INPUT_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = get_parsed_input_1(lines=lines)

    hold_button_times = get_hold_button_times(parsed=parsed)
    product_of_winning_times_per_race = math.prod(
        [len(_) for _ in hold_button_times.values()]
    )

    parsed = get_parsed_input_2(lines=lines)
    hold_button_times = get_hold_button_times(parsed=parsed)
    task2_answer = len(hold_button_times["race 0"])

    return [product_of_winning_times_per_race, task2_answer]
