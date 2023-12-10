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


def sum_of_extrapolated_vals_reversed(parsed, debug=False):
    extrapolated_vals = {}
    for ind, line in enumerate(parsed):
        differences_per_level = []
        latest_difference_set = None
        curr_sequence = line

        while latest_difference_set != set([0]):
            differences = []
            for i in range(len(curr_sequence) - 1):
                differences.append(curr_sequence[i + 1] - curr_sequence[i])
            differences_per_level.append(differences)
            curr_sequence = differences
            latest_difference_set = set(differences)

        if debug:
            print(line)
            [print(" ", _) for _ in differences_per_level]
        first_seq_vals = [val[0] for val in differences_per_level[:-1]]
        for i, first_val in enumerate(first_seq_vals):
            if i % 2 == 0:
                first_seq_vals[i] = -first_val
        extrapolated_vals[ind] = line[0] + sum(first_seq_vals)
        if debug:
            print(extrapolated_vals[ind])

    return extrapolated_vals


def sum_of_extrapolated_vals(parsed):
    extrapolated_vals = {}
    for ind, line in enumerate(parsed):
        differences_per_level = []
        latest_difference_set = None
        curr_sequence = line

        while latest_difference_set != set([0]):
            differences = []
            for i in range(len(curr_sequence) - 1):
                differences.append(curr_sequence[i + 1] - curr_sequence[i])
            differences_per_level.append(differences)
            curr_sequence = differences
            latest_difference_set = set(differences)

        last_seq_vals = [val[-1] for val in differences_per_level[:-1]]
        extrapolated_vals[ind] = line[-1] + sum(last_seq_vals)

    return extrapolated_vals


def parse_input1(lines):
    parsed = []
    for line in lines:
        parsed.append([int(l) for l in line.split(" ")])
    return parsed


def main(
    input_file: str = INPUT_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = parse_input1(lines)

    vals = sum_of_extrapolated_vals(parsed)
    task1_answer = sum(v for v in vals.values())

    vals = sum_of_extrapolated_vals_reversed(parsed)
    task2_answer = sum(v for v in vals.values())

    return [task1_answer, task2_answer]
