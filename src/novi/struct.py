import dataclasses
import enum


class SupportedLanguage(enum.Enum):
    ENGLISH = "english"


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
