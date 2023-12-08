from os.path import join
from pathlib import Path
from typing import List
from time import time
from src.utils import read_text_file
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Pool


def get_current_file_dir() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


TEST1_TXT = join(get_current_file_dir(), "inputs", "test1.txt")
TEST2_TXT = join(get_current_file_dir(), "inputs", "test2.txt")
INPUT_TXT = join(get_current_file_dir(), "inputs", "input.txt")
SAMPLE_TXT = join(get_current_file_dir(), "inputs", "sample.txt")


def get_lowest_seed_loc(args) -> int:
    seed_range, parsed = args
    lowest_seed_location = None
    cnt = 0
    # t_start = time()
    # refresh_rate = 100000
    for seed in seed_range:
        # if cnt % refresh_rate == 0:
        #     lowest_seed_location_str = (
        #         lowest_seed_location if lowest_seed_location is not None else 0
        #     )
        #     print(
        #         f"\rProcessed {cnt:_} / {tot_num_seeds:_} seeds. Current lowest seed_loc: {lowest_seed_location_str:_} (time_el: {(time()-t_start)/60:.2f}min, speed: {((time()-t_start))/((cnt+0.001)/refresh_rate):.2f}s/{refresh_rate:_})"
        #         " " * 100,
        #         end="",
        #     )

        source_data_val = seed
        for secn_name in [
            "seed-to-soil",
            "soil-to-fertilizer",
            "fertilizer-to-water",
            "water-to-light",
            "light-to-temperature",
            "temperature-to-humidity",
            "humidity-to-location",
        ]:
            for ind, line in enumerate(parsed[secn_name]):
                dest_start, source_start, range_len = line
                if source_start <= source_data_val <= (source_start + range_len):
                    diff = source_data_val - source_start
                    dest_data_val = dest_start + diff
                    source_data_val = dest_data_val
                    break
                elif ind == (len(parsed[secn_name]) - 1):
                    dest_data_val = source_data_val
            if secn_name.endswith("location") and (
                lowest_seed_location is None or (dest_data_val <= lowest_seed_location)
            ):
                lowest_seed_location = dest_data_val
        cnt += 1
    # print(
    #     f"\nProcessed {cnt} / {tot_num_seeds} seeds. Current lowest seed_loc: {lowest_seed_location}. Done!\n"
    # )
    return lowest_seed_location


def get_seed_location_numbers_short(parsed: dict, debug_range: int = None) -> int:
    raw_seeds = parsed.pop("seed", None)
    new_seeds = []
    for i in range(len(raw_seeds) // 2):
        idx_start = i * 2
        idx_end = (i + 1) * 2
        range_start, range_len = raw_seeds[idx_start:idx_end]
        if debug_range:
            range_len = debug_range  # TODO: DEBUG
        new_seeds.append(range(range_start, (range_start + range_len)))

    tot_num_seeds = sum([len(_) for _ in new_seeds])
    print(
        f"There are {len(new_seeds):_} seed ranges.\nLength of each: {[len(_) for _ in new_seeds]}\nTotal seeds: {tot_num_seeds:_}\n"
    )
    lowest_seed_location = None

    args = [(seed_range, parsed) for seed_range in new_seeds]
    with ProcessPoolExecutor() as executor:
        for r in executor.map(get_lowest_seed_loc, args):
            print(f"Lowest seed loc for range: {r}")
            if lowest_seed_location is None or r <= lowest_seed_location:
                lowest_seed_location = r
    return lowest_seed_location


def get_seed_location_numbers(parsed: dict, debug_range: int = None) -> dict:
    if debug_range:
        raw_seeds = parsed.pop("seed", None)
        new_seeds = []
        for i in range(len(raw_seeds) // 2):
            idx_start = i * 2
            idx_end = (i + 1) * 2
            range_start, range_len = raw_seeds[idx_start:idx_end]
            if debug_range:
                range_len = debug_range  # TODO: DEBUG
            new_seeds.extend(list(range(range_start, (range_start + range_len))))
        parsed["seed"] = new_seeds
    seed_location_numbers = {}
    for seed in parsed["seed"]:
        source_data_val = seed
        seed_location_numbers[seed] = []
        for secn_name in [
            "seed-to-soil",
            "soil-to-fertilizer",
            "fertilizer-to-water",
            "water-to-light",
            "light-to-temperature",
            "temperature-to-humidity",
            "humidity-to-location",
        ]:
            for ind, line in enumerate(parsed[secn_name]):
                dest_start, source_start, range_len = line
                if source_start <= source_data_val <= (source_start + range_len):
                    diff = source_data_val - source_start
                    dest_data_val = dest_start + diff
                    seed_location_numbers[seed].append((source_data_val, dest_data_val))
                    source_data_val = dest_data_val
                    break
                elif ind == (len(parsed[secn_name]) - 1):
                    dest_data_val = source_data_val
                    seed_location_numbers[seed].append((source_data_val, dest_data_val))
    return seed_location_numbers


def get_parsed_input_1(lines: List[str]) -> dict:
    parsed_lines = {}

    # seed info
    line = lines[0]
    parsed_lines["seed"] = [int(_) for _ in line.split(":")[-1].strip().split(" ")]

    idx_seed_soil_line = [i for i, _ in enumerate(lines) if "seed-to-soil map" in _]
    idx_soil_fertilizer_line = [
        i for i, _ in enumerate(lines) if "soil-to-fertilizer map" in _
    ]
    idx_fertilizer_water_line = [
        i for i, _ in enumerate(lines) if "fertilizer-to-water map" in _
    ]
    idx_water_light_line = [i for i, _ in enumerate(lines) if "water-to-light map" in _]
    idx_light_temperature_line = [
        i for i, _ in enumerate(lines) if "light-to-temperature map" in _
    ]
    idx_temperature_humidity_line = [
        i for i, _ in enumerate(lines) if "temperature-to-humidity map" in _
    ]
    idx_humidity_location_line = [
        i for i, _ in enumerate(lines) if "humidity-to-location map" in _
    ]

    for line in [
        idx_seed_soil_line,
        idx_soil_fertilizer_line,
        idx_fertilizer_water_line,
        idx_water_light_line,
        idx_light_temperature_line,
        idx_temperature_humidity_line,
        idx_humidity_location_line,
    ]:
        assert len(line) == 1

    for section_name, idx_start, idx_end in [
        ("seed-to-soil", idx_seed_soil_line[0], idx_soil_fertilizer_line[0]),
        (
            "soil-to-fertilizer",
            idx_soil_fertilizer_line[0],
            idx_fertilizer_water_line[0],
        ),
        ("fertilizer-to-water", idx_fertilizer_water_line[0], idx_water_light_line[0]),
        ("water-to-light", idx_water_light_line[0], idx_light_temperature_line[0]),
        (
            "light-to-temperature",
            idx_light_temperature_line[0],
            idx_temperature_humidity_line[0],
        ),
        (
            "temperature-to-humidity",
            idx_temperature_humidity_line[0],
            idx_humidity_location_line[0],
        ),
        ("humidity-to-location", idx_humidity_location_line[0], len(lines)),
    ]:
        section_lines = [line for line in lines[idx_start:idx_end] if line]
        parsed_lines[section_name] = [
            [int(_) for _ in line.strip().split(" ")] for line in section_lines[1:]
        ]

    return parsed_lines


def main(
    input_file: str = INPUT_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = get_parsed_input_1(lines=lines)

    seed_location_numbers = get_seed_location_numbers(parsed=parsed)
    task1_answer = min([_[-1][-1] for _ in seed_location_numbers.values()])

    task2_answer = get_seed_location_numbers_short(parsed=parsed)

    return [task1_answer, task2_answer]
