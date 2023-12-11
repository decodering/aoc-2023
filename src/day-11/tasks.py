from os.path import join
from pathlib import Path
from typing import List, Union
from itertools import combinations
from src.utils import read_text_file
from math import comb
import numpy as np


def get_current_file_dir() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


TEST1_TXT = join(get_current_file_dir(), "inputs", "test1.txt")
TEST2_TXT = join(get_current_file_dir(), "inputs", "test2.txt")
INPUT_TXT = join(get_current_file_dir(), "inputs", "input.txt")
SAMPLE_TXT = join(get_current_file_dir(), "inputs", "sample.txt")


def get_galaxy_shortest_distances_wexpansion(
    parsed: np.ndarray,
    galaxy_locs: List[tuple],
    expansion: int = (1_000_000 - 1),
):
    distances = []

    cols_to_expand = []
    rows_to_expand = []

    rows_with_galaxies = [y for y, _ in galaxy_locs]
    cols_with_galaxies = [x for _, x in galaxy_locs]

    m, n = parsed.shape
    for y in range(m):
        if y in rows_with_galaxies:
            continue
        if "#" not in parsed[y, :]:
            rows_to_expand.append(y)
    for x in range(n):
        if x in cols_with_galaxies:
            continue
        if "#" not in parsed[:, x]:
            cols_to_expand.append(x)

    for location_pair in combinations(galaxy_locs, 2):
        distance = get_shortest_distance_wexpansion(
            location_pair[0],
            location_pair[1],
            cols_to_expand,
            rows_to_expand,
            expansion,
        )
        distances.append(distance)
    return distances


def get_galaxy_shortest_distances(
    parsed: np.ndarray,
    galaxy_locs: List[tuple],
    expansion: int = 1,
):
    distances = []

    cols_to_expand = []
    rows_to_expand = []

    rows_with_galaxies = [y for y, _ in galaxy_locs]
    cols_with_galaxies = [x for _, x in galaxy_locs]

    m, n = parsed.shape
    for y in range(m):
        if y in rows_with_galaxies:
            continue
        if "#" not in parsed[y, :]:
            rows_to_expand.append(y)
    for x in range(n):
        if x in cols_with_galaxies:
            continue
        if "#" not in parsed[:, x]:
            cols_to_expand.append(x)

    _, n = parsed.shape
    for offset, y in enumerate(sorted(rows_to_expand)):
        offset *= expansion
        newline = np.full((expansion, n), ".")
        parsed = np.insert(parsed, y + offset, newline, axis=0)
    m, _ = parsed.shape
    for offset, x in enumerate(sorted(cols_to_expand)):
        offset *= expansion
        newline = np.full((m, expansion), ".")
        parsed = np.insert(parsed, x + offset, newline.transpose(), axis=1)

    # [print("".join(line)) for line in parsed]

    galaxy_locs = get_galaxy_locs(parsed)
    for location_pair in combinations(galaxy_locs, 2):
        distance = get_shortest_distance(location_pair[0], location_pair[1])
        distances.append(distance)
    return distances


def parse_input1(lines):
    lines = [[c for c in l] for l in lines]
    lines = np.array(lines)
    return lines, get_galaxy_locs(lines)


def get_galaxy_locs(parsed: np.ndarray) -> List[tuple]:
    galaxy_locations = []
    for y, line in enumerate(parsed):
        x_vals = np.where(line == "#")[0]
        if x_vals.size > 0:
            galaxy_locations.extend([(y, x) for x in x_vals])
    return galaxy_locations


def get_shortest_distance_wexpansion(loc1, loc2, cols_to_expand, rows_to_expand, expansion):
    y1, x1 = loc1
    y2, x2 = loc2

    rows_expansion_count = 0
    cols_expansion_count = 0
    for y in rows_to_expand:
        if min(y1, y2) < y < max(y1, y2):
            rows_expansion_count += expansion
    for x in cols_to_expand:
        if min(x1, x2) < x < max(x1, x2):
            cols_expansion_count += expansion

    return abs(y1 - y2) + abs(x1 - x2) + rows_expansion_count + cols_expansion_count


def get_shortest_distance(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


def main(
    input_file: str = INPUT_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed, galaxy_locs = parse_input1(lines)

    distances = get_galaxy_shortest_distances(parsed, galaxy_locs)
    task1_answer = sum(distances)

    distances = get_galaxy_shortest_distances_wexpansion(parsed, galaxy_locs)
    task2_answer = sum(distances)

    return [task1_answer, task2_answer]
