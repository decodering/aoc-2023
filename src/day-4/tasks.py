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


def get_num_cards_per_card(card_scores: dict, parsed: dict) -> dict:
    num_cards = {}
    for key in card_scores.keys():
        card_score = card_scores[key]
        current_nums, winning_nums = parsed[key]
    return num_cards


def get_score_per_card(parsed: dict) -> dict:
    card_scores = {}
    for key, line in parsed.items():
        score_cnt = 0
        current_nums, winning_nums = line
        for num in current_nums:
            if num in winning_nums:
                score_cnt += 1
        card_scores[key] = 2 ** (score_cnt - 1) if score_cnt else score_cnt
    return card_scores


def get_parsed_input_1(lines: List[str]) -> dict:
    """Replace * symbols with standard 'S' letter."""

    parsed_lines = {}
    for line in lines:
        key, val = line.split(":")
        key = key.split(" ")[-1]
        val = [_.rstrip().lstrip().split(" ") for _ in val.split(" | ")]

        # Prune empty ones
        output_list = []
        for s in val:
            output_set = []
            for v in s:
                if v:
                    output_set.append(v)
            output_list.append(output_set)
        parsed_lines[key] = output_list

    return parsed_lines


def main(
    input_file: str = TEST2_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = get_parsed_input_1(lines=lines)

    # score_counts = get_score_per_card(parsed=parsed)
    # task1_answer = sum([_ for _ in score_counts.values()])

    num_cards = get_num_cards_per_card(parsed=parsed)

    # _ = [print(_) for _ in lines]
    # print("")
    # _ = [print(f"{k}: {v}") for k, v in parsed.items()]
    # print("")
    # print(score_counts)
    # print("")

    # print(task1_answer)
    print(num_cards)
