from os.path import join
from pathlib import Path
from typing import List
from enum import Enum
from src.utils import read_text_file


def get_current_file_dir() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


TEST1_TXT = join(get_current_file_dir(), "inputs", "test1.txt")
TEST2_TXT = join(get_current_file_dir(), "inputs", "test2.txt")
INPUT_TXT = join(get_current_file_dir(), "inputs", "input.txt")
SAMPLE_TXT = join(get_current_file_dir(), "inputs", "sample.txt")


MAPPING = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

MAPPING2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


class HandType(Enum):
    FIVE_OF_A_KIND = 1
    FOUR_OF_A_KIND = 2
    FULL_HOUSE = 3
    THREE_OF_A_KIND = 4
    TWO_PAIR = 5
    ONE_PAIR = 6
    HIGH_CARD = 7


def get_total_winnings2(parsed: List) -> dict:
    hand_winnings = {}
    res = {
        HandType.FIVE_OF_A_KIND: [],
        HandType.FOUR_OF_A_KIND: [],
        HandType.FULL_HOUSE: [],
        HandType.THREE_OF_A_KIND: [],
        HandType.TWO_PAIR: [],
        HandType.ONE_PAIR: [],
        HandType.HIGH_CARD: [],
    }

    for ind, line in enumerate(parsed):
        hand, bid = line
        unique_vals = set(hand)
        num_unique_vals = len(unique_vals)
        j_count = hand.count("J")
        val_counts = [hand.count(_) for _ in unique_vals]
        if num_unique_vals == 1:
            res[HandType.FIVE_OF_A_KIND].append([ind, hand, bid])
        elif num_unique_vals == 2:
            if j_count:
                res[HandType.FIVE_OF_A_KIND].append([ind, hand, bid])
            elif 4 in val_counts:
                res[HandType.FOUR_OF_A_KIND].append([ind, hand, bid])
            else:
                res[HandType.FULL_HOUSE].append([ind, hand, bid])
        elif num_unique_vals == 3:
            if 3 in val_counts:
                if j_count:
                    res[HandType.FOUR_OF_A_KIND].append([ind, hand, bid])
                else:
                    res[HandType.THREE_OF_A_KIND].append([ind, hand, bid])
            else:
                if j_count == 2:
                    res[HandType.FOUR_OF_A_KIND].append([ind, hand, bid])
                elif j_count == 1:
                    res[HandType.FULL_HOUSE].append([ind, hand, bid])
                else:
                    res[HandType.TWO_PAIR].append([ind, hand, bid])
        elif num_unique_vals == 4:
            if j_count:
                res[HandType.THREE_OF_A_KIND].append([ind, hand, bid])
            else:
                res[HandType.ONE_PAIR].append([ind, hand, bid])
        else:
            if j_count:
                res[HandType.ONE_PAIR].append([ind, hand, bid])
            else:
                res[HandType.HIGH_CARD].append([ind, hand, bid])

    rank_count = 0
    num_lines = len(parsed)
    for key in sorted(res.keys(), key=lambda x: x.value):
        val = res[key]
        if not val:
            continue

        # Sort by first element
        res[key] = sorted(val, key=lambda x: tuple(MAPPING2[i] for i in x[1]), reverse=True)
        res[key] = [
            (ind, hand, bid, num_lines - (i + rank_count))
            for i, (ind, hand, bid) in enumerate(res[key])
        ]
        for ind, _, bid, rank in res[key]:
            hand_winnings[ind] = (bid, rank)

        rank_count += len(val)

    return res, hand_winnings


def get_total_winnings(parsed: List) -> dict:
    hand_winnings = {}
    res = {
        HandType.FIVE_OF_A_KIND: [],
        HandType.FOUR_OF_A_KIND: [],
        HandType.FULL_HOUSE: [],
        HandType.THREE_OF_A_KIND: [],
        HandType.TWO_PAIR: [],
        HandType.ONE_PAIR: [],
        HandType.HIGH_CARD: [],
    }

    for ind, line in enumerate(parsed):
        hand, bid = line
        unique_vals = set(hand)
        num_unique_vals = len(unique_vals)
        val_counts = [hand.count(_) for _ in unique_vals]
        if num_unique_vals == 1:
            res[HandType.FIVE_OF_A_KIND].append([ind, hand, bid])
        elif num_unique_vals == 2:
            if 4 in val_counts:
                res[HandType.FOUR_OF_A_KIND].append([ind, hand, bid])
            else:
                res[HandType.FULL_HOUSE].append([ind, hand, bid])
        elif num_unique_vals == 3:
            if 3 in val_counts:
                res[HandType.THREE_OF_A_KIND].append([ind, hand, bid])
            else:
                res[HandType.TWO_PAIR].append([ind, hand, bid])
        elif num_unique_vals == 4:
            res[HandType.ONE_PAIR].append([ind, hand, bid])
        else:
            res[HandType.HIGH_CARD].append([ind, hand, bid])

    rank_count = 0
    num_lines = len(parsed)
    for key in sorted(res.keys(), key=lambda x: x.value):
        val = res[key]
        if not val:
            continue

        # Sort by first element
        res[key] = sorted(val, key=lambda x: tuple(MAPPING[i] for i in x[1]), reverse=True)
        res[key] = [
            (ind, hand, bid, num_lines - (i + rank_count))
            for i, (ind, hand, bid) in enumerate(res[key])
        ]
        for ind, _, bid, rank in res[key]:
            hand_winnings[ind] = (bid, rank)

        rank_count += len(val)

    return res, hand_winnings


def get_parsed_input1(lines: List[str]):
    parsed = []
    for l in lines:
        l = [_.strip() for _ in l.split(" ")]
        l[-1] = int(l[-1])
        parsed.append(l)
    return parsed


def main(
    input_file: str = INPUT_TXT,
) -> List[int]:
    lines = read_text_file(input_file)
    parsed = get_parsed_input1(lines)
    res, hand_winnings = get_total_winnings(parsed)
    task1_answer = sum([bid * rank for bid, rank in hand_winnings.values()])

    res, hand_winnings = get_total_winnings2(parsed)
    task2_answer = sum([bid * rank for bid, rank in hand_winnings.values()])

    return task1_answer, task2_answer
