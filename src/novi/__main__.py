import importlib.metadata
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--debug", help="Enable debug logs.", action="store_true")
parser.add_argument(
    "-V",
    "--version",
    help="Show program version.",
    action="version",
    version=importlib.metadata.version("novi"),
)
parser.add_argument(
    "words",
    help=(
        "Words to search. "
        "You can specify multiple words by splitting them by whitespace."
    ),
    nargs="*",
)

cli_args = parser.parse_args()

import logging  # noqa: E402
import logging.config  # noqa: E402

from requests.sessions import Session  # noqa: E402
from requests.structures import CaseInsensitiveDict  # noqa: E402

logging.basicConfig(
    format="%(message)s",
    datefmt="[%X]",
    level=logging.DEBUG if cli_args.debug else logging.INFO,
)


from novi import constants, http, parser, util  # noqa: E402

log = logging.getLogger(__name__)


def exit_gracefully(session: Session, code: int) -> None:
    session.close()
    exit(code)


def handle_word(session: Session, word: str) -> int:
    util.inform_searching_word(word)

    word_html = http.get_word_file(session, constants.LANGUAGE, word)
    if not word_html:
        util.inform_invalid_word(word)
        return 1

    util.inform_found_word(word)

    word_defs = parser.cambridge.parse_definitions(word_html)
    if not word_defs:
        log.debug(f"Could not parse word definitions for {word=}")
        return 1

    for df in word_defs:
        if not df.def_texts:
            continue
        util.output_word(df.word, "")
        if df.word_class:
            util.output_word_class(df.word_class, "")
        for dt in df.def_texts:
            util.output_word_def(dt.text, 4)
            for exm in dt.examples:
                util.output_def_example(exm, 8)

    return 0


def main() -> tuple[int, Session]:
    session = Session()
    session.headers = CaseInsensitiveDict({"user-agent": constants.USER_AGENT})

    words = cli_args.words

    for word in words:
        word = util.serialize_word(word)
        code = handle_word(session, word)
        log.debug(f"Returned {code=} for `handle_word` of {word=}")

    return 0, session


def _main() -> None:
    """Run main and exit gracefully."""
    # NOTE: this exists because rye prints the return value of `main`
    # so I had to create a silent one. If you know a better way,
    # feel free to send a pull request.
    code, session = main()
    exit_gracefully(session, code)


if __name__ == "__main__":
    _main()
