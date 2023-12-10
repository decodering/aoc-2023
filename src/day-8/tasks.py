from concurrent.futures import ProcessPoolExecutor
from os.path import join
from pathlib import Path
from typing import List
from math import lcm
from src.utils import read_text_file


def get_current_file_dir() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


TEST1_TXT = join(get_current_file_dir(), "inputs", "test1.txt")
TEST2_TXT = join(get_current_file_dir(), "inputs", "test2.txt")
INPUT_TXT = join(get_current_file_dir(), "inputs", "input.txt")
SAMPLE_TXT = join(get_current_file_dir(), "inputs", "sample.txt")


def get_num_steps_ghost_parallel(parsed, debug=False):
    # CLUE: > 43_981_700_000
    """
    > for each starting point
    > Compute the first Z in parallel
    > then even out each starting point to the longest current path so it resets to the same num steps per point
    > continue process for the next z for each path in parallel again
    >
    """
    pass


def get_num_steps_ghost(parsed, debug=False):
    # CLUE: > 43_981_700_000
    curr_points = {i: k for i, k in enumerate(parsed.keys()) if k.endswith("A")}

    steps_sequence_len = len(parsed["instruct"])
    steps_taken = 0
    BREAK_FLAG = False

    a_to_z_steps = {i: None for i, k in curr_points.items()}
    start_to_end_mapping = {}

    if debug:
        print(curr_points)
    while not BREAK_FLAG:
        # if (steps_taken % (steps_sequence_len * 10_000)) == 0:
        #     print(
        #         f"\r{steps_taken:_} steps taken. ({len(start_to_end_mapping.keys()):_}/{len(parsed.keys())-1:_} keys mapped!). {a_to_z_steps}",
        #         end="",
        #     )

        if all(v.endswith("Z") for v in curr_points.values()):
            BREAK_FLAG = True
            break

        starting_points = curr_points.copy()
        for step in parsed["instruct"]:
            for i, curr_point in curr_points.items():
                if step == "L":
                    curr_points[i] = parsed[curr_point][0]
                else:
                    curr_points[i] = parsed[curr_point][1]
                if curr_points[i].endswith("Z") and a_to_z_steps[i] is None:
                    a_to_z_steps[i] = steps_taken + 1
            if debug:
                print(curr_points)
            steps_taken += 1

        if all([(_ is not None) for _ in a_to_z_steps.values()]):
            steps_taken = lcm(*a_to_z_steps.values())
            BREAK_FLAG = True
            break

    print("")
    return steps_taken


def get_num_steps(parsed, debug=False):
    curr_point = "AAA"
    end_point = "ZZZ"
    steps_taken = 0

    if debug:
        print(curr_point)
    while curr_point != end_point:
        for step in parsed["instruct"]:
            if curr_point == end_point:
                break

            if step == "L":
                curr_point = parsed[curr_point][0]
            else:
                curr_point = parsed[curr_point][1]
            if debug:
                print(curr_point)
            steps_taken += 1

    return steps_taken


def parse_lines1(lines: List[str]) -> dict:
    parsed = {}
    parsed["instruct"] = lines.pop(0)

    lines = [l for l in lines if l]

    for line in lines:
        line = line.split(" = ")
        parsed[line[0]] = tuple(line[-1][1:-1].split(", "))

    return parsed


def main(
    input_file: str = INPUT_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = parse_lines1(lines)

    task1_answer = get_num_steps(parsed=parsed)
    task2_answer = get_num_steps_ghost(parsed)

    return (task1_answer, task2_answer)
