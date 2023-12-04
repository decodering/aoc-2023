from src.utils import read_text_file
from pathlib import Path
from os.path import join
from textwrap import dedent


def get_current_file_dir() -> str:
    return f"{Path(__file__).absolute().parent.resolve()}"


TEST1_TXT = join(get_current_file_dir(), "inputs", "test1.txt")
TEST2_TXT = join(get_current_file_dir(), "inputs", "test2.txt")
INPUT_TXT = join(get_current_file_dir(), "inputs", "input.txt")
SAMPLE_TXT = join(get_current_file_dir(), "inputs", "sample.txt")

if __name__ == "__main__":
    lines = read_text_file(INPUT_TXT)
    to_sum = []
    for line in lines:
        num = ""
        for char in line:
            if char.isdigit():
                num += char
                break
        for char in reversed(line):
            if char.isdigit():
                num += char
                break
        to_sum.append(int(num))
    sum_answer_digit_chars_only = sum(to_sum)

    # Task 2: Replace substring for actual digits and then repeat above
    to_sum = []
    for line in lines:
        line = line.lower()
        for digit_str, digit_int in [
            ("one", "1"),
            ("two", "2"),
            ("three", "3"),
            ("four", "4"),
            ("five", "5"),
            ("six", "6"),
            ("seven", "7"),
            ("eight", "8"),
            ("nine", "9"),
        ]:
            if digit_str in line:
                # Append first and last chars so that it works for continuous string edge cases:
                # E.g.: eightwothree -> ['eight','two','three]
                line = line.replace(
                    digit_str, f"{digit_str[0]}{digit_str}{digit_str[-1]}"
                )
                line = line.replace(digit_str, digit_int)
        num = ""
        for char in line:
            if char.isdigit():
                num += char
                break
        for char in reversed(line):
            if char.isdigit():
                num += char
                break
        to_sum.append(int(num))
    sum_answer_full = sum(to_sum)

    print(
        dedent(
            f"""
            Task 1 answer: {sum_answer_digit_chars_only}
            Task 2 answer: {sum_answer_full}
          """
        )
    )
