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


def get_sum_of_power_of_sets(min_playable_combos: dict) -> int:
    total = 0
    for min_playable_combo in min_playable_combos.values():
        total += np.prod(min_playable_combo)
    return total


def get_minimum_playable_combo(parsed: dict) -> dict:
    minimum_playable_combo_per_game = {}
    for game_id, cube_combo_sets in parsed.items():
        red_cubes_per_set = [el[0] for el in cube_combo_sets]
        green_cubes_per_set = [el[1] for el in cube_combo_sets]
        blue_cubes_per_set = [el[2] for el in cube_combo_sets]
        minimum_playable_combo_per_game[game_id] = (
            max(red_cubes_per_set),
            max(green_cubes_per_set),
            max(blue_cubes_per_set),
        )
    return minimum_playable_combo_per_game


def get_valid_games(parsed: dict, valid_combo_set: list = None) -> List[int]:
    if valid_combo_set is None:
        valid_combo_set = [12, 13, 14]
    RED_VALID = valid_combo_set[0]
    GREEN_VALID = valid_combo_set[1]
    BLUE_VALID = valid_combo_set[2]
    valid_game_ids = []
    for game_id, cube_combo_sets in parsed.items():
        red_cubes_per_set = [el[0] for el in cube_combo_sets]
        green_cubes_per_set = [el[1] for el in cube_combo_sets]
        blue_cubes_per_set = [el[2] for el in cube_combo_sets]

        if not all([el <= RED_VALID for el in red_cubes_per_set]):
            continue
        if not all([el <= GREEN_VALID for el in green_cubes_per_set]):
            continue
        if not all([el <= BLUE_VALID for el in blue_cubes_per_set]):
            continue

        valid_game_ids.append(game_id)

    return valid_game_ids


def get_parsed_input(lines: List[str]) -> dict:
    output = {}
    for line in lines:
        game_id, cube_combo_sets = line.split(":")
        game_id = game_id.split(" ")[-1]
        cube_combo_sets = [el.rstrip().lstrip() for el in cube_combo_sets.split(";")]

        # Intended output: [(R,G,B), ...]
        rgb_list_tuples = []
        for combo_set in cube_combo_sets:
            RED, GREEN, BLUE = 0, 0, 0
            cubes_in_combo = [el.lstrip().rstrip() for el in combo_set.split(", ")]
            for cube in cubes_in_combo:
                if "red" in cube:
                    RED = int(cube.split(" ")[0])
                elif "green" in cube:
                    GREEN = int(cube.split(" ")[0])
                else:
                    BLUE = int(cube.split(" ")[0])
            rgb_list_tuples.append((RED, GREEN, BLUE))

        if game_id in output.keys():
            raise ValueError
        output[game_id] = rgb_list_tuples
    return output


def main(
    input_file: str = INPUT_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = get_parsed_input(lines=lines)
    task1_output = get_valid_games(parsed=parsed)
    task1_answer = sum([int(el) for el in task1_output])

    min_playable_combos = get_minimum_playable_combo(parsed=parsed)
    task_2_answer = get_sum_of_power_of_sets(min_playable_combos=min_playable_combos)

    return [task1_answer, task_2_answer]
