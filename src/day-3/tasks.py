from os.path import join
from pathlib import Path
from typing import List
import numpy as np
from src.utils import read_text_file


def get_current_file_dir() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


TEST1_TXT = join(get_current_file_dir(), "inputs", "test1.txt")
TEST2_TXT = join(get_current_file_dir(), "inputs", "test2.txt")
INPUT_TXT = join(get_current_file_dir(), "inputs", "input.txt")
SAMPLE_TXT = join(get_current_file_dir(), "inputs", "sample.txt")


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def get_gear_part_numbers(parsed: List[str], debug: bool = True) -> dict:
    part_numbers_per_gear = {}

    for ind, line in enumerate(parsed):
        if "*" not in line:
            continue

        num_values = [_ for _ in line.replace("*", ".").split(".") if _]
        prev_line = parsed[ind - 1] if ind > 0 else None
        next_line = parsed[ind + 1] if ind < (len(parsed) - 1) else None
        max_num_char_len = (
            max([len(num_str) for num_str in num_values]) if num_values else 0
        )

        idxs_of_gears = list(find_all(line, "*"))
        for idx in idxs_of_gears:
            pass


def get_part_numbers(parsed: List[str], debug: bool = True) -> dict:
    part_numbers_per_line = {}

    for ind, line in enumerate(parsed):
        part_numbers_per_line[ind] = []
        num_values = [_ for _ in line.replace("S", ".").split(".") if _]
        prev_line = parsed[ind - 1] if ind > 0 else None
        next_line = parsed[ind + 1] if ind < (len(parsed) - 1) else None
        max_num_char_len = (
            max([len(num_str) for num_str in num_values]) if num_values else 0
        )

        if debug:
            print(f"{ind}: {num_values}")
        for line_ind, val in enumerate(num_values):
            # TODO: e.g. if '7' also present in '73'
            # how bout duplicates?...
            """
            0. For the current value, check if there are any other exact matches, if so check which nth occurance this is
            1. Find all occurances in idx form
            2. For each idx occurance, check if found val is exact match (i.e. to substring)
            3. If exact match, check for nth occurance
            """
            duplicate_substr_flag = [True if val in v else False for v in num_values]
            if sum(duplicate_substr_flag) > 1:
                idx_occurances = list(find_all(line, val))
                exact_matches = [i for i, v in enumerate(num_values) if v == val]
                idx_in_exact_matches = [
                    i for i, v in enumerate(exact_matches) if v == line_ind
                ][0]

                # For each occurance, check if substr matches val exactly
                match_hit_cnt = 0
                for idx in idx_occurances:
                    first_token = [
                        _
                        for _ in line[(idx - (max_num_char_len // 2)) :]
                        .replace("S", ".")
                        .split(".")
                        if _
                    ][0]

                    if first_token == val and match_hit_cnt == idx_in_exact_matches:
                        start_idx = idx
                        break
                    elif first_token == val:
                        match_hit_cnt += 1
            else:
                start_idx = line.find(val)
            end_idx = start_idx + len(val) - 1

            if debug:
                print(f"{val}: {start_idx} <-> {end_idx}")
                # if val == "92" and ind == 12:
                #     print("===================")
                #     print(end_idx)
                #     print(line)
                #     print(end_idx < (len(line) - 1))
                #     print(line[end_idx + 1])

            # Perform lateral and longitudinal checks
            if start_idx > 0 and line[start_idx - 1] == "S":
                part_numbers_per_line[ind].append(int(val))
                continue
            if end_idx < (len(line) - 1) and line[end_idx + 1] == "S":
                part_numbers_per_line[ind].append(int(val))
                continue
            for adj_line in [_ for _ in [prev_line, next_line] if _ is not None]:
                idxs_of_symbols = [i for i, x in enumerate(adj_line) if x == "S"]
                adjacent_symbols = [
                    sym_idx
                    for sym_idx in idxs_of_symbols
                    if (start_idx - 1) <= sym_idx <= (end_idx + 1)
                ]
                if adjacent_symbols:
                    part_numbers_per_line[ind].append(int(val))
                    break

    return part_numbers_per_line


def get_parsed_input_1(lines: List[str]) -> list:
    """Replace symbols with standard 'S' letter."""

    parsed_lines = []
    list_of_unique_symbols = []
    for line in lines:
        orig_line = line
        line = line.replace(".", "")

        for char in line:
            if not char.isdigit():
                orig_line = orig_line.replace(char, "S")
                if char not in list_of_unique_symbols:
                    list_of_unique_symbols.append(char)
        parsed_lines.append(orig_line)

    return parsed_lines


def get_parsed_input_2(lines: List[str]) -> list:
    """Replace * symbols with standard 'S' letter."""

    parsed_lines = []
    for line in lines:
        orig_line = line
        line = line.replace(".", "")

        for char in line:
            if not char.isdigit() and char != "*":
                orig_line = orig_line.replace(char, ".")
        parsed_lines.append(orig_line)

    return parsed_lines


def main(
    input_file: str = TEST2_TXT,
    debug: bool = False,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = get_parsed_input_1(lines=lines)

    task1_output = get_part_numbers(parsed=parsed, debug=debug)
    task1_answer = sum([sum(_) for _ in task1_output.values()])

    debug = True
    parsed = get_parsed_input_2(lines=lines)
    task2_output = get_gear_part_numbers(parsed=parsed, debug=debug)

    _ = [print(l) for l in parsed]
    print(f"\n{task2_output}")

    # if debug:
    #     _ = [print(l) for l in parsed]
    #     print("")
    #     for key, val in task1_output.items():
    #         print(f"{key} (x{len(val)}): {val} (=> {sum(val)})")
    # else:
    #     print(f"\n{task1_answer}")
