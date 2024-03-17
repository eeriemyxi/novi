import dataclasses
import enum


class SupportedLanguage(enum.Enum):
    ENGLISH = "english"


class Emoji(enum.Enum):
    WARNING = "⚠"
    DIM_BUTTON = "🔅"
    HEARTS = "♥"
    SMALL_BLUE_DIAMOND = "🔹"
    SMALL_ORANGE_DIAMOND = "🔸"


@dataclasses.dataclass
class WordClass:
    cls: str
    code: str


@dataclasses.dataclass
class WordDefinition:
    text: str
    examples: list[str]


@dataclasses.dataclass
class WordBody:
    word: str
    word_class: WordClass | None
    def_texts: list[WordDefinition]
