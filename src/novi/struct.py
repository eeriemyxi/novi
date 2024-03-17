from dataclasses import dataclass
from enum import Enum


class SupportedLanguage(Enum):
    ENGLISH = "english"


class Emoji(Enum):
    WARNING = "⚠"
    DIM_BUTTON = "🔅"
    HEARTS = "♥"
    SMALL_BLUE_DIAMOND = "🔹"
    SMALL_ORANGE_DIAMOND = "🔸"


@dataclass
class WordClass:
    cls: str
    code: str


@dataclass
class WordDefinition:
    text: str
    examples: list[str]


@dataclass
class WordBody:
    word: str
    word_class: WordClass | None
    def_texts: list[WordDefinition]
