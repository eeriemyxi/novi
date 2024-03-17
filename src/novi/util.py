import logging

from blessings import Terminal

from novi import constants, struct

log = logging.getLogger(__name__)
t = Terminal()


def serialize_word(word: str) -> str:
    return word.replace(" ", "-")


def hyperlink(url: str, label: str) -> str:
    return f"\033]8;;{url}\033\\{label}\033]8;;\033\\"


def inform_invalid_word(word: str) -> None:
    print(t.bold_red(f"{struct.Emoji.WARNING.value} Could not find word: {word!r}"))


def inform_searching_word(word: str) -> None:
    print(t.bold_green(f"{struct.Emoji.DIM_BUTTON.value} Searching for: {word!r}"))


def inform_found_word(word: str) -> None:
    print(t.bold_green(f"{struct.Emoji.HEARTS.value}  Found word: {word!r}"))


def output_word(word: str, end: str) -> None:
    print(t.bold_green(f"{struct.Emoji.SMALL_BLUE_DIAMOND.value}{word}"), end=end)


def output_word_class(word_class: struct.WordClass, end: str) -> None:
    if word_class.cls:
        print(t.bold_yellow(f" ({word_class.cls})"), end=end)

    if word_class.code:
        print(
            t.bright_red(" ["),
            t.bold_yellow(hyperlink(constants.CODES_LINK, word_class.code)),
            t.bright_red("]"),
            sep="",
            end="",
        )

    print()


def output_word_def(df: str, indent: int) -> None:
    print(t.bold_white(f"{' ' * indent}{struct.Emoji.SMALL_ORANGE_DIAMOND.value}{df}"))


def output_def_example(exm: str, indent: int) -> None:
    print(
        t.italic_white(
            f"{' ' * indent}{exm}".replace(t.normal, t.normal + t.italic + t.white)
        )
    )
