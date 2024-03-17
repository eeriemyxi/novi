import logging

import rich

from novi import constants, struct

log = logging.getLogger(__name__)


def serialize_word(word: str) -> str:
    return word.replace(" ", "-")


def inform_invalid_word(console: rich.console.Console, word: str) -> None:
    console.print(f":warning: Could not find word: {word!r}", style="danger")


def inform_searching_word(console: rich.console.Console, word: str) -> None:
    console.print(f":dim_button: Searching for: {word!r}", style="info")


def inform_found_word(console: rich.console.Console, word: str) -> None:
    console.print(f":hearts:  Found word: {word!r}", style="info")


def output_word(console: rich.console.Console, word: str, end: str) -> None:
    console.print(f":small_blue_diamond:{word}", style="info", end=end)


def output_word_class(
    console: rich.console.Console, word_class: struct.WordClass, end: str
) -> None:
    if word_class.cls:
        console.print(f" ({word_class.cls})", style="bold yellow", end=end)

    if word_class.code:
        console.print(
            (
                f" [red][[/][bold yellow][link={constants.CODES_LINK}]"
                f"{word_class.code}[/][red]][/]"
            ),
            style="red",
            end="",
        )

    console.print()


def output_word_def(console: rich.console.Console, df: str, indent: int) -> None:
    console.print(f"{' ' * indent}:small_orange_diamond:{df}", style="bold white")


def output_def_example(console: rich.console.Console, exm: str, indent: int) -> None:
    console.print(f"{' ' * indent}{exm}", style="italic white")
