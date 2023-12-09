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


def get_num_steps_ghost(parsed, debug=False):
    # CLUE: > 43_981_700_000
    curr_points = {i: k for i, k in enumerate(parsed.keys()) if k.endswith("A")}
    steps_taken = 0
    BREAK_FLAG = False

    if debug:
        print(curr_points)
    while not BREAK_FLAG:
        for step in parsed["instruct"]:
            if steps_taken % 10_000 == 0:
                print(f"\r{steps_taken:_} steps taken", end="")

            if all(v.endswith("Z") for v in curr_points.values()):
                BREAK_FLAG = True
                break

            for i, curr_point in curr_points.items():
                if step == "L":
                    curr_points[i] = parsed[curr_point][0]
                else:
                    curr_points[i] = parsed[curr_point][1]
            if debug:
                print(curr_points)
            steps_taken += 1

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

    num_steps = get_num_steps_ghost(parsed, debug=False)

    # print("")
    # _ = [print(k, v) for k, v in parsed.items()]
    print("")
    print(num_steps)
    print("")
