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


def get_seed_location_numbers(parsed: dict) -> dict:
    seed_location_numbers = {}
    for seed in parsed["seed"]:
        source_data_val = seed
        for line in parsed["seed-to-soil"]:
            dest_start, source_start, range_len = line
            if source_start <= source_data_val <= source_start + range_len:
                pass
                $$
    return seed_location_numbers


def get_parsed_input_1(lines: List[str]) -> dict:
    parsed_lines = {}

    # seed info
    line = lines[0]
    parsed_lines["seed"] = [int(_) for _ in line.split(":")[-1].strip().split(" ")]

    idx_seed_soil_line = [i for i, _ in enumerate(lines) if "seed-to-soil map" in _]
    idx_soil_fertilizer_line = [i for i, _ in enumerate(lines) if "soil-to-fertilizer map" in _]
    idx_fertilizer_water_line = [i for i, _ in enumerate(lines) if "fertilizer-to-water map" in _]
    idx_water_light_line = [i for i, _ in enumerate(lines) if "water-to-light map" in _]
    idx_light_temperature_line = [i for i, _ in enumerate(lines) if "light-to-temperature map" in _]
    idx_temperature_humidity_line = [
        i for i, _ in enumerate(lines) if "temperature-to-humidity map" in _
    ]
    idx_humidity_location_line = [i for i, _ in enumerate(lines) if "humidity-to-location map" in _]

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
        ("soil-to-fertilizer", idx_soil_fertilizer_line[0], idx_fertilizer_water_line[0]),
        ("fertilizer-to-water", idx_fertilizer_water_line[0], idx_water_light_line[0]),
        ("water-to-light", idx_water_light_line[0], idx_light_temperature_line[0]),
        ("light-to-temperature", idx_light_temperature_line[0], idx_temperature_humidity_line[0]),
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
    input_file: str = TEST1_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = get_parsed_input_1(lines=lines)

    seed_location_numbers = get_seed_location_numbers(parsed=parsed)

    _ = [print(k, v) for k, v in parsed.items()]
    print(seed_location_numbers)
