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
    word: str
    word_class: WordClass | None
    def_texts: list[str]
